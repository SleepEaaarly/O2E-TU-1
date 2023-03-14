<template>
  <a-card :bordered="false">
    <h2>选择用户类型</h2>
    <a-space>
      <a-select
          ref="select"
          v-model:value="selectedType"
          style="width: 120px"
          @change="selectChange"
          :disabled="!changeable"
      >
        <a-select-option value="0">普通用户</a-select-option>
        <a-select-option value="1">专家认证中</a-select-option>
        <a-select-option value="2">企业认证中</a-select-option>
        <a-select-option value="3">封禁中</a-select-option>
        <a-select-option value="4">认证专家</a-select-option>
        <a-select-option value="5">认证企业</a-select-option>
        <a-select-option value="6">全部</a-select-option>
      </a-select>
    </a-space>
    <br/>
    <br/>
    <a-table :data-source="data" :columns="columns" :pagination="pagination" :key="itemKey">
      <template
        v-for="col in ['name', 'ins', 'email', 'type']"
        :slot="col"
        slot-scope="text, record"
      >
        <div :key="col">
          <a-input
            v-if="record.editable"
            style="margin: -5px 0"
            :value="text"
            @change="(e) => handleChange(e.target.value, record, col)"
          />
          <template v-else>
            {{ text }}
          </template>
        </div>
      </template>
      <template slot="operation" slot-scope="text, record">
        <div class="editable-row-operations">
          <span v-if="record.editable">
            <a-space>
              <a @click="() => save(record.key)">Save</a>
              <a-popconfirm
                title="Sure to cancel?"
                @confirm="() => cancel(record.key)"
              >
                <a>Cancel</a>
              </a-popconfirm>
            </a-space>
          </span>
          <span v-else>
            <a :disabled="editingKey !== ''" @click="() => edit(record.key)"
              >Edit</a
            >
          </span>
        </div>
        <a-popconfirm
          v-if="data.length"
          title="Sure to delete?"
          @confirm="() => onDelete(record.key)"
        >
          <a href="javascript:0;">Delete</a>
        </a-popconfirm>
      </template>
    </a-table>


  </a-card>
</template>

<script>
import { getUserAll,UserDel,UserModify, getSelectUser} from "../../../services/dataSource";
const columns = [
  {
    title: "用户名",
    dataIndex: "name",
    width: "20%",
    scopedSlots: { customRender: "name" },
  },
  {
    title: "所属机构",
    dataIndex: "ins",
    width: "25%",
    scopedSlots: { customRender: "ins" },
  },
  {
    title: "邮箱",
    dataIndex: "email",
    width: "20%",
    scopedSlots: { customRender: "email" },
  },
  {
    title: "用户类型",
    dataIndex: "type",
    width: "15%",
    scopedSlots: { customRender: "type" },
    // onFilter: (value, record) => record.type.indexOf(value) === 0,
  },
  {
    title: "操作",
    dataIndex: "operation",
    scopedSlots: { customRender: "operation" },
  },
];
const data = [];

export default {
  name: "UserForm",
  inject: ['reload'],
  i18n: require("./i18n-user"),
  data() {
    this.cacheData = data.map((item) => ({ ...item }));
    return {
      type:"",
      type1:0,
      data,
      columns,
      editingKey: "",
      editData: {},
      changeable: true,
      selectedType: "全部",
      pagination: {
        current: 1,
        onChange: (page) => {
          if (!this.changeable) {
            alert("请完成修改后再切换页面！")
            return
          }
          this.$forceUpdate()
          console.log(page);
          console.log(this.selectedType);
          getSelectUser(this.selectedType === "全部" ? 6 : this.selectedType, page).then((oriRes) => {
            console.log(oriRes);
            let res = oriRes.data;
            data.length = 0;
            for (let i = 0; i < res.data.length; i++) {
              if (res.data[i].type==0) {
                this.type="普通用户"
              } else if (res.data[i].type==1){
                this.type="专家认证中"
              } else if (res.data[i].type==2){
                this.type="企业认证中"
              }else if (res.data[i].type==3){
                this.type="封禁中"
              }else if (res.data[i].type==4){
                this.type="认证专家"
              }else if (res.data[i].type==5){
                this.type="认证企业"
              }
              data.push({
                key: res.data[i].id,
                name: res.data[i].username,
                ins: res.data[i].institution,
                type: this.type,
                email: res.data[i].email,
                editable: false
              });
            }
            this.cacheData = data.map((item) => ({ ...item }));
            this.totalCnt = res.data.total_count;
            this.loading = false;
            // this.itemKey = Math.random();
            this.pagination.current = page;
          }).catch((error) => {
            console.log(error);
          });
        },
        total: 10
      },
      itemKey: "",
    };
  },
  // computed: {
  //   dataColumns() {
  //     return this.columns.map(column => {
  //       column.title = this.$t('table.' + column.key)
  //       return column
  //     })
  //   }
  // },
  watch: {
    editingKey: function (newValue) {
      this.changeable = newValue === "";
    }
  },

  mounted() {
    this.init();
  },

  methods: {
    init: async function() {
      this.loadUser();
    },

    loadUser: function() {
      this.loading = true;
      data.length=0;
      this.pagination.current = 1;
      getSelectUser(6, 1).then((oriRes) => {
        // const target = data.filter((item) => key === item.key)[0];
        // this.editingKey = key;
        // if (target) {
        //   target.editable = true;
        // }
        for (let i = 0; i < data.length; i++) {
          data[i].target = false;
        }
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].type==0) {
            this.type="普通用户"
          } else if (res.data[i].type==1){
            this.type="专家认证中"
          } else if (res.data[i].type==2){
            this.type="企业认证中"
          }else if (res.data[i].type==3){
            this.type="封禁中"
          }else if (res.data[i].type==4){
            this.type="认证专家"
          }else if (res.data[i].type==5){
            this.type="认证企业"
          }
          data.push({
            key: res.data[i].id,
            name: res.data[i].username,
            ins: res.data[i].institution,
            type: this.type,
            email: res.data[i].email,
          });
        }
        this.cacheData = data.map((item) => ({ ...item }));
        this.totalCnt = res.data.total_count;
        this.loading = false;
        this.pagination.total = res.page_num;
        console.log(data)
        console.log(this.cacheData)
      }).catch((error) => {
        console.log(error);
      });
    },
    onDelete(key) {
      const newData = [...this.data];
      this.data = newData.filter((item) => item.key !== key);
      const target = newData.filter((item) => key === item.key)[0];
      if(target.type=="个人"){
        this.type1=0
      }else if(target.type=="学校"){
        this.type1=1
      }else{
        this.type1=2
      }
      const params = {
        id:target.key,
        name: target.name,
        usertype: this.type1,
        institution:target.ins,
        mail: target.email,
      };
      let that = this
      UserDel(params)
        .then((res) => {
          this.$message.info("成功删除");
          // this.loadUser();
          console.log(res)
        }).then((res) => {
          that.reload()
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleChange(value, record, col) {
      if (!this.editData.key) {
        this.editData = record
      }
      if (col === "name") {
        this.editData.name = value;
      } else if (col === 'ins') {
        this.editData.ins = value;
      } else if (col === 'email') {
        this.editData.email = value;
      } else if (col === 'type') {
        alert("暂不允许修改用户类型！！")
        this.reload()
      }
      console.log(this.editData)

      this.loadUser()
    },
    edit(key) {
      const newData = [...this.data];
      const target = newData.filter((item) => key === item.key)[0];
      console.log(target)
      this.editingKey = key;
      if (target) {
        target.editable = true;
        this.data = newData;
      }
    },
    // edit(key) {
    //   const target = data.filter((item) => key === item.key)[0];
    //     this.editingKey = key;
    //     if (target) {
    //       target.editable = true;
    //     }
    // },
    save(key) {
      const newData = [...this.data];
      const newCacheData = [...this.cacheData];
      const target = newData.filter((item) => key === item.key)[0];
      const targetCache = newCacheData.filter((item) => key === item.key)[0];
      console.log(target);
      console.log(targetCache);
      if (target && targetCache) {
        delete target.editable;
        this.data = newData;
        Object.assign(targetCache, target);
        this.cacheData = newCacheData;
      }
      this.editingKey = "";
      if(target.type=="个人"){
        this.type1=0
      }else if(target.type=="学校"){
        this.type1=1
      }else{
        this.type1=2
      }
      const params = {
        id: this.editData.key,
        name: this.editData.name,
        // usertype: this.type1,

        institution:this.editData.ins,
        mail: this.editData.email,
      };

      let that = this
      UserModify(params)
        .then((res) => {
          this.$message.info("成功修改");
          console.log(res)
        }).then((res) => {
          that.reload()
        })
        .catch((error) => {
          this.$message.error("无法修改")
          console.log(error);
        });
      if (target) {
        Object.assign(
          target,
          this.cacheData.filter((item) => key === item.key)[0]
        );
        delete target.editable;
        this.data = newData;
      }
      this.reload()
      // this.loadUser()
      // console.log(target.editable
    },
    cancel(key) {
// <<<<<<< HEAD
      let that = this
      let promise = new Promise(function (resolve, reject) {
            const newData = [...that.data];
            const target = newData.filter((item) => key === item.key)[0];
            that.editingKey = "";
            if (target) {
              Object.assign(
                  target,
                  that.cacheData.filter((item) => key === item.key)[0]
              );
              delete target.editable;
              that.data = newData;
            }
            resolve()
          }
      )
      promise.then(
          that.reload()
      )
// =======
//       const newData = [...this.data];
//       for (let i = 0; i < newData.length; i++) {
//         newData[i].editable = false;
//       }
//       const target = newData.filter((item) => key === item.key)[0];
//       this.editingKey = "";
//       if (target) {
//         Object.assign(
//           target,
//           this.cacheData.filter((item) => key === item.key)[0]
//         );
//         console.log(target)
//         this.data = newData;
//       }
//       console.log(data)
// >>>>>>> 27da2901a4f9cddd7dcaaa8106ab332cd6de4a7b
    },
    selectChange(value) {
      if (!this.changeable) {

        alert("请先完成编辑！")
        return
      }
      console.log(value);
      console.log(this.selectedType);
      this.pagination.current = 1;
      getSelectUser(this.selectedType, 1).then((oriRes) => {
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        console.log(data);
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].type==0) {
            this.type="普通用户"
          } else if (res.data[i].type==1){
            this.type="专家认证中"
          } else if (res.data[i].type==2){
            this.type="企业认证中"
          }else if (res.data[i].type==3){
            this.type="封禁中"
          }else if (res.data[i].type==4){
            this.type="认证专家"
          }else if (res.data[i].type==5){
            this.type="认证企业"
          }
          data.push({
            key: res.data[i].id,
            name: res.data[i].username,
            ins: res.data[i].institution,
            type: this.type,
            email: res.data[i].email,
            editable: false
          });
        }
        this.totalCnt = res.data.total_count;
        this.loading = false;
        this.pagination.total = res.page_num;
        this.itemKey = Math.random();
      }).catch((error) => {
        console.log(error);
      });
    }
  },
};
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
