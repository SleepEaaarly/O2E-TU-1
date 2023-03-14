<template>
  <div>
    <card :bordered="false" dis-hover :style="citeStyle">
      <template v-if="kind === 0">
        <Row>
          标题: <a :href='title'> {{title}} </a> ( {{ publishedYear }} ) 作者：{{ item.name }}
        </Row>
        <br>
      </template>
          <br>
          <i-col style="font-size: 18px">
            摘要: <a :href='item.source'> {{item.citation}} </a>
          </i-col> 
         <i-col style="font-size: 18px">
            正文：{{ item.content }}
          </i-col>
          <Divider />
      <Row>
        <Tag v-for="(tag, index) in tags" :key="index" class="sysTopics">{{ tag.name }}</Tag>
      </Row>
    </card>
    <Divider />
  </div>
</template>

<script>
export default {
  name: 'RpaperCard',
  components: {
  },
  props: {

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

    publishedYear: {
      type: Number,
      default: 0
    },

  },

  data () {
    return {
    }
  },

  computed: {
    likeColor: function () {
      return this.like ? '#0084ff' : '#747b8b'
    },

    collectType: function () {
      return this.collect ? 'ios-heart' : 'ios-heart-outline'
    },

    collectColor: function () {
      return this.collect ? '#fb7299' : 'default'
    },

    citeStyle: function () {
      return this.cite ? 'margin-left:100px;' : ''
    },

    citeMessage: function () {
      return this.cited ? '取消' : this.citeMessageInit
    },

    popId: function () {
      return 'pop' + this.$props.id
    }
  },

  methods: {

    showDetail: function () {
      if (this.evidences.length === 0) {
        microInterpretationIdReq(this.id, this.kind, 'get').then(res => {
          this.evidences = res.data.evidences
          this.detailController = true
        }).catch(error => {
          console.log(error)
        })
      } else {
        this.detailController = true
      }
    },
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
