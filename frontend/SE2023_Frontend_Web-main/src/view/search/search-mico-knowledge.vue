<template>
  <Row>
    <i-col
      offset="2"
      span="15"
    >
    <p class="type-selector"> 热搜:</p>
      <Card>
      </Card>
        
        <p class="type-selector">
           检索:
        </p>
        <i-col offset="0" style="width: 80%">
          <i-input placeholder="请输入...." v-model="searchText" type="text" style="width: 80%" suffix="ios-search" search @on-search="onSearch" />
          &nbsp;
        <br>
        <p class="type-selector">
          微知识类型：
        </p>
        <i-select
          v-model="knowledgeType"
          @on-change="selectType"
          style="width: 80%"
        >
          <Option value="all">
            全部
          </Option>
          <Option value="micro-evidence">
            微证据
          </Option>
          <Option value="micro-suppose">
            微猜想
          </Option>
        </i-select>
        <br>
        <br>
        <p class="type-selector">
          标签：
        </p>
        <i-select
          v-model="selectTagList"
          style="width: 80%"
          multiple
          @on-change="changeTag"
          filterable
        >
          <Option
            v-for="item in tagList"
            :value="item.value"
            :key="item.value"
          >
            {{ item.label }}
          </Option>
        </i-select>
        <br>
        <br>
        <i-button type="primary" @click="search">
            搜索
          </i-button>
        </i-col>
    </i-col>
  </Row>
</template>

<script>
import { getKnowledgePage, getTags } from '@/api/microknowledge'
import { getErrModalOptions, getLocalTime } from '@/libs/util.js'
export default {
  name: 'Search',
  components: { SearchrnakCard },

  data () {
    return {
      activeTab: 'recommend',
      knowledgeType: 'all',
      searchText:'',
      selectTagList: [],
      tagSearch: '',
      tagList: [],
      pageIndex: 1,
      hasNextPage: true,
      items: [],
      pageSize: 15,
      query: this.$route.params.query,
      searchEvidence: true,
      searchConjecture: true,
      loading: true
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
      getKnowledgePage('get', {
        pindx: this.pageIndex,
        num_per_page: this.pageSize,
        tags: this.tagSearch === '' ? null : this.tagSearch,
        keywords: this.$route.params.query,
        micro_evidence: this.searchEvidence,
        micro_conjecture: this.searchConjecture
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
            evidences: item.evidences,
            key: `${item.type}-${item.id}`
          }
        })
        this.items.push(...mapData)
        this.loading = false
        this.hasNextPage = res.data.has_next
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
    },

    selectType: function (value) {
      this.knowledgeType = value
      if (value === 'all') {
        this.searchEvidence = true
        this.searchConjecture = true
      } else if (value === 'micro-evidence') {
        this.searchEvidence = true
        this.searchConjecture = false
      } else {
        this.searchEvidence = false
        this.searchConjecture = true
      }
      // reset
      this.pageIndex = 1
      this.items = []
      this.loadData()
    },

    search () {
      if (this.searchText !== '') {
        this.$router.push({
          name: 'search',
          params: {
            query: this.searchText
          }
        })
      } else {
        this.$Message.info('请键入搜素关键词')
      }
    },

    onSearch (value) {
      this.searchText = value
      this.search()
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
      this.loadData()
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
