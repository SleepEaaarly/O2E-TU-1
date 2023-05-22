<template>
  <div>
    <div class="row" >
    <card :bordered="false" dis-hover :style="citeStyle">
      <div :id="paperId">
      <div slot="title">
        发布者:
        <a @click.prevent="showUser" :id="id">{{ creator['username'] === '' ? '未知用户' : creator['username']}}</a>
        <Modal v-model="showUserControl" footer-hide>
          <Row>
            <i-col span="4">
              <Avatar :src="userpic" style="width: 100%;height: 100%" />
            </i-col>
            <i-col span="10">
              <div class="user-name">
                {{ userInfo.username }}
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
              <i-button v-if="!userInfo.is_following&&this.$store.state.user.userId!=userInfo.id" style="width: 100%" @click="handleFollow">
                关注
              </i-button>
              <i-button v-else-if="this.$store.state.user.userId!=userInfo.id" style="width: 100%" type="primary" @click="handleFollow">
                取消关注
              </i-button>
            </i-col>
            <i-col span="7" offset="2">
              <i-button v-if="this.$store.state.user.userId!=userInfo.id" style="width: 100%" @click="jumpUserInfo(userInfo.id)">
                他的主页
              </i-button>
            </i-col>
          </Row>
        </Modal>
      </div>
      <p slot="extra">{{ kind === 1 ? '论文解读' : '批注' }}发布于: {{ createAt }}</p>
        <Row>
          解读对象: <a :href='source'> {{citation}} </a>-------{{publishedYear}}年
        </Row>
        <Row>
          标题: {{title}}
        </Row>
        <br>
        <br>
        <br>
        <editor v-html="content"></editor>
      <br />
      <Row>
        <Tag v-for="(tag, index) in tags" :key="index" class="sysTopics">{{ tag.name }}</Tag>
      </Row>
      </div>
      <br />
      <template v-if="displayType === 0">
        <Row>
          <i-col span="12">
            <ButtonGroup>
              <i-button @click="onLike" style="font-size: 14px">
                <Icon type="md-thumbs-up" :color="likeColor" />
                点赞 {{ totalLike }}
              </i-button>
              <i-button @click="onCollect" style="font-size: 14px">
                <Icon :type="collectType" :color="collectColor" />
                收藏 {{ totalFavor }}
              </i-button>
              <i-button @click="onComment" style="font-size: 14px">
                <Icon type="ios-chatbubbles" />
                评论 {{ totalcomment}}
              </i-button>
              <br/>
                <i-button  @click="onOut" style="font-size: 14px">
                   <Icon type="ios-cloud-download" />
                   导出解读对象
                 </i-button>
           <Poptip confirm title="确定导出？" @on-ok="getPdf();onOut4()" @on-cancel="onOut4()" >
                <i-button  @click="onOut3()" style="font-size: 14px">
                 <Icon type="ios-cloud-download" />
                 导出解读
                </i-button>
               </Poptip>
              <!--<i-button  @click="download()" style="font-size: 14px">
                 <Icon type="ios-cloud-download" />
                 导出解读
                </i-button>-->
            </ButtonGroup>
          </i-col>
        </Row>
        <Card v-if='showComment' style="margin-top: 10px;">
          <comment v-bind='comments'></comment>
        </Card>
      </template>
      <template v-else-if="displayType === 1">
        <Button class="cite" @click="onCite" type="primary">{{citeMessage}}</Button>
      </template>
    </card>
    </div>
    <Divider />
  </div>
</template>

<script>
import { collectInterpretation, likeInterpretation, InterpretationIdReq, getInterpretationComments } from '@/api/paper.js'
import { follow, unfollow, getUserInfo } from '@/api/user'
import { getErrModalOptions, getLocalTime } from '@/libs/util'
import editor from '@/components/editor/editor.vue'
import Editor from '../../components/editor/editor.vue'
import comment from '@/components/comment/comment.vue'
import {saveAS} from 'file-saver'
export default {
  name: 'PaperCard',
  components: {
    comment,
    editor,
    Editor
  },
  props: {
    id: {
      type: Number,
      default: 0
    },

    creator: {
      type: Object,
      default: () => {
        return {
          username: 'xx',
          id: '0'
        }
      }
    },

    title: {
      type: String,
      default: '引用'
    },

    kind: {
      type: Number,
      default: 0
    },

    citeMessageInit: {
      type: String,
      default: '引用'
    },

    createAt: {
      type: String,
      default: '年/月/日'
    },

    content: {
      type: String,
      default: '这是一个展示示例'
    },

    tags: {
      type: Array,
      default: () => {
        return []
      }
    },

    isLike: {
      type: Boolean,
      default: false
    },

    isCollect: {
      type: Boolean,
      default: false
    },

    likeNumber: {
      type: Number,
      default: 0
    },

    commentNumber: {
      type: Number,
      default: 0
    },

    favorNumber: {
      type: Number,
      default: 0
    },

    displayType: {
      type: Number,
      default: 0
    },

    source: {
      type: String,
      default: 'qq'
    },

    citation: {
      type: String,
      default: 'ss'
    },

    publishedYear: {
      type: Number,
      default: 0
    },

    interpretations: {
      type: Array,
      default: () => {
        return []
      }
    },
    userpic: {
      type: String,
      default: 'http://116.63.14.146:8000/api/images/default_user_icon.jpg'
    }
  },

  data () {
    return {
      like: this.$props.isLike,
      totalLike: this.$props.likeNumber,
      totalcomment: this.$props.commentNumber,
      totalFavor: this.$props.favorNumber,
      collect: this.$props.isCollect,
      cited: false,
      showComment: false,
      comments: [],
      detailController: false,
      showUserControl: false,
      userInfo: {},
      htmlTitle: this.title,
      followText: '',
      paperid: '1'
    }
  },

  computed: {
    likeColor: function () {
      return this.like ? '#0084ff' : '#747b8b'
    },

    paperId: function () {
      return this.paperid
    },

    collectType: function () {
      return this.collect ? 'ios-heart' : 'ios-heart-outline'
    },

    collectColor: function () {
      return this.collect ? '#fb7299' : 'default'
    },

    citeStyle: function () {
      let style = ''
      style += this.cite ? 'margin-left:100px;' : ''
      style += ' word-break: break-all'
      return style
    },

    citeMessage: function () {
      return this.cited ? '取消' : this.citeMessageInit
    },

    popId: function () {
      return 'pop' + this.$props.id
    },

    word: function () {
      return 'word-break: break-all'
    }

  },

  methods: {
    ToText (HTML) {
      var input = HTML
      return input.replace(/<(style|script|iframe)[^>]*?>[\s\S]+?<\/\1\s*>/gi, '').replace(/<[^>]+?>/g, '').replace(/\s+/g, ' ').replace(/ /g, ' ').replace(/>/g, ' ')
    },

    onLike: function () {
      this.like = !this.like
      if (this.like) {
        this.totalLike += 1
      } else {
        this.totalLike -= 1
      }
      likeInterpretation('post', this.$props.id).then(res => {
        const info = this.like ? '成功点赞' : '成功取消点赞'
        this.$Message.info(info)
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
    },

    download: function () {
      let a = document.createElement('a')
      a.href = `/api/download/Interpretation/${this.id}`
      a.setAttribute('download', this.title)
      a.click()
    },

    onOut: function () {
      console.log("enter onOut")
      console.log(this.citation)
      console.log(this.source)
      let str = new Blob([this.citation + '  ' + this.source], { type: 'text/plain;charset=utf-8' })
      console.log(str)
      saveAs(str, `解读对象.txt`)
    },

    onOut3: function () {
      this.paperid = 'pdfDom'
      console.log('1')
    },

    onOut4: function () {
      this.paperid = '1'
      console.log('2')
    },

    onCollect: function () {
      this.collect = !this.collect
      if (this.collect) {
        this.totalFavor += 1
      } else {
        this.totalFavor -= 1
      }
      collectInterpretation('post', this.$props.id, this.collect ? 'favor' : 'unfavor').then(res => {
        const info = this.collect ? '成功收藏' : '成功取消收藏'
        this.$Message.info(info)
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
    },

    onComment: async function () {
      await this.getComments()
      this.showComment = !this.showComment
    },

    onCite: function () {
      this.cited = !this.cited
      this.$emit('cite-event', { id: this.id, content: this.content, cited: this.cited })
    },

    showDetail: function () {
      if (this.evidences.length === 0) {
        InterpretationIdReq(this.id, this.kind, 'get').then(res => {
          this.evidences = res.data.evidences
          this.detailController = true
        }).catch(error => {
          console.log(error)
        })
      } else {
        this.detailController = true
      }
    },

    convertComments: function (comments) {
      console.log(comments)
      comments = comments.map(x => ({
        commentId: x.id,
        name: x.username,
        time: getLocalTime(x.created_at),
        id: x.user_id,
        comment: x.text,
        to: x.to_user ? x.to_user.username : 0,
        toId: x.to_user ? x.to_user.id : '',
        inputShow: false,
        headImg: 'http://116.63.14.146:8000/api/' + x.userpic,
        parent_comment_id: x.parent_comment_id,
        reply: []
      }))
      let father_comments_map = {}
      comments.filter(x => (x.parent_comment_id === undefined)).forEach(x => {
        father_comments_map[x.commentId] = x
      })
      comments.forEach(x => {
        if (x.parent_comment_id !== undefined) {
          father_comments_map[x.parent_comment_id].reply.push(x)
        }
      })
      return Object.values(father_comments_map)
    },

    getComments: async function () {
      let username = ''
      let userid = ''
      let userpic = ''
      await getUserInfo().then(res => {
        userid = res.data.id
        username = res.data.username
        userpic = 'http://116.63.14.146:8000/api/' + res.data.userpic
      }).catch(error => {
        this.$Modal.error(getErrModalOptions(error))
      })
      let header = {
        myName: username,
        interpretation_id: this.id,
        myHeader: userpic,
        myId: userid
      }
      await getInterpretationComments('get', {
        interpretation_id: this.id,
        pindex: 1,
        psize: 20
      }).then(res => {
        this.comments = { ...header, comments_init: this.convertComments(res.data.comment_list) }
        console.log(this.comments)
      }).catch(err => {
        console.log(err)
        this.comments = header
      })
    },

    showUser: function () {
      getUserInfo(this.$props.creator.id).then(res => {
        this.showUserControl = true
        this.userInfo = res.data
        this.userpic = 'http://116.63.14.146:8000/api/' + res.data.userpic
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

    jumpUserInfo: function (id) {
      this.$router.push({
        name: 'user_info',
        params: {
          id: id
        }
      })
    },

    getTime: function (time) {
      return getLocalTime(time)
    }
  }
}
</script>

<style>
.user-name {
  font-size: 26px;
  color: #4d4d4d;
}
.data-title {
  font-size: 18px;
  font-weight: bold;
}
</style>
