<template>
  <Row>
    <i-col
      offset="4"
      span="15"
    >
        <Card>
             <Tabs v-model="tabName" @on-click="changeTab">
               <TabPane label="论文解读" name="Interpretation">
              <template v-if="items.length !== 0">
               <PaperCard
               v-for="item in items"
               :key="item.key"
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
                 暂无更多
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
            暂无相关搜索结果
            <br>
            <br>
            <br>
          </div>
              </template>
               </TabPane>
            <!--  <TabPane label="用户" name="user">
               <template v-if="items.length !== 0">
                <Row v-if="loading">
                  <i-col class="demo-spin-col" offset="8" span="8">
                    <Spin fix>
                      <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                      <div>Loading</div>
                    </Spin>
                  </i-col>
                </Row>
                <div v-else v-for="item in items" :key="item.id">
                  <Row>
                    <i-col span="2">
                      <Avatar src="https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png" style="width: 100%;height: 100%" />
                    </i-col>
                    <i-col span="5">
                      <div class="user-name">
                        {{item.username}}
                      </div>
                      <p style="margin-top: 5px"> 邮箱: {{ item.email || '暂无邮箱信息' }} </p>
                      <p> 所属组织: {{ item.institution || '暂无组织信息'}} </p>
                    </i-col>
                    <i-col offset="11" span="4">
                      <i-button type="primary" style="width: 100px; height: 35px; top: 31px; position: relative;" @click="jumpUserInfo(item.id)">
                        他的主页
                      </i-button>
                    </i-col>
                  </Row>
                  <Divider />
                </div>
              </template>
              <Row v-else-if="loading">
                <i-col class="demo-spin-col" offset="8" span="8">
                  <Spin fix>
                    <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                    <div>Loading</div>
                  </Spin>
                </i-col>
              </Row>
              <template v-else>
                <div style="text-align: center; font-size: 20px">
                  暂无相关搜索结果
                </div>
              </template>
            </TabPane>-->
            </Tabs>
        </Card>
    </i-col>
    <i-col offset="1" span="6">
    </i-col>
  </Row>
</template>

<script>
// import KnowledgeCard from '@/view/micro-knowledge/knowledge-card'
import PaperCard from '@/view/paper/paper-card'
import RpaperCard from '@/view/paper/rpaper-card'
import { getKnowledgePage, getTags } from '@/api/microknowledge'
import { getErrModalOptions, getLocalTime } from '@/libs/util.js'
import {getInterpretationPage, getPaperPage ,getUserPage}from '@/api/paper'
import Clipboard from 'clipboard';
export default {
  name: 'Search',
  components: { PaperCard, RpaperCard},

  data () {
    return {
      activeTab: 'recommend',
      knowledgeType: 'all',
      selectTagList: [],
      tagSearch: '',
      tagList: [],
      pageIndex: 1,
      hasNextPage: true,
      items: [],
      pageSize: 5,
      query: this.$route.params.query,
      searchInterpretation:true,
      searchuser: false,
      searchpaper: false,
      loading: true,
      tabName: 'Interpretation',
    }
  },

  watch: {
    '$route' (to, from) {
      this.query = this.$route.params.query
      this.pageIndex = 1
      this.items = []
      this.loadData()
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
      this.loading = true
      if(this.searchInterpretation===true){
      getInterpretationPage('get', {
        pid: this.pageIndex,
        num_per_page: this.pageSize,
        tags: this.tagSearch === '' ? null : this.tagSearch,
        keywords: this.$route.params.query,
      }).then(res => {
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
            isCollect: item.is_favor,
            likeNumber: item.like_num,
            commentNumber: item.commentNum,
            favorNumber: item.favor_num,
            source: item.source,
            citation: item.citation,
            kind: 1
          }
        })
        this.items.push(...mapData)
        this.loading = false
        this.hasNextPage = res.data.has_next
      }).catch(error => {
        console.log(error)
        this.$Modal.error(getErrModalOptions(error))
      })
      }else if(this.searchpaper===true){
       getPaperPage('get', {
        pindx: this.pageIndex,
        num_per_page: this.pageSize,
        tags: this.tagSearch === '' ? null : this.tagSearch,
        keywords: this.$route.params.query,
      }).then(res => {
        const mapData = res.data.page.map(item => {
          return {
          }
        })
        this.items.push(...mapData)
        this.loading = false
        this.hasNextPage = res.data.has_next
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
      }else{
        getUserPage('get', {
        page: this.pageIndex,
        page_size: this.pageSize,
        keywords: this.$route.params.query,
      }).then(res => {
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
      }
    },

    changeTab: function (name) {
      this.tabName = name;
      if (this.tabName === 'Interpretation') {
        this.searchInterpretation = true;
        this.searchpaper = false;
        this.searchuser = false;
      }else if(this.tabName === 'paper'){
        this.searchpaper =true;
        this.searchInterpretation = false;
        this.searchuser = false;
      }else{
        this.searchuser = true;
        this.searchInterpretation = false;
        this.searchpaper = false;
      }
       this.loadData()
    },

    jumpUserInfo: function (id) {
      this.$router.push({
        name: 'user_info',
        params: {
          id: id
        }
      })
    },

    loadMoreData: function () {
      this.pageIndex += 1
      this.loadData()
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
</style>
