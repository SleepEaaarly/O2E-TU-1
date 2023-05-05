<template>
  <a-card :bordered="false">
    <a-table :data-source="data" :columns="columns">
      <template slot="operation" slot-scope="text, record">
        <div>
          <span>
            <a @click="checkFeedback(record)" v-if="record.flag==0">回复</a>
            <a  v-else>已成功回复</a>
            <a-modal v-model="showDetail" title="回复反馈" @ok="handleOk()" width="750px">
              <a-card :bordered="false" dis-hover>
                <a-row>姓名：{{selectData.name}}</a-row>
                <br/>
                <a-row>性别：{{selectData.sex}}</a-row>
                <br/>
                <a-row>邮箱：{{selectData.email}}</a-row>
                <br/>
                <a-row>问题类型：{{selectData.qtype}}</a-row>
                <br/>
                <a-row>发布时间：{{selectData.datatime}}</a-row>
                <br/>
                <a-row>问题：{{selectData.description}}</a-row>
                <br/>
                <a-row>回答：</a-row>
                <br/>
                <a-textarea v-model="reply"></a-textarea>
              </a-card>
            </a-modal>
          </span>
        </div>
      </template>
      <template #expandedRowRender="record,index" class="ant-table-thead">
        <p style="margin: 0">
          {{ record.description }}
        </p>
        <br/>
        <div  v-if="record.flag">
          <p style="margin: 0">
            回复：
          </p>
          <br/>
          <p style="margin: 0">
            {{ record.message }}
          </p>
        </div>
        <div v-else>
          <p style="margin: 0">
            暂未回复
          </p>
        </div>
      </template>
    </a-table>
  </a-card>
</template>

<script>
import {getFeedbackAll, replyFeedback} from "../../services/feedback";

const columns = [
  {
    title: "姓名",
    dataIndex: "name",
    scopedSlots: { customRender: "name" },
    width: 100,

  },
  {
    title: "性别",
    dataIndex: "sex",
    scopedSlots: { customRender: "sex" },
    width: 100
  },
  {
    title: "邮箱",
    dataIndex: "email",
    scopedSlots: { customRender: "email" },
    width: 150
  },
  {
    title: "问题类型",
    dataIndex: "qtype",
    scopedSlots: { customRender: "qtype" },
    width: 150
  },
  {
    title: "发布时间",
    dataIndex: "datatime",
    scopedSlots: { customRender: "datatime" },
    width: 150
  },
  {
    title: "回复状态",
    dataIndex: "state",
    scopedSlots: { customRender: "state" },
    width: 150
  },
  {
    title: "操作",
    dataIndex: "operation",
    scopedSlots: { customRender: "operation" },
    width: 150,
    render: () => <a>反馈</a>,
  }
];
const data = [];

export default {
  name: "feedbackList",
  inject: ['reload'],
  components: {},
  data() {
    return {
      data,
      columns,
      showDetail: false,
      reply: '',
      selectData: {},
    }
  },
  mounted() {
    this.init();
  },

  methods: {
    init: async function() {
      this.loadNeed();
    },
    loadNeed: function () {
      data.length = 0;
      getFeedbackAll().then((res)=>{
        console.log(res);
        let d = res.data.data;
        console.log(d);
        for (let i = 0; i < d.length; i++) {
          if(d[i].qtype) {
            console.log(d[i].name + " OK!")
            console.log(typeof (d[i].qtype))
          } else {
            console.log(d[i].name + " ERROR!")
          }
          let str = d[i].qtype[0];
          for (let j = 1; j < d[i].qtype.length; j++) {
            str = str + ', ' + d[i].qtype[j];
          }
          let s = '';
          if (d[i].flag == 1) {
            s = '已回复'
          } else {
            s = '未回复'
          }
          // console.log(d[i].name)
          // console.log(str)
          // console.log(d[i].qtype)
          // console.log(typeof(d[i].qtype))
          data.push({
            feedback_id: d[i].feedback_id,
            user_id: d[i].user_id,
            name: d[i].name,
            email: d[i].email,
            sex: d[i].sex,
            qtype: str,
            description: d[i].description,
            datatime: d[i].datatime,
            flag: d[i].flag,
            message: d[i].message,
            state: s
          })
        }
      }).catch((error) => {
        console.log(error);
      })
    },
    handleOk() {
      console.log(this.selectData)
      this.showDetail = false;
      let params = {
        feedback_id: this.selectData.feedback_id,
        message: this.reply
      }
      console.log(params)
      replyFeedback(params, 'post').then((res) => {
        console.log("答复成功！")
      }).catch((error) => {
        console.log(error)
      })
      this.reload();
    },
    checkFeedback(record) {
      console.log(record)
      console.log(record.name)
      this.showDetail = true;
      this.selectData = record;
    },
  }
}
</script>

<style scoped>
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
.editable-row-operations a {
  margin-right: 8px;
}
</style>
