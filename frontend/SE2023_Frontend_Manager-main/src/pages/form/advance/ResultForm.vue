<template>
    <a-card :bordered="false">
      <h2>选择成果类型</h2>
      <a-space>
        <a-select
            ref="select"
            v-model:value="selectedType"
            style="width: 120px"
            @change="selectChange"
            :disabled="!changeable"
        >
          <a-select-option value="1">认证中</a-select-option>
          <a-select-option value="2">已认证</a-select-option>
          <a-select-option value="3">全部</a-select-option>
        </a-select>

        <a-input-search
          v-model="searchText"
          placeholder="请输入成果关键词"
          enter-button
          @search="onSearch()"
          style="width: 300px;margin-left: 10px;"
        />
        <!-- <a-button
                  type="primary"
                  @click="adminCreateResult()"
        >
                添加成果
        </a-button> -->
        <a-modal v-model="result_visible" title="添加成果" @ok="handleOk">
          <a-form :form="result_info" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }" @submit="handleSubmit">
            
            <a-form-item label="成果标题">
              <a-input
                placeholder="请输入成果标题"
                v-decorator="['note', { rules: [{ required: true, message: '请输入有效的成果标题!' }] }]"
              />
            </a-form-item>

            <a-form-item label="成果摘要">
              <a-input
                type="textarea"
                placeholder="请输入成果摘要"
              />
            </a-form-item>

            <a-form-item label="成果作者">
              <a-input
                placeholder="多个作者用英文逗号分隔"
              />
            </a-form-item>


            <a-form-model-item label="成果领域">
              <a-select placeholder="请为您的成果确定主要领域方向">
                <a-select-option value="0">
                  信息技术
                </a-select-option>
                <a-select-option value="1">
                  装备制造
                </a-select-option>
                <a-select-option value="2">
                  新材料
                </a-select-option>
                <a-select-option value="3">
                  新能源
                </a-select-option>
                <a-select-option value="4">
                  节能环保
                </a-select-option>
                <a-select-option value="5">
                  生物医药
                </a-select-option>
                <a-select-option value="6">
                  科学创意
                </a-select-option>
                <a-select-option value="7">
                  检验检测
                </a-select-option>
                <a-select-option value="8">
                  其他
                </a-select-option>
              </a-select>
            </a-form-model-item>

            <a-form-model-item label="成果阶段">
              <a-radio-group>
                <a-radio value="0">
                  实验室
                </a-radio>
                <a-radio value="1">
                  样品
                </a-radio>
                <a-radio value="2">
                  中试
                </a-radio>
                <a-radio value="3">
                  产业化
                </a-radio>
              </a-radio-group>
            </a-form-model-item>

            <!-- <a-form-item label="成果示意图">
              <a-upload
                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                list-type="picture-card"
                :file-list="fileList"
                @preview="handlePreview"
                @change="handleChange"
              >
                <div v-if="fileList.length < 1">
                  <a-icon type="plus" />
                  <div class="ant-upload-text">
                    Upload
                  </div>
                </div>
              </a-upload>
              <a-modal :visible="previewVisible" :footer="null" @cancel="handleCancel">
                <img alt="example" style="width: 100%" :src="previewImage" />
              </a-modal>
            </a-form-item> -->

            <a-form-item label="成果内容">
              <a-input
                type="textarea"
                placeholder="介绍成果的内容"
              />
            </a-form-item>

            <!-- <a-form-item label="成果详情图">
              <a-upload
                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                list-type="picture-card"
                :file-list="fileList"
                @preview="handlePreview"
                @change="handleChange"
              >
                <div v-if="fileList.length < 9">
                  <a-icon type="plus" />
                  <div class="ant-upload-text">
                    Upload
                  </div>
                </div>
              </a-upload>
              <a-modal :visible="previewVisible" :footer="null" @cancel="handleCancel">
                <img alt="example" style="width: 100%" :src="previewImage" />
              </a-modal>
            </a-form-item> -->
          
          </a-form>
        </a-modal>
        
      </a-space>
      <br/>
      <br/>
      <a-table :data-source="data" :columns="columns" :pagination="pagination" :key="itemKey">
        <template
          v-for="col in ['name', 'pyear', 'field', 'period', 'abstract', 'content']"
          :slot="col"
          slot-scope="text, record"
        >
        <!-- <template
          v-for="col in ['name', 'pyear', 'field', 'period']"
          :slot="col"
          slot-scope="text, record"
        > -->
        
          <div :key="col" class="ellipsis" style="text-overflow:ellipsis;overflow:hidden;white-space:nowrap;">
            <a-input
              v-if="record.editable"
              style="margin: -5px 0;"
              :value="text"
              @change="(e) => handleChange(e.target.value, record, col)"
              class="ellipsis"
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
  import { searchWork, getWorkAll, WorkDel, WorkModify} from '../../../services/work';
  const columns = [
    {
      title: "成果名",
      dataIndex: "name",
      width: "20%",
      scopedSlots: { customRender: "name" },
    },
    {
      title: "年份",
      dataIndex: "pyear",
      width: "10%",
      scopedSlots: { customRender: "pyear" },
    },
    {
      title: "领域",
      dataIndex: "field",
      width: "10%",
      scopedSlots: { customRender: "field" },
    },
    {
      title: "阶段",
      dataIndex: "period",
      width: "10%",
      scopedSlots: { customRender: "period" },
      // onFilter: (value, record) => record.type.indexOf(value) === 0,
    },
    {
      title: "摘要",
      dataIndex: "abstract",
      width: "20%",
      scopedSlots: { customRender: "abstract" },
      //class: "my-cell"
    },
    {
      title: "内容",
      dataIndex: "content",
      width: "20%",
      scopedSlots: { customRender: "content" },
      // class: "my-cell"
    },
    {
      title: "操作",
      dataIndex: "operation",
      scopedSlots: { customRender: "operation" },
    },
  ];
  const data = [];
  
  export default {
    name: "ResultForm",
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
        searchText: '',
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
            getWorkAll(page).then((oriRes) => {
              console.log(oriRes);
              let res = oriRes.data;
              data.length = 0;
              for (let i = 0; i < res.data.length; i++) {
                if (res.data[i].state==0) {
                  this.type="认证中"
                } else if (res.data[i].state==1){
                  this.type="已认证"
                } else if (res.data[i].state==2){
                  this.type="认证失败"
                }
                data.push({
                  key: res.data[i].id,
                  name: res.data[i].title,
                  pyear: res.data[i].pyear,
                  abstract: res.data[i].abstract,
                  content: res.data[i].content, 
                  type: this.type,
                  period: res.data[i].period,
                  field: res.data[i].field,
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
        this.loadResult();
      },
  
      loadResult: function() {
        this.loading = true;
        data.length=0;
        this.pagination.current = 1;
        getWorkAll(1).then((oriRes) => {
          // const target = data.filter((item) => key === item.key)[0];
          // this.editingKey = key;
          // if (target) {
          //   target.editable = true;
          // }
        for (let i = 0; i < data.length; i++) {
          data[i].target = false;
        }
        console.log('response')
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        for (let i = 0; i < res.data.length; i++) {
            if (res.data[i].state==0) {
                this.type="认证中"
            } else if (res.data[i].state==1){
                this.type="已认证"
            } else if (res.data[i].state==2){
                this.type="认证失败"
            }
            data.push({
                key: res.data[i].id,
                name: res.data[i].title,
                abstract: res.data[i].abstract,
                content: res.data[i].content, 
                pyear: res.data[i].pyear,
                type: this.type,
                period: res.data[i].period,
                field: res.data[i].field,
                editable: false
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

        const params = {
          id:target.key,
          name: target.name,
          type:this.type,
          period: target.period,
          abstract:target.abstract,
          content: target.content, 
          pyear: target.pyear,
          field: target.field,
        };
        let that = this
        WorkDel(params)
          .then((res) => {
            this.$message.info("成功删除");
            // this.loadResult();
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
        console.log('check key')
        console.log(this.editData.key)
        if (col === "name") {
          alert("暂不允许修改成果名称！")
          this.reload()
          // this.editData.name = value;
        } else if (col === 'abstract') {
          this.editData.abstract = value;
        } else if (col === 'field') {
          this.editData.field = value;
        } else if (col === 'period') {
          this.editData.period = value
        } else if(col === 'pyear'){
          this.editData.pyear = value
        } else if(col === 'content'){
          this.editData.content = value
        }
        console.log(this.editData)
  
        this.loadResult()
      },
      edit(key) {
        const newData = [...this.data];
        // console.log(this.data)
        const target = newData.filter((item) => key === item.key)[0];
        // console.log(target)
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

        const params = {
          id: this.editData.key,
          title: this.editData.name,
          period: this.editData.period,
          abstract:this.editData.abstract,
          content: this.editData.content, 
          pyear: this.editData.pyear,
          field: this.editData.field,
        };
  
        let that = this
        WorkModify(params)
          .then((res) => {
            console.log('成功修改')
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
        // this.loadResult()
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
      adminCreateResult(){
      this.result_visible = true;
      console.log('Admin Create Reult');
      
      
    },
      selectChange(value) {
        if (!this.changeable) {
  
          alert("请先完成编辑！")
          return
        }
        console.log(value);
        console.log(this.selectedType);
        this.pagination.current = 1;
        getWorkAll(1).then((oriRes) => {
          console.log(oriRes);
          let res = oriRes.data
          console.log(res);
          data.length = 0;
          console.log(data);
          for (let i = 0; i < res.data.length; i++) {
            if (res.data[i].state==0) {
                this.type="认证中"
            } else if (res.data[i].state==1){
                this.type="已认证"
            } else if (res.data[i].state==2){
                this.type="认证失败"
            }
            data.push({
                key: res.data[i].id,
                name: res.data[i].title,
                abstract: res.data[i].abstract,
                content: res.data[i].content, 
                pyear: res.data[i].pyear,
                period: res.data[i].period,
                field: res.data[i].field,
                type: this.type,
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
      },
      onSearch(){
        this.loading = true;
        data.length=0;
        this.pagination.current = 1;
        var params = {
          "title": this.searchText,
          "page": this.pagination.current
        }
        searchWork(params).then((oriRes) => {
          // const target = data.filter((item) => key === item.key)[0];
          // this.editingKey = key;
          // if (target) {
          //   target.editable = true;
          // }
        for (let i = 0; i < data.length; i++) {
          data[i].target = false;
        }
        console.log('response')
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        for (let i = 0; i < res.data.length; i++) {
            if (res.data[i].state==0) {
                this.type="认证中"
            } else if (res.data[i].state==1){
                this.type="已认证"
            } else if (res.data[i].state==2){
                this.type="认证失败"
            }
            data.push({
                key: res.data[i].id,
                name: res.data[i].title,
                abstract: res.data[i].abstract,
                pyear: res.data[i].pyear,
                content: res.data[i].content, 
                type: this.type,
                period: res.data[i].period,
                field: res.data[i].field,
                editable: false
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

  .ellipsis {
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  }

  
  </style>
  