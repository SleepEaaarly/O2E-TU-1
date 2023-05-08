<template>
  <div>
    <slot name="userType"></slot>
    <a @click.prevent="showUser">{{ creator['username'] === '' ? '未知用户' : creator['username']}}</a>
    <Modal v-model="showUserControl" footer-hide>
      <Row>
        <i-col span="4">
          <Avatar src="" style="width: 100%;height: 100%" />
        </i-col>
        <i-col span="10">
          <div class="user-name">
            {{ userInfo.nickname===''?userInfo.username:userInfo.nickname }}
          </div>
          <p style="margin-top: 5px"> 邮箱: {{ userInfo.email || '暂无邮箱信息' }} </p>
          <p> 所属组织: {{ userInfo.institution || '暂无组织信息'}} </p>
        </i-col>
      </Row>
      <Divider />
      <Row>
        <i-col span="8" style="text-align: center; font-size: 18px">
          <p class="data-title"> 总发布数 </p>
          <p> {{ userInfo.total_post }} </p>
        </i-col>
        <i-col span="8" style="text-align: center; font-size: 18px">
          <p class="data-title"> 总粉丝数 </p>
          <p> {{ userInfo.total_fan }} </p>
        </i-col>
        <i-col span="8" style="text-align: center; font-size: 18px">
          <p class="data-title"> 总点赞数 </p>
          <p> {{ userInfo.total_like }} </p>
        </i-col>
      </Row>
      <Divider />
      <Row>
        <i-col span="7" offset="4">
          <i-button v-if="!userInfo.is_following" style="width: 100%" @click="handleFollow">
            关注
          </i-button>
          <i-button v-else style="width: 100%" type="primary" @click="handleFollow">
            取消关注
          </i-button>
        </i-col>
        <i-col span="7" offset="2">
          <i-button type="primary" style="width: 100%" @click="jumpUserInfo">
            他的主页
          </i-button>
        </i-col>
      </Row>
    </Modal>
  </div>
</template>

<script>
import { follow, unfollow, getUserInfo } from '@/api/user'
export default {
  name: 'User',

  props: {
    creator: {
      type: Object,
      default: () => ({
        username: 'xx',
        id: '0'
      })
    }

  },

  data () {
    return {
      userInfo: {
        nickname: ''
      },
      showUserControl: false
    }
  },

  mounted () {
    getUserInfo(this.$props.creator.id).then(res => {
      this.userInfo = res.data
    }).catch(error => {
      console.log(error)
    })
  },

  methods: {
    showUser: function () {
      getUserInfo(this.$props.creator.id).then(res => {
        this.showUserControl = true
        this.userInfo = res.data
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
    },

    handleFollow: function () {
      if (this.userInfo.is_following) {
        unfollow(this.creator.id).then(res => {
          this.userInfo.is_following = false
          this.userInfo.total_fan -= 1
          this.$Message.info('成功取消关注')
        }).catch(error => {
          this.$Modal.error(getErrModalOptions(error))
        })
      } else {
        follow(this.creator.id).then(res => {
          this.userInfo.is_following = true
          this.userInfo.total_fan += 1
          this.$Message.info('成功关注')
        }).catch(error => {
          this.$Modal.error(getErrModalOptions(error))
        })
      }
    },

    jumpUserInfo: function () {
      this.$router.push({
        name: 'user_info',
        params: {
          id: this.userInfo.id
        }
      })
    }
  }

}
</script>
