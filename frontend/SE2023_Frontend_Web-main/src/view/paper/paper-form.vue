<template>
  <div>
  <Form ref="form" :model="form" :rules="ruleCustom" :label-width="120">
    <Form-item label="解读文献对象" prop="citation"><Input type="text" v-model="form.citation" placeholder='请输入解读文献(GB7714格式)' /></Form-item>
    <Form-item label="解读文献链接" prop="citationUrl"><Input type="url" placeholder='请输入解读文献链接' v-model="form.citationUrl" /></Form-item>
    <Form-item label="解读文献年份" prop="year">
      <Input-number v-model="form.year"/>
    </Form-item>
    <Form-item label="标签" prop="tags"><Input type="text" placeholder='请输入至少三个标签(以空格分隔)' v-model.trim="form.tags" /></Form-item>
    <Form-item label="标题" prop="title"><Input type="text" placeholder='请输入标题' v-model="form.title" /></Form-item>
     <Form-item label="论文解读" v-show="true" prop="paper">
      <editor v-model="form.paper" pasteFilter="true"></editor>
     </Form-item>
    <Button type="primary" @click="handleSubmit('form')" long>发布</Button>
    </Form>
  </div>
</template>
<script>
import { getErrModalOptions } from '@/libs/util.js'
import editor from '@/components/editor/editor.vue'
import Editor from '../../components/editor/editor.vue'
import { createPaper, getTags } from '@/api/paper.js'
//import { createEvidence, getTags } from '@/api/microknowledge.js'
export default {
  components: {
    editor,
    Editor
  },
  data () {
    const validateCitation = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入解读对象'))
      } else {
        callback()
      }
    }
    
    const validatePaper = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入论文解读'))
      }  else {
        callback()
      }
    }
    
    const validateTitle = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入标题'))
      }  else {
        callback()
      }
    }
  
   const validateYear = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入！'))
        
      }  
      else if(value<0){
        callback(new Error('年份不能为负数'))
      }else {
        callback()
      }
    }

    const validateUrl = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入链接'))
      } else if (!value.match(/^((ht|f)tps?):\/\/[\w-]+(\.[\w-]+)+([\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])?$/)) {
        callback(new Error('文献链接不正确'))
      } else {
        callback()
      }
    }

    const validateTags = (rule, value, callback) => {
      if (value === '' || value.split(/\s+/).length < 3) {
        callback(new Error('请输入至少3个标签(以空格分隔)'))
      } else {
       var m = value.split(/\s+/).map(el => el.trim()).filter(item => item.trim() != '')
           for (var i=0; i<m.length; i++) {
            for (var j=i+1; j<m.length; j++) {
               if (m[i] == m[j]) {
                callback(new Error('输入了重复的标签请检查'))
             }
           }
        }
        callback()
      }
    }

    const validateNotNull = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入！'))
      } else {
        callback()
      }
    }

    const validateArrayNotEmpty = (rule, value, callback) => {
      if (value.length === 0) {
      // callback(new Error('请选择主题'))
        callback()
      } else {
        callback()
      }
    }

    return {
      topicList: [
      ],
      form: {
        topic: [],
        paper: '',
        tags: '',
        year: null,
        citationUrl: '',
        title:'',
        citation: ''
      },
      ruleCustom: {
        citation: [
          {
            required: true,
            validator: validateCitation,
            trigger: 'blur'
          }
        ],
        citationUrl: [{
          required: true,
          validator: validateUrl,
          trigger: 'blur'
        }],
        topic: [
          {
            required: true,
            validator: validateArrayNotEmpty,
            trigger: 'blur'
          }
        ],
        paper: [
          {
            required: true,
            validator: validatePaper,
            trigger: 'blur'
          }
        ],
        year: [{
          required: true,
          validator: validateYear,
          trigger: 'blur'
        }],
        tags: [
          {
            required: true,
            validator: validateTags,
            trigger: 'blur'
          }
        ],
        title: [
          {
            required: true,
            validator: validateTitle,
            trigger: 'blur'
        }
        ]
      }
    }
  },
  mounted () {
    this.getTopicList()
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          const tags = this.form.topic.map(tag => { return { name: tag, type: 0 } }).concat(this.form.tags.split(/\s+/).map(tag => { return { name: tag, type: 1 } }))
          const data = {
            content: this.form.paper,
            tags: tags,
            citation: this.form.citation,
            source: this.form.citationUrl,
            title: this.form.title,
            published_year: this.form.year
          }
          createPaper('post', data).then(res => {
            this.$Message.success('发布成功!')
            this.$router.push({
             name: 'home',
            })
          }).catch(
            this.$Modal.error(getErrModalOptions(err))
          )
        } else {
          this.$Message.error('发布失败!')
        }
      })
      
    },
    getTopicList () {
      getTags('get', {
        pindx: 1,
        num_per_page: 99,
        presupposed: true
      }).then(res => {
        this.topicList = res.data.page.map(tag => ({ value: tag.name, label: tag.name }))
      }).catch(err => {
        console.log(err)
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
  }
}
</script>

<style>
form {
  margin-right: 200px;
}
</style>
