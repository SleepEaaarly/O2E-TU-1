<template>
	<view class="detail">
		<uni-row class="header">
			<uni-col :span="9" class="image">
				<image src="../../static/bgimg/need_contracted.jpg" mode="widthFix" lazy-load class="image-image"></image>
			</uni-col>
			<uni-col :span="14" :offset="1" class="title-info">
				<uni-row class="need-title">
					<text class="need-title">{{item.title}}</text>
				</uni-row>
				<uni-row class="need-info">
					<uni-row :span="14" class="need-info-item">
						<uni-icons type="fire" size="18"></uni-icons>
						<text class="need-info-text">领域：{{field_items[item.field]}}</text>
					</uni-row>
					<uni-row :span="14" class="need-info-item">
						<uni-icons type="gear" size="18"></uni-icons>
						<text class="need-info-text">关键词：</text>
						<text class="need-info-text-detail">{{item.key_word}}</text>
					</uni-row>
					<uni-row :span="14" class="need-info-item">
						<uni-icons type="home" size="18"></uni-icons>
						<text class="need-info-text">企业信息：</text>
						<text class="need-info-text-detail">{{item.enterprise_name}}</text>
					</uni-row>
				</uni-row>
			</uni-col>
		</uni-row>
		<uni-row class="need-header">
			<uni-section title="Introduction" subTitle="需求说明" type="line">
			</uni-section>
		</uni-row>
		<uni-row class="need-introduction">
			<uni-col :span="14" :offset="1">
				<uni-icons type="location" size="18"></uni-icons>
				<text class="need-introduction-text">地址：{{item.address}}</text>
			</uni-col>
			<uni-col :span="8" :offset="1">
				<uni-icons type="cart" size="18"></uni-icons>
				<text class="need-introduction-text">经费：￥{{item.money}}万</text>
			</uni-col>
		</uni-row>
		<uni-row class="need-introduction">
			<uni-col :span="23" :offset="1">
				<uni-icons type="calendar" size="18"></uni-icons>
				<text class="need-introduction-text">开始日期：{{item.start_time}}</text>
			</uni-col>
		</uni-row>
		<uni-row class="need-introduction">
			<uni-col :span="23" :offset="1">
				<uni-icons type="calendar" size="18"></uni-icons>
				<text class="need-introduction-text">截止日期：{{item.end_time}}</text>
			</uni-col>
		</uni-row>
		<uni-row class="need-header">
			<uni-section title="Description" subTitle="需求描述" type="line">
				
			</uni-section>
		</uni-row>
		<uni-row class="need-description">
			<text class="need-description">{{item.description}}</text>
		</uni-row>
		
		<uni-row class="need-after">
			<uni-section title="Contributors" subTitle="订单信息" type="line">
			</uni-section>
		</uni-row>
		
		<uni-row class="need-contributors">
			<uni-list>
				<view v-if="orderlist.length === 0" class="load-text">
					<load-more loadtext="暂时没有订单信息~"></load-more>
				</view>
				<view v-else>
					<view v-for="(orderdetail,index) in orderlist" :key="index" @click="gotoSpace(orderdetail)">
						<uni-list-item :thumb="orderdetail.expertPic" :title="orderdetail.expert_name" :rightText="orderdetail.state" >
						</uni-list-item>
					</view>
					<view class="load-text">
						<load-more loadtext="没有更多信息了~"></load-more>
					</view>
				</view>
			</uni-list>
		</uni-row>
		
		<uni-row class="fix-button">
			<view v-if="userInfo.type==4&&order.order_id==0">
				<uni-col :span="8">
					<button type="primary" @click="goToEnterpriseSpace" class="fix-button-left">企业详情</button>
				</uni-col>
				<uni-col :span="8" :offset="8">
					<button type="primary" @click="contact" class="fix-button-right">立即对接</button>
				</uni-col>
			</view>
		</uni-row>
	</view>
</template>

<script>
	import {
		mapState,
		mapMutations
	} from 'vuex'
	import {
		getNeedDetail,
		createContact
	} from '@/api/need-detail.js'
	import tuiCard from '@/components/thorui/tui-card/tui-card.vue'
	import tuiListView from '@/components/thorui/tui-list-view/tui-list-view'
	import tuiListCell from '@/components/thorui/tui-list-cell/tui-list-cell'
	import loadMore from '@/components/common/load-more.vue'
	import { getOrder } from '@/api/user-chat.js'
	import {
		getOrderDetail,
		needToOrderlist,
	} from '@/api/order-detail.js'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import uniSection from '@/components/uni-section/uni-section.vue'
	import uniCard from '@/components/uni-card/uni-card.vue'
	import uniCollapseItem from '@/components/uni-collapse-item/uni-collapse-item.vue'
	import uniCollapse from '@/components/uni-collapse/uni-collapse.vue'
	import { picUrl } from '@/api/common.js'
	// import { getUserProfile } from '@/api/home.js'
	import { getUserInfo } from '@/api/user-space.js'
	var graceRichText = require('../../components/common/richText.js')
	export default {
		components: {
			tuiCard,
			tuiListView,
			tuiListCell,
			uniCol,
			uniRow,
			uniSection,
			uniCard,
			loadMore
		},
		data() {
			return {
				order:{
					order_id:0,
					state:-1,
				},
				field_items: [
					'信息技术', '装备制造', '新材料', '新能源', '节能环保', '生物医药', '科学创意', '检验检测', '其他'
				],
				emergencyItems: [
					{
						value: '0',
						name: '低'
					},
					{
						value: '1',
						name: '中'
					},
					{
						value: '2',
						name: '高'
					}
				],
				item: [],
				orderlist:[],
				sum:0,
				detail: { id: 10 },
				sponsor: {},
			}
		},
		onLoad(data) {
			console.log('data should be:' + data + ' and id should be:' + data.id)
			this.initData(data.id)
		},
		onShow(){
			// console.log(this.detail.id)
			// this.initData(this.detail.id)
			// oyk: 这里不能使用detail.id。因为会自动为其默认值，使用nextTick保存对item的更新
			this.initData(this.item.need_id)
		},
		// watch:{
		// 	orderlist(val){
				
		// 	},
		// },
		// 监听导航右边按钮
		onNavigationBarButtonTap(e) {
			
		},
		computed: { ...mapState(['userInfo']) },
		methods: {
			//初始化数据
			async initData(id) {
				if (!id) {
					console.log('error!')
					return 
				}
				uni.setNavigationBarTitle({ title: '需求详情' })
				console.log('the id is ' + id)
				let detail = await getNeedDetail(id)
				this.item = detail
				this.detail.id = detail.need_id
				this.$nextTick(()=>{
					this.item = detail
				})
				if (this.item) {
					this.getOrderList()
				}
			},
			async getOrderList() {
				// this.detail.id = detail.need_id
				// console.log("the detail-need-id is " + detail.need_id)
				console.log(this.detail.id)
				let temp = {}
				if(this.userInfo.type===4){
					temp={
						enterprise_id:this.item.enterprise_id,
						expert_id:this.userInfo.id,
						need_id:this.item.need_id,
					}
					let temp1 = await getOrder(temp)
					//console.log(this.item.need_id)
					if(temp1){
						let temp2 = await getOrderDetail(temp1.order_id)
						if(temp2.order_id){
							this.order = temp2
						}
					}
				}
				
				// let result = await needToOrderlist(this.item.need_id)
				let result = this.item.order
				if(result && result.length){
					let i = 0
					let temparray=[]
					for(i;i<result.length;i++){
						// let orderdetail = await getOrderDetail(result[i])
						// let expertdetail = await getUserInfo({ 'user_id':orderdetail.expert_id})
						// console.log(orderdetail.expert_id)
						// console.log(expertdetail.userpic)
						let orderdetail = {
expertPic: result[i].expert_icon,
											state: result[i].order_state,
											order_id: result[i].order_id,
											expert_id: result[i].expert_id,
											expert_name: result[i].expert_name,
											enterprise_id: result[i].enterprise_id
										}
						if(orderdetail.state===0){
							orderdetail.state='订单待接受'
						}
						else if(orderdetail.state===1){
							orderdetail.state='订单进行中'
						}
						else if(orderdetail.state===3){
							orderdetail.state='订单已完成'
						}
						temparray.push(orderdetail)
						//console.log(orderdetail.expertPic)
					}
					this.orderlist = temparray
					this.sum = i+1
					//console.log(this.orderlist[0])
				}
			},
			
			formatRichText (html) {
				// 去掉img标签里的style、width、height属性
				let newContent= html.replace(/<img[^>]*>/gi,function(match,capture){
					match = match.replace(/style="[^"]+"/gi, '').replace(/style='[^']+'/gi, '')
					match = match.replace(/width="[^"]+"/gi, '').replace(/width='[^']+'/gi, '')
					match = match.replace(/height="[^"]+"/gi, '').replace(/height='[^']+'/gi, '')
					return match
				})
				// 修改所有style里的width属性为max-width:100%
				newContent = newContent.replace(/style="[^"]+"/gi,function(match,capture){
					match = match.replace(/width:[^;]+;/gi, 'max-width:100%;').replace(/width:[^;]+;/gi, 'max-width:100%;')
					return match
				})
				// 去掉<br/>标签
				newContent = newContent.replace(/<br[^>]*\/>/gi, '')
				// img标签添加style属性：max-width:100%;height:auto
				newContent = newContent.replace(/\<img/gi, '<img style="max-width:100%;height:auto;display:block;margin:0px auto;"')
				return newContent
			},
			contact(){
				let temp={
					enterprise_id:this.item.enterprise_id,
					expert_id:this.userInfo.id,
					need_id:this.item.need_id,
				}
				let s =createContact(temp)
				console.log(temp)
				uni.navigateTo({ url:'../user-chat/user-chat?fid='+this.item.enterprise_id })
			},
			gotoSpace(orderdetail){
				console.log(orderdetail.enterprise_id)
				console.log(this.userInfo.id)
				console.log(orderdetail.expert_id)
				console.log(this.userInfo.id)
			
				if(orderdetail.enterprise_id === this.userInfo.id || orderdetail.expert_id === this.userInfo.id){
					uni.navigateTo({ url:'../order-detail/order-detail?id='+orderdetail.order_id })
				}else{
					uni.navigateTo({ url:'../user-space/user-space?uid='+orderdetail.expert_id })
				}
			},
			goToEnterpriseSpace() {
				uni.navigateTo({ url:'../user-space/user-space?uid='+this.item.enterprise_id })
			}
		}
	}
</script>

<style>
	.detail {
		min-height: 1380upx;
		background-color: #F1F1F1;
		padding: 10upx;
	}
	.header {
		margin: 10upx;
		background-color: white;
		border: solid #F5FFF0 2upx;
		height: 17%;
	}
	.image-image {
		padding-top: 5%;
		width:100%;
	}
	.title-info {
		
	}
	.need-title {
		font-size: 35upx;
		font-weight: bold;
		color: skyblue;
		overflow: hidden;
		width: 400rpx !important;
	    overflow: unset;
	    word-break: break-all;
	    text-overflow: ellipsis;
	    display: -webkit-box;
	   -webkit-box-orient: horizontal;
	   -webkit-line-clamp: 2;
	   white-space: nowrap;
	}
	/* .need-info {
		padding-top: 10upx;
	} */
	/* .need-info-item {
		height: 50upx;
	} */
	.need-info-text {
		font-weight: 100;
		font-size: 20upx;
	}
	.need-info-text-detail {
		font-weight: 100;
		font-size: 20upx;
		color: blue;
		height: 10upx;
	}
	.need-header {
	}
	.need-introduction {
		max-height: 150upx;
		opacity: 0.8;
		background-color: #FFFFFD;
		margin-top: 10upx;
	}
	.need-description {
		margin: 10upx;
		padding-left: 10upx;
		min-height: 200upx;
		background-color: #FFFFFD;
		font-family: 'SimHei';
		font-size: 30upx;
	}
	.need-contributors {
		margin-bottom: 15%;
		/* display: flex; */
		z-index: 1;
	}
	.load-text {
		bottom: 30upx;
		padding-bottom: ;
	}
	.fix-button {
		background-color: white;
		position: fixed;
		bottom: 0upx;
		/* right: 10upx; */
		width: 100%;
		height: 120upx;
		z-index: 2;
	}
	.fix-button-left {
		margin: 25upx;
		font-size: 30upx;
		/* float: left; */
		left: 10upx;
		background-color: orange;
		/* float: left; */
	}
	.fix-button-right {
		margin: 25upx;
		font-size: 30upx;
		right : 10upx;
		/* float: right; */
	}
</style>
