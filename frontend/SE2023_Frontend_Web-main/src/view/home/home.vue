<template>
  <Row>
    <i-col
      offset="4"
      span="15"
    >
   <Card>
        <Tabs
          v-model="activeTab"
          @on-click="changeTab"
          span="15"
        >
          <TabPane label="热榜" name="recommend">
            <template v-if="items.length !== 0">
                <div  v-for="(item,index) in items" :key="item.id">
                  <Row>
                  <i-col span="1">
                      {{ index+1 }}:
                    </i-col>
                    <i-col span="4">
                      {{ '论文解读' }}:
                    </i-col>
                    <i-col span="11" class="title">
                          <editor v-html="item.title"></editor>
                    </i-col>
                    <i-col offset="4" span="4" >
                      <i-button type="info" style="width: 80px" @click="handleShow(item.id, item.type)">
                        查看详情
                      </i-button>
                    </i-col>
                  </Row>
                  <Divider />
               <Modal v-model="showDetail" footer-hide width="720">
                <PaperCard v-if="showDetail" v-bind='data' />
                </Modal>
                </div>
              <Row v-if="loading">
                <i-col class="demo-spin-col" offset="8" span="8">
                  <Spin fix>
                    <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                    <div>Loading</div>
                  </Spin>
                </i-col>
              </Row>
            </template>
            <template v-else>
              <Row>
                <i-col class="demo-spin-col" offset="8" span="8">
                  <Spin fix>
                    <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                    <div>Loading</div>
                  </Spin>
                </i-col>
              </Row>
            </template>
          </TabPane>
          <!--<TabPane label="关注" name="favorite">
            <template v-if="items.length !== 0">
              <KnowledgeCard
                v-for="item in items"
                :key="item.id"
                v-bind='item'
              />
              <Row v-if="loading">
                <i-col class="demo-spin-col" offset="8" span="8">
                  <Spin fix>
                    <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                    <div>Loading</div>
                  </Spin>
                </i-col>
              </Row>
              <Row v-else-if="hasNextPage">
                <i-col style="text-align: center">
                  <a @click.prevent="loadMoreData"> 加载更多 </a>
                </i-col>
              </Row>
              <Row v-else>
                <i-col style="text-align: center">
                  暂无更多微知识
                </i-col>
              </Row>
            </template>
            <template v-else>
              <Row v-if="loading">
                <i-col class="demo-spin-col" offset="8" span="8">
                  <Spin fix>
                    <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                    <div>Loading</div>
                  </Spin>
                </i-col>
              </Row>
              <div style="text-align: center; font-size: 20px;" v-else>
                <br>
                <br>
                <br>
                暂无关注用户动态
                <br>
                <br>
                <br>
              </div>
            </template>
          </TabPane>-->
        </Tabs>
      </Card>
    </i-col>
  </Row>
</template>

<script>
import PaperCard from '@/view/paper/paper-card'
// import KnowledgeCard from '@/view/micro-knowledge/knowledge-card'
import { InterpretationIdReq} from '@/api/paper'
import { recentKnowledge } from '@/api/user'
import { getTags, recommend } from '@/api/microknowledge'
import { getErrModalOptions, getLocalTime } from '@/libs/util.js'
import editor from '@/components/editor/editor.vue'
export default {
  name: 'home',

  components: { PaperCard,editor},

  data () {
    return {
      activeTab: 'recommend',
      knowledgeType: 'micro-evidence', // TODO: 这个应该用 vuex 记住用户的上一次选择
      selectTagList: [],
      tagSearch: '',
      tagList: [],
      pageIndex: 1,
      hasNextPage: true,
      items: [],
      pageSize: 15,
      idList: [],
      loading: true,
      showDetail: false,
      indec:0
    }
  },

  mounted () {
    getTags('get', {
      pindx: 1,
      num_per_page: 99,
      presupposed: true
    }).then(res => {
      this.tagList = res.data.page.map(tag => ({ value: tag.name, label: tag.name }))
    }).catch(err => {
      console.log(err)
    })
    this.loadData()
  },

  methods: {
    loadData: function () {
      recommend().then(res => {
        const mapData = res.data.map(item => {
          return {
            id: item.id,
            creator: item.created_by,
            title:item.title,
            createAt: getLocalTime(item.created_at),
            publishedYear: item.published_year,
            content: item.content,
            tags: item.tags,
            isLike: item.is_like,
            favorNumber: item.favor_num,
            source: item.source,
            citation: item.citation,
            commentNumber: item.commentNum,
            kind: 1
          }
        })
        this.items.push(...mapData)
        this.loading = false
      }).catch(error => {
        console.log(error)
        this.$Modal.error(getErrModalOptions(error))
      })
    },

    loadFavor: function () {
      this.loading = true
      recentKnowledge({
        pindex: this.pageIndex,
        num_per_page: this.pageSize,
        micro_evidence: true,
        micro_conjecture: true
      }).then(res => {
        const mapData = res.data.page.map(item => {
          return {
            id: item.id,
            creator: item.created_by,
            kind: item.type - 1,
            createAt: getLocalTime(item.created_at),
            publishedYear: item.published_year,
            content: item.content,
            tags: item.tags,
            isLike: item.is_like,
            isCollect: item.is_favor,
            likeNumber: item.like_num,
            favorNumber: item.favor_num,
            displayType: 0,
            source: item.source,
            citation: item.citation,
            evidences: item.evidences
          }
        })
        this.items.push(...mapData)
        this.hasNextPage = res.data.has_next
        this.loading = false
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
    },

    selectType: function (value) {
      this.knowledgeType = value
      // reset
      this.pageIndex = 1
      this.items = []
      this.idList = []
      this.loadData()
    },

    handleShow: function (id, type) {
      InterpretationIdReq(id, type, 'get').then(res => {
        this.data = {
          id: res.data.id,
          creator: res.data.created_by,
          kind: 1,
          source: res.data.source,
          citation: res.data.citation,
          title: res.data.title,
          createAt: getLocalTime(res.data.created_at),
          content: res.data.content,
          tags: res.data.tags,
          isLike: res.data.is_like,
          isCollect: res.data.is_favor,
          likeNumber: res.data.like_num,
          favorNumber: res.data.favor_num,
          publishedYear: res.data.published_year,
          commentNumber: res.data.commentNum
        }
        this.showDetail = true
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
    },

    changeTag: function (tags) {
      this.selectTagList = tags
      this.tagSearch = ''
      tags.forEach(item => {
        this.tagSearch += item + ' '
      })
      this.tagSearch = this.tagSearch.trim()
      this.pageIndex = 1
      this.items = []
      this.idList = []
      this.loadData()
    },

    loadMoreData: function () {
      this.pageIndex += 1
      if (this.activeTab === 'favorite') {
        this.loadFavor()
      } else {
        this.loadData()
      }
    },

    changeTab: function (name) {
      this.activeTab = name
      this.pageIndex = 1
      this.items = []
      this.idList = []
      if (this.activeTab === 'favorite') {
        this.loadFavor()
      } else {
        this.loadData()
      }
    }
  }
}
</script>

<style lang="less">
.ivu-tabs-tab{
  font-size: 20px;
  font-family: -apple-system,BlinkMacSystemFont,Helvetica Neue,PingFang SC,Microsoft YaHei,Source Han Sans SC,Noto Sans CJK SC,WenQuanYi Micro Hei,sans-serif;
}
.type-selector{
  font-size: 16px;
  font-weight: bold;
  padding-bottom: 5px;
}
.title{
  font-size: 16px;
  overflow: hidden;
  -webkit-line-clamp: 2;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
}
</style>
