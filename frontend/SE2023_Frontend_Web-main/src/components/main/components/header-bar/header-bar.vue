<template>
  <div class="header-bar" :style ="backgroundDiv">
    <template>
      <Row>
        <i-col span="1">
          <sider-trigger :collapsed="collapsed" icon="md-menu" @on-change="handleCollpasedChange"></sider-trigger>
        </i-col>
        <i-col span="7">
          <custom-bread-crumb show-icon :list="breadCrumbList"></custom-bread-crumb>
        </i-col>

        <i-col offset="1" span="7">
          <i-input placeholder="请输入...." v-model="searchText" type="text" style="width: 60%" suffix="ios-search" search @on-search="onSearch" />
          &nbsp;
          <i-button type="primary" @click="search">
            搜索
          </i-button>
        </i-col>
        <i-col offset="6" span="2">
          <slot></slot>
        </i-col>
      </Row>
    </template>
  </div>
</template>
<script>
import siderTrigger from './sider-trigger'
import customBreadCrumb from './custom-bread-crumb'
import './header-bar.less'
export default {
  name: 'HeaderBar',
  components: {
    siderTrigger,
    customBreadCrumb
  },
  props: {
    collapsed: Boolean
  },
  data () {
    return {
       backgroundDiv: {
       // backgroundImage: "url(" + require("@/assets/images/a.png") + ")",
       backgroundRepeat: "repeat",
       backgroundSize: "auto 100%",
       },
      searchText: ''
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.name !== 'search') {
        this.searchText = ''
      }
    }
  },
  computed: {
    breadCrumbList () {
      return this.$store.state.app.breadCrumbList
    }
  },
  methods: {
    handleCollpasedChange (state) {
      this.$emit('on-coll-change', state)
    },

    selectMenu (name) {
      if (name === 'home') {
        this.$router.push({ name: 'home' })
      }
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
    }
  }
}
</script>
<style scoped>
.ivu-menu {
  display: inline;
}
.ivu-menu-item {
  font-size: 15px;
}
</style>
