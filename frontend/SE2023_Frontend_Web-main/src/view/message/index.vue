<template>
  <Card shadow>
    <div>
      <div class="message-page-con message-category-con">
        <Menu width="auto" active-name="unread" @on-select="handleSelect">
          <MenuItem name="unread">
          <span class="category-title">未读消息</span>
          <Badge style="margin-left: 10px" :count="unreadCount"></Badge>
          </MenuItem>
          <MenuItem name="readed">
          <span class="category-title">全部消息</span>
          <Badge style="margin-left: 10px" class-name="gray-dadge"></Badge>
          </MenuItem>
        </Menu>
      </div>
      <div class="message-page-con message-list-con">
        <Spin fix v-if="listLoading" size="large"></Spin>
        <Menu width="auto" active-name="" :class="titleClass" @on-select="handleView">
          <Scroll height="450">
            <MenuItem v-for="(item,index) in messageList" :name="item.msg_id" :key="index">
            <div>
              <p class="msg-title">{{ item.title }}</p>
              <Badge status="default" :text="item.create_time" />
              <!-- <Button style="float: right;margin-right: 20px;" :style="{ display: item.loading ? 'inline-block !important' : '' }" :loading="item.loading" size="small" :icon="currentMessageType === 'readed' ? 'md-trash' : 'md-redo'" :title="currentMessageType === 'readed' ? '删除' : '还原'" type="text" v-show="currentMessageType !== 'unread'" @click.native.stop="removeMsg(item)"></Button> -->
            </div>
            </MenuItem>
          </Scroll>
          <Row v-if="hasNext">
            <i-col style="text-align: center">
              <a @click.prevent="loadMore"> 加载更多 </a>
            </i-col>
          </Row>
          <Divider v-else>暂无更多</Divider>
        </Menu>
      </div>
      <div class="message-page-con message-view-con">
        <Spin fix v-if="contentLoading" size="large"></Spin>
        <div class="message-view-header">
          <h2 class="message-view-title">{{ showingMsgItem.title }}</h2>
          <time class="message-view-time">{{ showingMsgItem.create_time }}</time>
        </div>
        <div v-html='messageContent'></div>
      </div>
    </div>
  </Card>
</template>

<script>
import { getMessages, getUserInfo } from '@/api/user'
const listDic = {
  unread: 'messageUnreadList',
  readed: 'messageReadedList',
  trash: 'messageTrashList'
}
export default {
  name: 'message_page',
  data () {
    return {
      psize: 10,
      pindex: 1,
      listLoading: false,
      contentLoading: false,
      currentMessageType: 'unread',
      messageContent: '',
      showingMsgItem: {},
      unReadHasNext: true,
      readedHasNext: true,
      readedSet: new Set(),
      messageUnreadList: [],
      messageReadedList: []
    }
  },
  computed: {
    messageList () {
      return this[listDic[this.currentMessageType]]
    },
    titleClass () {
      return {
        'not-unread-list': this.currentMessageType !== 'unread'
      }
    },
    hasNext () {
      return this.currentMessageType !== 'unread' ? this.readedHasNext : this.unReadHasNext
    },
    unreadCount () {
      return this.$store.state.user.unreadCount
    },
    only_unread () {
      return this.currentMessageType === 'unread'
    }
  },
  methods: {
    stopLoading (name) {
      this[name] = false
    },
    handleSelect (name) {
      this.currentMessageType = name
    },
    async handleView (msg_id) {
      if (!this.readedSet.has(msg_id) && this.currentMessageType === 'unread') {
        this.readedSet.add(msg_id)
        this.$store.commit('setMessageCount', this.$store.state.user.unreadCount - 1)
      }
      this.contentLoading = true
      this.messageContent = await this.convertContent(this.messageList[msg_id])
      this.contentLoading = false
    },
    removeMsg (item) {
      // item.loading = true
      // const msg_id = item.msg_id
      // if (this.currentMessageType === 'readed') this.removeReaded({ msg_id })
      // else this.restoreTrash({ msg_id })
    },
    convertTitle (content) {
      console.log(content)
      if (content.search(/favored/) >= 0) {
        return '收藏了你的解读！'
      } else if (content.search(/Liked/) >= 0) {
        return '点赞了你的解读!'
      } else if (content.search(/fan/) >= 0) {
        return '关注了你!'
      } else if (content.search(/reply/) >= 0){
        return '回复了你！'
      }else if (content.search(/Created/) >= 0){
        return '创建了一个解读！'
      }else{
        return '提醒了你'
      }
    },
    async convertContent (msg) {
      console.log(msg)
      let name = ''
      await getUserInfo(msg.to_user
      ).then(res => {
        name = res.data.nickname === '' ? res.data.username : res.data.nickname
      }).catch(err => {
        console.log(err)
      })
      return `<a href='/user/user-info/${msg.to_user}'>${name}</a><p>${this.convertTitle(msg.content)}</p>`
    },
    convertTo (arr) {
      return arr.map((x, index) => ({
        title: '有一位用户' + this.convertTitle(x.content),
        creat_time: x.created_at,
        to_user: parseInt(x.to_user),
        content: x.content,
        msg_id: index,
        loading: false
      }))
    },
    async loadMore () {
      if (!this.only_unread) {
        this.pindex += 1
      }
      let has_next = true
      return getMessages({
        pindex: this.only_unread ? 1 : this.pindex,
        num_per_page: this.psize,
        only_unread: this.only_unread
      }).then(res => {
      
        const unread = this.convertTo(res.data.page)
        this.messageList.push(...unread.sort((a, b) => new Date(b.create_time) - new Date(a.create_time)))
        has_next = res.data.has_next
        if (this.only_unread) {
          this.unReadHasNext = has_next
        } else {
          this.readedHasNext = has_next
        }
      }).catch(err => {
        console.log(err)
      })
    }
  },
  mounted () {
    getMessages({
      pindex: this.pindex,
      num_per_page: this.psize,
      only_unread: true
    }).then(res => {
      console.log(res)
      this.unReadHasNext = res.data.has_next
      const unread = this.convertTo(res.data.page)
      this.messageUnreadList.push(...unread.sort((a, b) => new Date(b.create_time) - new Date(a.create_time)))
    }).catch(err => {
      console.log(err)
    })
    getMessages({
      pindex: this.pindex,
      num_per_page: this.psize
    }).then(res => {
      this.readedHasNext = res.data.has_next
      const readed = this.convertTo(res.data.page)
      this.messageReadedList.push(...readed.sort((a, b) => new Date(b.create_time) - new Date(a.create_time)))
    }).catch(err => {
      console.log(err)
    })
  }
}
</script>

<style lang="less">
.message-page {
  &-con {
    height: ~"calc(100vh - 176px)";
    display: inline-block;
    vertical-align: top;
    position: relative;
    &.message-category-con {
      border-right: 1px solid #e6e6e6;
      width: 200px;
    }
    &.message-list-con {
      border-right: 1px solid #e6e6e6;
      width: 230px;
    }
    &.message-view-con {
      position: absolute;
      left: 446px;
      top: 16px;
      right: 16px;
      bottom: 16px;
      overflow: auto;
      padding: 12px 20px 0;
      .message-view-header {
        margin-bottom: 20px;
        .message-view-title {
          display: inline-block;
        }
        .message-view-time {
          margin-left: 20px;
        }
      }
    }
    .category-title {
      display: inline-block;
      width: 65px;
    }
    .gray-dadge {
      background: gainsboro;
    }
    .not-unread-list {
      .msg-title {
        color: rgb(170, 169, 169);
      }
      .ivu-menu-item {
        .ivu-btn.ivu-btn-text.ivu-btn-small.ivu-btn-icon-only {
          display: none;
        }
        &:hover {
          .ivu-btn.ivu-btn-text.ivu-btn-small.ivu-btn-icon-only {
            display: inline-block;
          }
        }
      }
    }
  }
}
</style>
