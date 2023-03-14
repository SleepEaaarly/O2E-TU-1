<template>
	<view>

		<!-- 顶端多栏导航-->
		<swiper-tab-head :tabBars="tabBars" :tabIndex="tabIndex" @tabtap="tabtap" scrollItemStyle="width:25%;">

		</swiper-tab-head>
		
		<!-- 分享订单弹窗 -->
		<uni-popup ref="shareLink" type="share">
			<uni-popup-share title="分享到" @select="select"></uni-popup-share>
		</uni-popup>
		
		
		<!-- 接受、拒绝订单的二次提示 -->
		<uni-popup ref="confirmOperation" type="dialog">
			<uni-popup-dialog type="warn" cancelText="取消" confirmText="确定" title="警告" content="确认吗？此操作将不可更改" 
				@confirm="operationConfirm"	@close="operationClose"></uni-popup-dialog>
		</uni-popup>
		
		<!-- bar1:全部 -->
		<view v-if="tabIndex == 0">
			<!-- 若无返回数据，展示无订单界面 -->
			<view v-if="datalist1.length == 0">
				<no-order @goToExplore="goToExplore"></no-order>
			</view>
			
			<uni-section v-else title="全部订单" type="line" >
				<uni-card v-for="(item, index) in datalist1" :key="index" :title="'需求：'+item.title" 
					:sub-title="userInfo.type == EXPERT ? item.entp_name : item.exp_name" :extra="item.time" 
					:thumbnail="userInfo.type == EXPERT ? item.headpic : item.exp_pic" @click="openOrderDetail(item)">
					<text class="uni-body">{{userInfo.type == EXPERT ? item.description: item.exp_des}}</text>
					<!-- 底部功能组件 -->
					
					<!-- state = 0, 待接受 -->
					<view v-if="item.state == 0" slot="actions" class="card-actions no-border u-f-ac u-f-jsb">	<!-- ac和jsb是设置横向+居中+两端对齐样式 -->
						<!-- 4 = 企业， 5 = 专家 -->
						<view v-if="userInfo.type == EXPERT" class="card-actions-item" @click.stop="actionsClick('拒绝订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="closeempty" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">拒绝订单</text>
						</view>
						<view v-if="userInfo.type == EXPERT" class="card-actions-item" @click.stop="actionsClick('接受订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="checkmarkempty" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">接受订单</text>
						</view>
						<view v-if="userInfo.type == EXPERT" class="card-actions-item" @click.stop="actionsClick('联系企业', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="chatboxes" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">联系企业</text>
						</view>
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('催促专家', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="notification" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">催促专家</text>
						</view>
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('联系专家', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="chatboxes" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">联系专家</text>
						</view>
					</view>
					
					<!-- state = 1, 正在合作中 -->
					<view v-else-if="item.state == 1" slot="actions" class="card-actions no-border u-f-ac u-f-jsb">	<!-- ac和jsb是设置横向+居中+两端对齐样式 -->
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('完成订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="medal" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">完成订单</text>
						</view>
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('放弃订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="link" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">放弃订单</text>
						</view>
						<view class="card-actions-item" @click.stop="actionsClick('帮助', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="help" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">帮助</text>
						</view>
					</view>
					
					<!-- state = 2+3, 已拒绝+已结束 -->
					<view v-else slot="actions" class="card-actions no-border u-f-ac u-f-jsb">	<!-- ac和jsb是设置横向+居中+两端对齐样式 -->
						<view class="card-actions-item" @click.stop="actionsClick('分享', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="redo" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">分享</text>
						</view>
						<view v-show='userInfo.type==5' class="card-actions-item" @click.stop="actionsClick('评价', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="chatbubble" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">评价</text>
						</view>
						<view class="card-actions-item" @click.stop="actionsClick('再来一单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="cart" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">再来一单</text>
						</view>
					</view>
				</uni-card>
			</uni-section>
		</view>
		
		<!-- bar2:待处理 -->
		<view v-else-if="tabIndex == 1">
			<!-- 若无返回数据，展示无订单界面 -->
			<view v-if="datalist2.length == 0">
				<no-order @goToExplore="goToExplore"></no-order>
			</view>
			
			<uni-section title="待处理订单" type="line" >
				<uni-card v-for="(item, index) in datalist2" :key="index" :title="'需求：'+item.title"
					:sub-title='userInfo.type == EXPERT ? item.entp_name : item.exp_name' :extra="item.time" 
					:thumbnail='userInfo.type == EXPERT ? item.headpic : item.exp_pic' @click="openOrderDetail(item)">
					
					<text class="uni-body">{{userInfo.type == EXPERT ? item.description: item.exp_des}}</text>
					<!-- 底部功能组件 -->
					<view slot="actions" class="card-actions no-border u-f-ac u-f-jsb">	<!-- ac和jsb是设置横向+居中+两端对齐样式 -->
						<!-- 4 = 企业， 5 = 专家 -->
						<view v-if="userInfo.type == EXPERT" class="card-actions-item" @click.stop="actionsClick('拒绝订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="closeempty" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">拒绝订单</text>
						</view>
						<view v-if="userInfo.type == EXPERT" class="card-actions-item" @click.stop="actionsClick('接受订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="checkmarkempty" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">接受订单</text>
						</view>
						<view v-if="userInfo.type == EXPERT" class="card-actions-item" @click.stop="actionsClick('联系企业', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="chatboxes" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">联系企业</text>
						</view>
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('催促专家', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="notification" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">催促专家</text>
						</view>
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('联系专家', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="chatboxes" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">联系专家</text>
						</view>
					</view>
					
				</uni-card>
			</uni-section>
		</view>

		
		<!--bar3:进行中 -->
		<view v-else-if="tabIndex == 2">
			<!-- 若无返回数据，展示无订单界面 -->
			<view v-if="datalist3.length == 0">
				<no-order @goToExplore="goToExplore"></no-order>
			</view>
			
			<uni-section title="进行中订单" type="line" >
				<uni-card v-for="(item, index) in datalist3" :key="index" :title="'需求：'+item.title"
					:sub-title="userInfo.type == EXPERT ? item.entp_name : item.exp_name" :extra="item.time" 
					:thumbnail="userInfo.type == EXPERT ? item.headpic : item.exp_pic" @click="openOrderDetail(item)">
					<text class="uni-body">{{userInfo.type == EXPERT ? item.description: item.exp_des}}</text>
					<!-- 底部功能组件 -->
					<view slot="actions" class="card-actions no-border u-f-ac u-f-jsb">	<!-- ac和jsb是设置横向+居中+两端对齐样式 -->
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('完成订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="medal" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">完成订单</text>
						</view>
						<view v-if="userInfo.type == ENTERPRISE" class="card-actions-item" @click.stop="actionsClick('放弃订单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="link" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">放弃订单</text>
						</view>
						<view class="card-actions-item" @click.stop="actionsClick('帮助', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="help" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">帮助</text>
						</view>
					</view>
				</uni-card>
			</uni-section>
		</view>
		
		<!-- bar4:已完成 -->
		<view v-else>
			<!-- 若无返回数据，展示无订单界面 -->
			<view v-if="datalist4.length == 0">
				<no-order @goToExplore="goToExplore"></no-order>
			</view>
			
			<uni-section title="已完成订单" type="line" >
				<uni-card v-for="(item, index) in datalist4" :key="index" :title="'需求：'+item.title" 
					:sub-title="userInfo.type == EXPERT ? item.entp_name : item.exp_name" :extra="item.time" 
					:thumbnail="userInfo.type == EXPERT ? item.headpic : item.exp_pic" @click="openOrderDetail(item)">
					<text class="uni-body">{{userInfo.type == EXPERT ? item.description: item.exp_des}}</text>
					<!-- 底部功能组件 -->
					<view slot="actions" class="card-actions no-border u-f-ac u-f-jsb">	<!-- ac和jsb是设置横向+居中+两端对齐样式 -->
						<view class="card-actions-item" @click.stop="actionsClick('分享', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="redo" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">分享</text>
						</view>
						<view v-show='userInfo.type==5' class="card-actions-item" @click.stop="actionsClick('评价', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="chatbubble" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">评价</text>
						</view>
						<view class="card-actions-item" @click.stop="actionsClick('再来一单', item)">	<!--加stop修饰阻止事件继续冒泡传播-->
							<uni-icons type="cart" size="20" color="#999"></uni-icons>
							<text class="card-actions-item-text">再来一单</text>
						</view>
					</view>
				</uni-card>
			</uni-section>
		</view>
	</view>
	
</template>

<script>
	//关于需求平台各类型需求订单主界面的样式
	import uniCard from '@/components/uni-card/uni-card.vue'
	import uniSwipeAction from '@/components/uni-swipe-action/uni-swipe-action.vue'
	import uniSwipeActionItem from '@/components/uni-swipe-action-item/uni-swipe-action-item.vue'
	import swiperTabHead from '@/components/index/swiper-tab-head.vue'
	
	//import tuiCard from "@/components/thorui/tui-card/tui-card"
	//import tuiSwipeAction from "@/components/thorui/tui-swipe-action/tui-swipe-action"
	//import tuiBubblePopup from "@/components/thorui/tui-bubble-popup/tui-bubble-popup"
	//import tuiIcon from "@/components/thorui/tui-icon/tui-icon"
	
	import tuiModal from '@/components/thorui/tui-modal/tui-modal'	//提示窗
	import tuiAlert from '@/components/thorui/tui-alert/tui-alert'	//提示窗
	
	import noOrder from '@/components/common/no-order.vue'	//无订单
	
	//订单相关函数
	import {
		getFinishedOrder,
		getCooperatingOrder,
		getPendingOrder,
		getAllOrder,
		acceptOrder,
		rejectOrder,
		accomplishOrder,
		abandonOrder,
	} from '@/api/platform/order.js'
	
	//需要用contact函数
	import { createContact } from '@/api/need-detail.js'
	
	export default {
		data(){
			return {
				curOperation: '',	//二次确认，当前的操作类型
				order_id: '',
								
				EXPERT: 4,
				ENTERPRISE: 5,	//usertype的常量
				show:[],
				tabIndex: 1,	//默认进“待处理”界面
				tabBars: [
					{
						name: '全部',
						id: 'quanbu',
						page: 1
					},
					{
						name: '待处理',
						id: 'daichuli',
						page: 1
					},
					{
						name: '进行中',
						id: 'jinxingzhong',
						page: 1
					},
					{
						name: '已完成',
						id: 'yiwancheng',
						page: 1
					},
				],
				actions:[
					{
						name:'删除',
						color: '#fff',
						fontsize: 30, //单位rpx
						width: 70, //单位px
						background: '#FD3B31',
					}
				],
				datalist1:[],	//全部
				datalist2:[],	//待处理
				datalist3:[],	//进行中
				datalist4:[],	//已完成
			}
		},
		
		components:{
			swiperTabHead,
			noOrder,
			// tuiCard,
			// tuiSwipeAction,
			// tuiBubblePopup,
			// tuiIcon,
			// tuiModal,
		},
		props:{
			needdata: Array,
			userInfo: Object,
			//item:Object,	//关于odrder_list信息
		},
		onShow(){		//页面加载,一个页面只会调用一次
			console.log('onshow')
			this.refreshData()
		},
		onLoad(){		//页面显示,每次打开页面都会调用一次
			console.log('onload')
			this.refreshData()
		},
		created(){
			this.refreshData()
		},
		beforeMount(){
			//this.refreshData()
		},
		mounted(){
			//this.refreshData()			
		},
		beforeUpdate(){
			
		},
		updated() {
			//this.refreshData();	万万不可刷新！否则就永远loading了
		},
		methods:{
			temp(id){
				console.log(id)
			},
			tabtap(index) {
				this.tabIndex = index
				this.refreshData()
			},
			goToNeed(index){
				console.log(index)
				this.$emit('goToNeedInfo',index)
			},
			closeshow(){
				this.show=false
			},
			onClick(){
				console.log('click for detail')
				//todo
			},
			print(id){
				if(this.show[id] === true){
					this.show.splice(id,1,false)
					
				}
				else{
					this.show.splice(id,1,true)
				}
				console.log(id+'success '+this.show[id])
			},
			
			//打开订单详情
			openOrderDetail(orderItem){
				console.log('click for order detail. id = '+ orderItem.order_id)
				this.$emit('openOrderDetail', orderItem.order_id)
			},
			
			// initData(){
			// 	this.datalist1 = [];	//已完成 全部
			// 	this.datalist2 = [];	//进行中
			// 	this.datalist3 = [];	//待处理
			// 	this.randIdPool = ["CSDN云社区", "Zhihu小管家", "微博Bot", "Siri"]
				
			// 	if(this.userInfo && this.userInfo.id){
			// 		for(var i=1;i<=10;i++){
			// 			this.show[i]=false;
			// 			let a={
			// 				// id:i,
			// 				// img: {
			// 				// 	url: this.userInfo.userpic,
			// 				// 	circle:true,
			// 				// },
			// 				// title: {
			// 				// 	text: this.randIdPool[Math.floor(Math.random() * this.randIdPool.length)],
			// 				// 	size: 34,
			// 				// },
			// 				// tag: {
			// 				// 	text: parseInt(Math.random()*(23+1),10)+"小时前",
			// 				// 	color: '#ed3f14',
			// 				// 	size: 26,
			// 				// },
			// 				// header: {
			// 				// 	bgcolor: '#f7f7f7',
			// 				// 	line: true,
			// 				// },
							
			// 				id:i,
			// 				img: this.userInfo.userpic,
			// 				title: this.randIdPool[Math.floor(Math.random() * this.randIdPool.length)],
			// 				extra: parseInt(Math.random()*(23+1),10)+"小时前",
			// 			};
			// 			Math.random() < 0.5 ? this.datalist1.push(a): 1;
			// 			Math.random() < 0.5 ? this.datalist2.push(a): 1;
			// 			Math.random() < 0.5 ? this.datalist3.push(a): 1;
			// 		}
			// 	}
			// },
			
			async refreshData(){	//需要加async/await, 否则接口返回为一个Promise类型
				switch (this.tabIndex) {
					case 0:
						this.datalist1 = await getAllOrder(this.userInfo.id)
						break
					case 1:
						this.datalist2 = await getPendingOrder(this.userInfo.id)
						break
					case 2:
						this.datalist3 = await getCooperatingOrder(this.userInfo.id)
						break
					case 3:
						this.datalist4 = await getFinishedOrder(this.userInfo.id)
						break
					default:
						break
				}
			},
			
			async actionsClick(str, item){
				let order_id = item.order_id
				switch(str) {
					case '联系企业': 	//与专家case二合一
					case '联系专家':
						console.log(str)
						this.contact(item)
						//this.refreshData()
						break
					case '帮助':
						uni.navigateTo({ url:'../feedback/feedback' })
						console.log(str)
						break
					case '分享':
						console.log(str)
						this.$refs.shareLink.open('center')
						break
					case '拒绝订单':
						this.curOperation = 'reject'
						this.order_id = order_id
						this.$refs.confirmOperation.open()
						console.log(str)
						break
					case '接受订单':
						this.curOperation = 'accept'
						this.order_id = order_id
						this.$refs.confirmOperation.open()
						console.log(str)
						break
					case '完成订单':
						this.curOperation = 'accomplish'
						this.order_id = order_id
						this.$refs.confirmOperation.open()
						console.log(str)
						break
					case '放弃订单':
						this.curOperation = 'abandon'
						this.order_id = order_id
						this.$refs.confirmOperation.open()
						console.log(str)
						// uni.showToast({ title:'施工中...', duration:500 })
						break
					case '评价':
						console.log(str)
						uni.navigateTo({ url:'../../pages/postEvaluation/postEvaluation?oid='+item.order_id })
						break
					case '再来一单':
						console.log(str)
						this.contact(item)
						// uni.showToast({
						// 	title:'跳转企业中', 
						// 	duration:1500 ,
						// 	})
						// setTimeout(function(){	//延迟跳转
						// 	uni.hideLoading()
						// 	this.contact(item)
						// }, 2000)
						break
					
					case '催促专家':
						console.log(str)
						uni.showToast({ title:'已发送提醒！', duration:500 })
						break
					default:
						break
				}
			},
			
			//跳转到联系对方聊天窗口
			contact(item) {
				if(this.userInfo.type === this.EXPERT) {
					//自己是企业，则联系专家
					var contact_id = item.entp_id	//不能用let!否则传不出 {} 区域
				} else {
					var contact_id = item.exp_id
				}
				let temp={
					enterprise_id:item.entp_id,
					expert_id:item.exp_id,
					need_id:item.need_id,
				}
				//console.log("contact:"+item.need_id)
				//console.log("Cid = ", contact_id)
				createContact(temp)
				uni.navigateTo({ url:'../user-chat/user-chat?fid=' + contact_id })
			},
			
			//去逛逛
			goToExplore(){
				//console.log("in needdata.")
				this.$emit('goToExplore')
			},
			
			//确认操作
			async operationConfirm(){
				switch(this.curOperation){
					case 'reject':	//拒绝订单
						await rejectOrder(this.userInfo.id, this.order_id)
						uni.showToast({ title:'操作成功！', duration:500 })
						break
					case 'accept':	//接受订单
						await acceptOrder(this.userInfo.id, this.order_id)
						uni.showToast({ title:'操作成功！', duration:500 })
						break
					case 'accomplish':	//完成订单
						await accomplishOrder(this.userInfo.id, this.order_id)
						uni.showToast({ title:'操作成功！', duration:500 })
						break
					case 'abandon':	//放弃订单
						await abandonOrder(this.userInfo.id, this.order_id)
						uni.showToast({ title:'操作成功！', duration:500 })
						break
				}
				// TODO 做一些其他的事情，手动执行 close 才会关闭对话框
				// ...
				this.refreshData()
				this.$refs.confirmOperation.close()
			},
			//关闭提示框
			operationClose(){
				// TODO 做一些其他的事情，before-close 为true的情况下，手动执行 close 才会关闭对话框
				// ...
				this.$refs.confirmOperation.close()
			}
		}
	}
</script>

<style scoped>

</style>
