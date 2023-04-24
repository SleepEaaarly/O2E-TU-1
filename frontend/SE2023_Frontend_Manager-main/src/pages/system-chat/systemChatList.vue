<template>
	<!-- <div>
		<el-row >
			<el-scrollbar style="height: 100%;">
			<el-col :span="6" style="height: 600px; overflow: auto;">
				<el-row v-for="(o, index) in 10" :key="o">
					<el-card >
						<el-row>
							<el-col :span="4">
								<el-avatar :size="100" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" rel="external nofollow"></el-avatar>
								<el-avatar icon="el-icon-user-solid"></el-avatar>
							</el-col>
							
							<el-col :span="18">
								<h2>小明同学{{index}}</h2>
								<h2></h2>
							</el-col>
						</el-row>
					</el-card>
				</el-row>
				 <div v-for="fit in fits" :key="fit">
					<el-ava
				</div>
			</el-col>
			</el-scrollbar>
			
			<el-col :span="18">
				<router-view>
					
				</router-view>
			</el-col>
		</el-row>
	</div> -->
	
	<a-card :bordered="false">
		<a-table :data-source="data" :columns="columns">
			<template slot="operation" slot-scope="text, record">
				<div >
					<span>
						<a @click="showSystemChat(record)" >回复</a>
						<a-modal v-model="showDetail" title="客服聊天" width="750px" footer="" ref="chatContent" >
							
							<a-card :bordered="false" dis-hover style="overflow-y: scroll; height: 600px;" >
								<!-- <div v-for="(item, index) in record.messages" :key="index">abc</div> -->
								<!-- <div v-show="false">{{selectData.messages[0].message}}</div>
								<div v-show="false">{{ selectData.messages[1].message }}</div> -->
								<span v-for="(item, index) in selectData.messages" :key="index" v-if="showDetail"  >
									<div class="chat-item">

									
										<a-row v-if="item.gstime" class="system-chat-item">{{item.gstime}}</a-row>
										<!-- 提示转换信息 -->
										<a-row v-if="item.type == 'switch_info'" class="system-chat-time">对方已转换为{{item.message}}服务</a-row>
										<div v-if="item.type !== 'switch_info'" class="system-chat-list" :class="{'system-chat-me': item.isme}">
											<!-- 显示管理员/AI头像 -->
											<Image v-if="!item.isme" :src="item.userpic" mode="widthFix" lazy-load></Image> 
											<!-- 消息 -->
											<a-row class="system-chat-list-body">
												<!-- 文字 -->
												<a-row v-if="item.type == 'text'">{{item.message}}</a-row>
												<!-- 图像 -->
												<a-row v-if="item.type == 'img'" :src="item.message" mode="widthFix" lazy-load></a-row>
												<!-- 卡片 -->
												<a-row v-if="item.type == 'card' && item.cardInfo.cardType == 'expert'">
													[卡片信息]专家名称：{{ item.cardInfo.title }}<br>
													专家信息：{{ item.cardInfo.info }}
												</a-row>
												<a-row v-if="item.type == 'card' && item.cardInfo.cardType == 'enterprise'">
													[卡片信息]企业名称：{{ item.cardInfo.title }}<br>
													专家信息：{{ item.cardInfo.info }}
												</a-row>
												<a-row v-if="item.type == 'card' && item.cardInfo.cardType == 'demand'">{{item.message}}</a-row>
												<a-row v-if="item.type == 'card' && item.cardInfo.cardType == 'technique'">{{item.message}}</a-row>
												<a-row v-if="item.type == 'report' && item.reportInfo.reportType == 'work'">{{item.message}}</a-row>
												<a-row v-if="item.type == 'report' && item.reportInfo.reportType == 'need'">{{item.message}}</a-row>
												<a-row v-if="item.type == 'report' && item.reportInfo.reportType == 'order'">{{item.message}}</a-row>
												<!-- 待会实现 -->
												
											</a-row>
										</div>
									</div>
								</span>
							</a-card>
							<a-card>
								<a-row>
									<a-col :span="20">
										<a-textarea
										v-model:value="reply"
										placeholder="请输入回复，shift+回车换行"
										:auto-size="{ minRows: 2, maxRows: 5 }"
										@keydown.native="handleKeyCode($event)"
										/>
									</a-col>
									<a-col :span="4">
										<a-button @click="handleSubmit(selectData)" >发送</a-button>
									</a-col>
								</a-row>
							</a-card>
							</a-modal>
					</span>
				</div>
			</template>
			<template #expandedRowRender="record, index" class="ant-table-thead">
				<p>{{record.description}}</p>
			</template>
		</a-table>
	</a-card>
</template>

<script>
import {getSystemChatAll, pushSystemChat} from "../../services/systemChat";
import {gettime} from "../../utils/time.js"
// 写一下获取所有聊天的接口
const columns = [{
		title: "姓名",
		dataIndex: "name",
		scopedSlots: {customRender: "name"},
		width: 100,
	}, {
		title: "邮箱",
		dataIndex: "email",
		scopedSlots: {customRender: "email"},
		width: 150
	}, {
		title: "时间",
		dataIndex: "time",
		scopedSlots: {customRender: "time"},
		width: 150
	}, {
		title: "最新消息",
		dataIndex: "message",
		scopedSlots: {customRender: "message"},
		width: 150
	}, {
		title: "操作",
		dataIndex: "operation",
		scopedSlots: {customRender: "operation"},
		width: 150,
		render: () => <a>回复</a>
	}
];
// const data = [
// 	{
// 		name: "usr1",
// 		sex: "男",
// 		email: "123@qq.com",
// 		time: "4/3",
// 		message: "你好你好",
// 		messages: [
// 			{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "sdfadfadfadfadfa",
// 				gstime: "text gstime",
// 				created_at: "test created"
// 			},
// 			{
// 				isme: true,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "msg2",
// 				gstime: null,
// 				created_at: "test created"
// 			},
// 			{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息",
// 				gstime: null,
// 				created_at: "test created"
// 			},
// 			{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息",
// 				gstime: null,
// 				created_at: "test created"
// 			},
// 			{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息",
// 				gstime: null,
// 				created_at: "test created"
// 			},
// 			{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息",
// 				gstime: null,
// 				created_at: "test created"
// 			},
// 			{
// 				isme: true,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "回复回复回复回复",
// 				gstime: null,
// 				created_at: "test created"
// 			},
// 			{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息一个长消息",
// 				gstime: null,
// 				created_at: "test created"
// 			},{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "你好你好",
// 				gstime: null,
// 				created_at: "test created"
// 			}
// 		],
// 	}, 
// 	{
// 		name: "usr2",
// 		sex: "女",
// 		email: "456@qq.com",
// 		time: "4/2",
// 		message: "你好你好",
// 		messages: [{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "sdfadfadfadfadfa",
// 				gstime: "text gstime",
// 				created_at: "test created"
// 			}],
// 	},
// 	{
// 		name: "usr3",
// 		sex: "武装直升机",
// 		email: "abc@buaa.edu.cn",
// 		time: "4/3",
// 		message: "测试长消息测试长消息测试长消息测试长消息测试长消息测试长消息测试长消息",
// 		messages: [{
// 				isme: false,
// 				userpic: "usrpiclink",
// 				type: 'text',
// 				message: "sdfadfadfadfadfa",
// 				gstime: "text gstime",
// 				created_at: "test created"
// 			}],
// 	}
// ];
export default {
	name: "systemChatList",
	inject: ['reload'],
	components: {},
	data() {
		return {
			data: [],
			columns,
			showDetail: false,
			reply: '',
			selectData: {},
			style: {
				contentH: 0,
				itemH: 0
			}
		}
	},
	mounted() {
		this.init();
		this.pageToBottom()
	},
	onload() {
		this.init()
	},
	updated() {
		this.pageToBottom()
	},
	methods: {
		init: async function() {
			console.log("init")
			this.loadAllChat();
		},
		async initdata() {	// 获得当前页面的高度
			try {
				const windowHeight = window.innerHeight
				let t = 200
				// this.style.contentH = windowHeight - uni.upx2px(t)
				this.style.contentH = windowHeight - 2 * t
				// uni.stopPullDownRefresh()
			} catch(e) { console.log(e) }
		},
		pageToBottom() {	// 将聊天界面固定在新聊天底部，目前未实现
			console.log("page to bottom")
			console.log(this)
			// let q = uni.createSelectorQuery().in(this)
			// let itemH = q.selectAll('.chat-item')   // TODO: 不确定这个是否可行
			// console.log(this.currentSystemChatMsgs)
			// if (this.currentSystemChatMsgs.length !== 0) {
			// 	this.$nextTick(() => {
			// 		itemH.fields({size: true}, data => {
			// 			console.log("data is")
			// 			console.log(data)
			// 			if (data) {
			// 				if (isfirst) {
			// 					for (let i = 0; i < data.length; i++) {
			// 						this.style.itemH += data[i].height
			// 					}
			// 					console.log(this.style.itemH)
			// 				} else {
			// 					this.style.itemH += data[data.length - 1].height
			// 				}
			// 				this.scrollTop = (this.style.itemH > this.style.contentH) ? this.style.itemH : 0
			// 			}
			// 		}).exec()
			// 	})
			// }

			// this.$nextTick(() =>{
			// 	console.log(this.$refs.chatContent)
            //     this.$refs.chatContent.scrollTop = this.$refs.chatContent.scrollHeight;
            // })
		},
		loadAllChat: function() {	// 从后端获取所有数据
			console.log("load all chat")
			getSystemChatAll().then((res) => {
				console.log(res);
				// TODO：这部分需要看后端返回的数据是什么
				// let d = res.data.data
				for (let i = 0; i < res.data.system_chat_list.length; i++) {
					let item = res.data.system_chat_list[i]
					let data_item = {}
					data_item.messages = []
					// data_item.name = // TODO: 这块看看用户名称能不能传一下，或者我获取再获取一下用户信息
					data_item.uId = item.userInfo.uId
					data_item.email = item.userInfo.email
					data_item.name = item.userInfo.name
					let bef_time = null
					let last_message = null
					for (let j = 0; j < item.messages.length; j++) {
						let res_message = item.messages[j]
						let data_message = {}
						data_message.isme = res_message.isme
						data_message.userpic = res_message.userpic
						data_message.type = res_message.type
						data_message.message = res_message.message
						data_message.cardInfo = res_message.cardInfo
						data_message.created_at = res_message.created_at
						if (bef_time === null) {
							data_message.gstime = gettime.gettime(res_message.created_at, 0)
							bef_time = res_message.created_at
						} else {
							data_message.gstime = 
								gettime.gettime(res_message.created_at, bef_time)
							bef_time = res_message.created_at
						}
						console.log(res_message.created_at)
						data_item.messages.push(data_message)
						last_message = data_message.message
					}
					// for (res_message in item.messages) {
						
					// }
					data_item.time = bef_time
					data_item.message = last_message
					console.log(data_item)
					this.data.push(data_item)
				}
				
			}).catch((error) => {
				console.log(error);	
			})
		},
		handleSubmit(selectData) {	// 用户选择提交之后，将信息数据提交给后端
			// console.log(this.selectData)
			console.log("abc")
			// 发送回复的 submit 函数，需要确定数据类型
			pushSystemChat({
				"uId": this.selectData.uId,
				"content": this.reply, 
			}).then((res) => {
				console.log(res);
				// let d = res.data.data
				// if res.data.recode == 200 | 500
				let now = new Date().getTime()
				let obj = {
					isme: false,
					userpic: "",
					type: "text",
					message: this.reply,
					gstime: gettime.gettime(now, selectData.messages[selectData.messages.length - 1].created_at),
					created_at: now
				}
				selectData.messages.push(obj)
			}).catch((error) => {
				console.log(error)
			})
			this.reply = ""
		},
		showSystemChat(record) {	// 页面中展示聊天框，没有实际作用
			// 感觉这里record只需要用户id这类的值
			this.showDetail = true;
			this.selectData = record;
			console.log(record)
		}, 
		handleKeyCode(event) {
			console.log(event)
			if (event.keyCode == 13) {
				if (!event.shiftKey) {
					event.preventDefault();
					this.handleSubmit(this.reply);
				} else {
					this.reply = this.reply + "\n";
					event.preventDefault();
				}
			}
		}
	},

}

</script>

<style>
.el-row {
  display: flex;
  flex-wrap: wrap;
}
.highlight {
	background-color: rgb(255, 192, 105);
	padding: 0px;
}
.editable-row-operations a {
	margin-right: 8px;
}

.system-chat-list {
    padding: 20px 0;
}

.system-chat-list>image {
    width: 80px !important;
    height: 80px !important;
    flex-shrink: 0;
    margin: 0 10px;
}

.system-chat-list-body {
    position: relative;
    background: #f4f4f4;
    padding: 25px;
    margin-left: 20px;
    border-radius: 20px;
    margin-right: 100px;
}
.system-chat-list-body:after {
    position: absolute;
    left: -30px;
    right: 0;
    top: 30px;
    content: '';
	width: 0;
	height: 0;
	border: 16px solid #F4F4F4;
	border-color: transparent #F4F4F4 transparent transparent;
}
.system-chat-me {
    justify-content: flex-end;
}
.system-chat-me .system-chat-list-body:after {
    left: auto;
	right: -30px;
	border-color: transparent transparent transparent #F4F4F4;
}

.system-chat-list-body>image {
    max-width: 150px;
	max-height: 200px;
}

.system-chat-list-body>system-chat-card {
    padding: 0;
    max-width: 150px;
	max-height: 200px;
}

.system-chat-time {
    padding: 50px 0;
	color: #a2a2a2;
	font-size: 24px;
}
</style>
