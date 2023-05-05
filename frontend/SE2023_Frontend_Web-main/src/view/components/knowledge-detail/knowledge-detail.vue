<template>
  <div>
    <card :bordered="false" dis-hover style="margin: 0 auto;width: 80%;">
      <p slot="title">
        发布者:
        <a href="">{{ creator.username }}</a>
      </p>
      <p slot="extra">{{ kind === 0 ? '微证据' : '微猜想' }}发布于: {{ createAt }}</p>
      <Row>{{ content }}</Row>
      <br />
      <template v-if="kind === 0">
        <Row>
          参考文献: <a :href='source'> {{citation}} </a> ( {{ publishedYear }} )
        </Row>
        <br>
      </template>
      <template v-if="showButtons">
        <Row>
          <i-col span="7">
            <ButtonGroup>
              <i-button :type="likeType" @click="onLike" style="font-size: 14px">
                <Icon type="md-arrow-dropup" />
                点赞
              </i-button>
              <i-button @click="onCollect" style="font-size: 14px">
                <Icon :type="collectType" />
                收藏
              </i-button>
              <i-button @click="onComment" style="font-size: 14px">
                <Icon type="ios-chatbubbles" />
                评论
              </i-button>
            </ButtonGroup>
          </i-col>
        </Row>
      </template>
      <Row>
        <Tag v-for="(tag,index) in topics" :key="index" type='border' color='blue' class="tag">{{ tag }}</Tag>
      </Row>
      <Row>
        <Tag v-for="(tag,index) in tags" :key="index" class="topic">{{ tag.name }}</Tag>
      </Row>
    </card>
    <template v-if="kind!=0">
      <div>
        <Row style='text-align: center;font-size: 20px;color: #00B7EE;'>参考</Row>
        <Row>
          <Col v-for='(post,index) in evidences' :key="index" span="9" offset='2'>
          <KnowledgeDetail v-bind='post'></KnowledgeDetail>
          </Col>
        </Row>
      </div>
    </template>

  </div>
</template>

<script>
export default {
  name: 'KnowledgeDetail',

  props: {
    id: {
      type: Number,
      default: 0
    },
    showButtons: {
      type: Boolean,
      default: false
    },
    creator: {
      type: Object,
      default: () => ({})
    },

    kind: {
      type: Number,
      default: 0
    },

    createAt: {
      type: String,
      default: '年/月/日'
    },

    content: {
      type: String,
      default: '这是一个展示示例'
    },
    evidences: {
      type: Array,
      default: () => {
        return []
      }
    },
    tags: {
      type: Array,
      default: () => {
        return []
      }
    },
    topics: {
      type: Array,
      default: () => {
        return []
      }
    },
    publishedYear: {
      type: Number,
      default: 1999
    },
    source: {
      type: String,
      default: ''
    },
    citation: {
      type: String,
      default: ''
    },

    isLike: {
      type: Boolean,
      default: false
    },

    isCollect: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      like: this.$props.isLike,
      collect: this.$props.isCollect
    }
  },

  computed: {
    likeType: function () {
      return this.like ? 'info' : 'default'
    },

    collectType: function () {
      return this.collect ? 'ios-heart' : 'ios-heart-outline'
    }
  },

  methods: {
    onLike: function () {
      this.like = ~this.like
    },

    onCollect: function () {
      this.collect = ~this.collect
    },

    onComment: function () {
      this.$Message.info('你点击了评论')
    }
  }
}
</script>

<style>
.citation {
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  text-align: left;
  color: #0bbdd1;
}
.source {
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  text-align: left;
  color: #0bbdd1;
}
.citeEvidence {
  display: inline-block;
  width: 500px;
}
Tag {
  color: #3f51b5;
}
</style>
