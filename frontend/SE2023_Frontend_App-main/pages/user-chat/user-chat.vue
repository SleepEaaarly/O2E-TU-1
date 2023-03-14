<template>
	<view>
		<tui-button v-if="need&& need.need_id" @click="openmenu" :size="28" :plain="true">
			
		需求标题：{{this.need.title}}
		
		</tui-button>
		<template v-if="userInfo.type=='5' && need">
			
			<tui-bubble-popup :show="show" :mask="true" position="absolute" width="370rpx" translateY="0rpx" triangleTop="-50rpx" borderWidth="0" @close="openmenu()">
				<tui-list-cell :hover="true" :arrow="true" backgroundColor="#dcdcdc" @click="goToNeedDetail(need.need_id)">
					<tui-icon name="search"></tui-icon>
						查看需求
				</tui-list-cell>
				
			</tui-bubble-popup>
			<view v-if="order.order_id==0">
			<tui-bubble-popup :show="show" :mask="false" position="absolute" width="370rpx" translateY="0rpx" translateX="380rpx" triangleTop="-20rpx" borderWidth="0" @close="openmenu()">
				
				<tui-list-cell :hover="true" :arrow="false" backgroundColor="#dcdcdc" @click="createOrderAndRefresh()">
					<tui-icon name="order"></tui-icon>
						发起订单
				</tui-list-cell>
			</tui-bubble-popup>
			</view>
			<view v-if="order.order_id!=0">
			<tui-bubble-popup :show="show" :mask="false" position="absolute" width="370rpx" translateY="0rpx" translateX="380rpx" triangleTop="-20rpx" borderWidth="0" @close="openmenu()">
				
				<tui-list-cell :hover="true" :arrow="true" backgroundColor="#dcdcdc" @click="goToOrderDetail(order.order_id)">
					<tui-icon name="search"></tui-icon>
						查看订单
						
				</tui-list-cell>
			</tui-bubble-popup>
			</view>
			<tui-bubble-popup v-if="order.order_id!=0 && order.state==1" :show="show" :mask="true" position="absolute" width="370rpx" translateY="120rpx" triangleTop="-50rpx" borderWidth="0" @close="openmenu()">
				<tui-list-cell :hover="true" :arrow="false" backgroundColor="#dcdcdc" @click="accomplishOrderAndRefresh()">
					<tui-icon name="check"></tui-icon>
						完成订单
				</tui-list-cell>
				
			</tui-bubble-popup>
			
		</template>
		<template v-else-if="userInfo.type=='4' && need">
			<tui-bubble-popup :show="show" :mask="true" position="absolute" width="370rpx" translateY="0rpx" triangleTop="-50rpx" borderWidth="0" @close="openmenu()">
				<tui-list-cell :hover="true" :arrow="true" backgroundColor="#dcdcdc" @click="goToNeedDetail(need.need_id)">
					<tui-icon name="search"></tui-icon>
						查看需求
				</tui-list-cell>
				
			</tui-bubble-popup>
			<template v-if="order.order_id!=0">
			<tui-bubble-popup :show="show" :mask="false" position="absolute" width="370rpx" translateY="0rpx" translateX="380rpx" triangleTop="-20rpx" borderWidth="0" @close="openmenu()">
				
				<tui-list-cell :hover="true" :arrow="true" backgroundColor="#dcdcdc" @click="goToOrderDetail(order.order_id)">
					<tui-icon name="search"></tui-icon>
						查看订单
						
				</tui-list-cell>
			</tui-bubble-popup>
			<view v-if="order.state==0">
			<tui-bubble-popup :show="show" :mask="true" position="absolute" width="370rpx" translateY="120rpx" triangleTop="-50rpx" borderWidth="0" @close="openmenu()">
				<tui-list-cell :hover="true" :arrow="false" backgroundColor="#dcdcdc" @click="acceptOrderAndRefresh()">
					<tui-icon name="check"></tui-icon>
						接受订单
				</tui-list-cell>
				
			</tui-bubble-popup>
			<tui-bubble-popup :show="show" :mask="false" position="absolute" width="370rpx" translateY="120rpx" translateX="380rpx" triangleTop="-20rpx" borderWidth="0" @close="openmenu()">
				
				<tui-list-cell :hover="true" :arrow="false" backgroundColor="#dcdcdc" @click="rejectOrderAndRefresh()">
					<tui-icon name="shut"></tui-icon>
						拒绝订单
						
				</tui-list-cell>
			</tui-bubble-popup>
			</view>
			</template>
		</template>
		<scroll-view id="scrollview" scroll-y :scroll-top="scrollTop" 
		:scroll-with-animation="true"
		refresher-enabled
		@refresherrefresh="scrollTopHandle"
		:refresher-triggered="triggered"
		:style="{height:style.contentH+'px'}">
			<!-- 聊天列表 -->
			<block v-for="(item,index) in currentChatMsgs" :key="index">
				<view class="chat-item">
				<user-chat-list 
					@goToUserInfo="goToUserInfo"
					:item="item" :index="index"></user-chat-list>
				</view>
			</block>
		</scroll-view>
		
		<!-- 输入框 -->
		<user-chat-bottom @submit="submit"></user-chat-bottom>
	</view>
</template>

<script>
	import userChatBottom from '../../components/user-chat/user-chat-bottom.vue'
	import time from '../../common/time.js'
	import userChatList from '../../components/user-chat/user-chat-list.vue'
	import { mapState,mapMutations,mapGetters } from 'vuex'
	import { pushMessage, createChat, getChat, getContact,getOrder,createOrder } from '@/api/user-chat.js'
	import { acceptOrder,rejectOrder,accomplishOrder } from '@/api/platform/order.js'
	import { picUrl } from '@/api/common.js'
	import Vue from 'vue'
	import { getOrderDetail } from '@/api/order-detail.js'
	import { getNeedDetail } from '@/api/need-detail.js'
	export default {
		components:{
			userChatBottom,
			userChatList
		},
		computed:{
			...mapState(['chatList','userInfo','msgIndex','msgPage']),
			...mapGetters(['currentChatMsgs'])
		},
		data() {
			return {
				scrollTop:0,
				triggered:false,
				index:-1,
				style:{
					contentH:0,
					itemH:0
				},
				list:[],
				cId:0,
				socket:null,
				fid: undefined,
				isShow:false,
				show:false,
				need:{ need_id:0, },
				order:{
					order_id:0,
					state:undefined,
				},
				timer:null,
			}
		},
		
		onShow() {
			this.isShow = true
		},
		beforeDestroy() {
			this.isShow = false
			this.setIndex(-1)
			this.setMsgPage(1)
			this.clear()
		},
		// 监听下拉刷新
		onPullDownRefresh(){
			this.initdata()
		},
		async onLoad(data) {
			if(data.index){
				this.setIndex(parseInt(data.index))
				this.index = data.index
				
				// 设置导航栏标题：增加企业或专家真实姓名@标识
				if (this.chatList[this.msgIndex].name) {
					let titlebarName = this.chatList[this.msgIndex].username + '（' + this.chatList[this.msgIndex].name +'）'
					uni.setNavigationBarTitle({ title: titlebarName, })
				} else {
					let titlebarName = this.chatList[this.msgIndex].username 
					uni.setNavigationBarTitle({ title: titlebarName, })
				}
				// console.log(this.chatList[this.msgIndex])
				
				// 设置导航栏颜色
				uni.setNavigationBarColor({
				    frontColor: '#000000',	//前景颜色值，包括按钮、标题、状态栏的颜色
				    backgroundColor: '#fffae1',
				    animation: {
				        duration: 500,
				        timingFunc: 'easeInOut'	//动画以低速开始和结束
				    }
				})
			}
			this.fid = data.fid
			let id = parseInt(data.fid)
			let flag = true
			
			if(!data.index){
				for(let i =0;i<this.chatList.length;i++){
					if(this.chatList[i].fid === id){
						this.index = i
						this.setIndex(i)
						flag = false
						// uni.setNavigationBarTitle({ title:this.chatList[this.msgIndex].username })
						
						if (this.chatList[this.msgIndex].name) {
							let titlebarName = this.chatList[this.msgIndex].username + '（' + this.chatList[this.msgIndex].name +'）'
							uni.setNavigationBarTitle({ title: titlebarName, })
						} else {
							let titlebarName = this.chatList[this.msgIndex].username 
							uni.setNavigationBarTitle({ title: titlebarName, })
						}
						
						this.cId = this.chatList[i].id
						return
					}
				}
				if(flag){
					this.fid = id
					let chat = await createChat({
						from_user_id: this.userInfo.id,
						to_user_id:parseInt(id),
						chatroom_name:''
					})
					let ans=await getChat(chat.id,this.userInfo)
					console.log(ans)
					this.cId = chat.id
					console.log(this.cId)
					// chat.time= time.gettime.gettime(ans.afterTime)
					this.setIndex(0)
					this.index = 0
					this.addChatList(ans)
					// uni.setNavigationBarTitle({ title:ans.username })
					if (ans.name) {
						let titlebarName = ans.username + '（' + ans.name +'）'
						uni.setNavigationBarTitle({ title: titlebarName, })
					} else {
						let titlebarName = ans.username 
						uni.setNavigationBarTitle({ title: titlebarName, })
					}
				}

			}else{
				this.fid = this.chatList[data.index].fid
				this.cId = this.chatList[data.index].id
			}
			
			this.initorder()
			
		},

		onReady() {
			this.getdata()
			this.initdata()
			this.pageToBottom(true)
			this.initorder()
			this.initdata()
			//this.refresh()
		},
		
		// 监听标题栏按钮点击事件
		onNavigationBarButtonTap(e) {
			// console.log(e.index)
			switch (e.index) {
				// 右上头像按钮跳转
				case 0:
					this.goToUserInfo(this.chatList[this.msgIndex].fid)
					break
			}
		},
		
		watch:{
			currentChatMsgs(old){
				if(this.triggered){
					
				}else{
					this.pageToBottom(true)
				}
			}
		},
		methods:{
			...mapMutations(['setChatMessage',
			'setIsPaper',
			'addChatList',
			'setIndex',
			'setMsgPage',
			'addChatMessage','addNoreadMessage']),
			// 初始化参数
			async initdata(){
				try {
					const res = uni.getSystemInfoSync()
					let t = 200
					//if(this.need.need_id===0)t=120
					this.style.contentH=res.windowHeight - uni.upx2px(t)
					//console.log(this.need.need_id)
					uni.stopPullDownRefresh()
				} catch (e) { }
			},
			refresh(){
				this.timer = setInterval(() => {
				      setTimeout(this.trym, 0)
				    }, 1000*5)
			},
			createOrderAndRefresh(){
				if(this.userInfo.type === 5){	//5 = 专家
					let temp={
						enterprise_id: this.userInfo.id,
						expert_id: this.fid,
						need_id: this.need.need_id,
					}
					
					createOrder(temp)
				}else if(this.userInfo.type === 4){	//4 = 企业
					let temp={
						enterprise_id: this.fid,
						expert_id: this.userInfo.id,
						need_id: this.need.need_id,
					}
					
					createOrder(temp)
				}
				this.initorder()
				this.sendm('我已向您发起订单，需求名为：' + this.need.title)
			},
			acceptOrderAndRefresh(){
				acceptOrder(this.userInfo.id,this.order.order_id)
				this.initorder()
				this.sendm('我已接受您的订单，需求名为：'+this.need.title)
			},
			rejectOrderAndRefresh(){
				rejectOrder(this.userInfo.id,this.order.order_id)
				this.initorder()
				this.sendm('我已拒绝您的订单，需求名为：'+this.need.title)
			},
			accomplishOrderAndRefresh(){
				if(this.userInfo.type===5){
					let temp={
						enterprise_id:this.userInfo.id,
						expert_id:this.fid,
						need_id:this.need.need_id,
					}
					
					accomplishOrder(temp.enterprise_id,this.order.order_id)
				}else if(this.userInfo.type===4){
					let temp={
						enterprise_id:this.fid,
						expert_id:this.userInfo.id,
						need_id:this.need.need_id,
					}
					
					accomplishOrder(temp.enterprise_id,this.order.order_id)
				}
				
				this.initorder()
				this.sendm('我们的订单已完成，需求名为：'+this.need.title)
			},
			async initorder(){
				if(this.userInfo.type===5){
					let temp={
						enterprise_id:this.userInfo.id,
						expert_id:this.fid,
					
					}
					let temp1= await getContact(temp)
					if(temp1)
						this.need = await getNeedDetail(temp1.need_id)
					else{
						this.need={ need_id:0, }
					}
				}else if(this.userInfo.type===4){
					let temp={
						enterprise_id:this.fid,
						expert_id:this.userInfo.id,
					
					}
					let temp1= await getContact(temp)
					//console.log("order:"+!this.temp1)
					if(temp1)
						this.need = await getNeedDetail(temp1.need_id)
					else{
						this.need={ need_id:0, }
					}
					//console.log("order:"+this.need!=undefined)
				}
				
				let temp
				if(this.userInfo.type===4){
					temp={
						enterprise_id:this.fid,
						expert_id:this.userInfo.id,
						need_id:this.need.need_id,
					}
				}else{
					temp={
						enterprise_id:this.userInfo.id,
						expert_id:this.fid,
						need_id:this.need.need_id,
					}
				}
				let temp1 = await getOrder(temp)
				console.log(temp1)
				if(temp1.order_id>0){
					this.order = await getOrderDetail(temp1.order_id)
				}
				else{
					this.order.state=undefined
					this.order.order_id=0
				}
				
				//console.log("order:"+this.need && this.need.need_id!=0)
			},
			async sendm(data){
				this.submit(data)
			},
			scrollTopHandle(){
				if (this.triggered) {
					setTimeout(()=>{
						if(this.msgPage>(this.currentChatMsgs.length/20)){
							uni.showToast({
								title:'没有更多消息了!',
								icon:'none'
							})
						}
						this.triggered = false
					},200)
					return
				}
				this.triggered = true
				this.setMsgPage()
			},
			pageToBottom(isfirst = false){
				let q=uni.createSelectorQuery().in(this)
				let itemH = q.selectAll('.chat-item')
				if(this.currentChatMsgs.length!==0){
					this.$nextTick(()=>{
						itemH.fields({ size:true },data => {
							if (data) {
								if (isfirst) {
									for (let i = 0; i < data.length; i++) {
										this.style.itemH += data[i].height
									}
								}else{
									this.style.itemH += data[data.length-1].height
								}
								this.scrollTop = (this.style.itemH > this.style.contentH) ? this.style.itemH : 0
							}
						}).exec()
					})
				}
			},
			openmenu(){
				
				if(this.show){
					this.show=false
				}else{
					this.show=true
				}
			},
			clear(){
				clearInterval(this.timer) //清除计时器
				this.timer = null //设置为null
			},
			goToUserInfo(uid){
				uni.navigateTo({ url:'../../pages/user-space/user-space?uid=' + uid })
			},
			goToNeedDetail(item){
				uni.navigateTo({ url:'../need-detail/detail?id='+item })
			},
			goToOrderDetail(item){
				uni.navigateTo({ url:'../order-detail/order-detail?id='+item })
			},
			// 获取聊天数据
			getdata() {
				// 从服务器获取到的数据
				if(this.chatList.length === 0){
					return
				}
			},
			async submit(data){
				// 构建数据
				let now=new Date().getTime()
				if(data===''){
					uni.showToast({
						title:'消息不能为空',
						icon:'none'
					})
					return
				}
				let msg =await pushMessage({
					'cId': this.chatList[this.msgIndex].id,
					'fromId': this.userInfo.id,
					'toId': this.chatList[this.msgIndex].fid,
					'content': data
				}) 
				
				if(msg.code&&msg.code!==0){
					uni.showToast({
						title:'消息发送失败!',
						icon:'none'
					})
					return
				}
				let obj={
						fromId:this.userInfo.id,
						toId:this.fid,
						index:this.index,
						isme:true,
						userpic:this.userInfo.userpic,
						type:'text',
						message:data,
						time:  time.gettime.gettime(now),
						gstime: now,
						created_at:now,
					}
				this.addChatMessage(obj)
				this.pageToBottom(true)
				
			}
		}
	}
</script>

<style>

</style>
