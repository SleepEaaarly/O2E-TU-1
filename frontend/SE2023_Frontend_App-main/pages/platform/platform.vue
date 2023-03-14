<template>
	<view>
	<template v-if="userInfo&&userInfo.id&&(userInfo.type=='4'||userInfo.type=='5')">
	
		<!--(我的-发现)导航栏-->
		<swiper-tab-head :tabBars="tabBars" :tabIndex="tabIndex" @tabtap="tabtap" scrollItemStyle="width:50%;"></swiper-tab-head>
			<view v-if="tabIndex == 0">
				<view v-if="userInfo.type=='4'">
					<need-data :needdata="needdata" :userInfo="userInfo" @goToExplore="goToExplore" @goToNeedInfo="goToNeedInfo" @openOrderDetail="openOrderDetail">
					</need-data>
				</view>
				<view v-else>
					<homeInfo :homeinfo="homeinfo"></homeInfo>
					<uni-section title="需求管理" subTitle="对您的需求进行管理" type="line">	
					</uni-section>
					<uni-list>
						<view @click="manageunfinishedneed">
							<uni-list-item title="已发布需求管理" 
										   :border="false" link rightText="点击体验AI推荐"
										   showBadge="true" badge-text="hot" badgeType="error"
										   :show-extra-icon="true" :extra-icon="extraIcon_fabu"
										   >	
							</uni-list-item>
						</view>
						<view @click="manageunissuedneed"> 
							<uni-list-item title="未发布需求管理" 
										   :border="false" link 
										   :show-extra-icon="true" :extra-icon="extraIcon_weifabu"
										   >	
							</uni-list-item>
						</view>
						<view @click="managefinishedneed">
							<uni-list-item title="已完成需求管理"
										   :border="false" link
										   :show-extra-icon="true" :extra-icon="extraIcon_wancheng"
										   >	
							</uni-list-item>
						</view>
						<view>
							<uni-row class="notice">
								<text class="notice">订单信息可点击需求进行查看，也可点击“+”进入订单管理界面哦~</text>
							</uni-row>
						</view>
					</uni-list>
					
					<uni-section title="更多信息" subTitle="更多功能,敬请期待!" type="line">
					</uni-section>
					<view>
						<load-more loadtext="没有更多数据了"></load-more>
					</view>
				</view>
			</view>
		 
			<!--需求平台-发现-->
			<view v-else-if="tabIndex == 1">
				<view class="box-bg">
					<uni-nav-bar>
						<block slot="left">
							<view class="left-head">
								<view>
									<text class="uni-nav-bar-text" @click="showNeedType">{{field_items[field]}}</text>
								</view>
							</view>
						</block>
						<view class="input-view">
							<uni-icons class="input-uni-icon" type="search" size="18" color="#999" />
							<input class="nav-bar-input" placeholder="输入搜索关键词" v-model="inputText"/>
						</view>
						<block slot="right">
							<view class="right-head">
								<text @click="searchNeed" class="nav-bar-text-right">搜索</text>
							</view>
						</block>
					</uni-nav-bar>
				</view>
				
				<!-- 筛选下拉框 -->
				<uni-popup ref="popup" background-color="#fff">
					<uni-list>
						<uni-list-item v-for="(item, index) in field_items" 
						:key="item" :title="item" @click="changeNeedType(index)" clickable></uni-list-item>
					</uni-list>
				</uni-popup>
				
				<view v-if="items_show">
					<view v-for="(item, index) in items_classified" :key="index">
						<need-list :item="item" :index="index" @openDetail="openDetail">
						</need-list>
					</view>
				</view>
				<view v-else-if="items_classified.length === 0">
					<load-more loadtext="没有更多数据了"></load-more>
				</view>
				<view v-else>
					<load-more loadtext="没有更多数据了"></load-more>
				</view>
			</view>
			
			<!-- 未登录状态 -->
			
		<!--右上角创建需求-->
		<platform-create v-if="userInfo.type=='5'" :show="show" @hide="hidepopup" @addneed="addneed" @manageorder="manageorder"></platform-create>
	</template>
	<template v-else-if="!userInfo.id">
		<view class="u-f-ajc">
			登陆PaperDaily，体验更多功能
		</view>
		<view class="u-f-ajc" @tap="openLogin">
			账号密码登陆 
			<view class="icon iconfont icon-jinru"></view>
		</view>
	</template>
	<template v-else>
		<view class="u-f-ajc">
			请先进行企业或专家认证
		</view>
	</template>
	
	<w-loading text="搬运数据中.." mask="true" click="true" ref="loading"></w-loading>
	</view>
</template>

<script>
	import needList from '@/components/platform/need-list.vue'
	import needData from '@/components/platform/need-data.vue'
	import swiperTabHead from '@/components/index/swiper-tab-head.vue'
	import myNavBarNeed from '@/components/common/my-nav-bar-need.vue'
	import homeInfo from '@/components/home/home-info-2'
	import card from '@/components/list-card/list-card-1.vue'
	import loadMore from '@/components/common/load-more.vue'
	import time from '@/common/time.js'
	import noThing from '@/components/common/no-thing.vue'
	import uniSwipeAction from '@/components/uni-swipe-action/uni-swipe-action.vue'
	import uniSwipeActionItem from '@/components/uni-swipe-action-item/uni-swipe-action-item.vue'
	import platformCreate from '@/components/platform/platform-create.vue'
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniPopup from '@/components/uni_popup_modules/uni-popup/components/uni-popup/uni-popup.vue'
	import wLoading from '@/components/w-loading/w-loading.vue'	// 加载动画
	import {
		getAllNeed,
		postNewNeed
	} from '@/api/platform.js'
	import { mapState } from 'vuex'
	import { getUserProfile, } from '@/api/home.js'
	import Vue from 'vue'
	import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue'
	import uniDataSelect from '@/components/uni-data-select/components/uni-data-select/uni-data-select.vue'
	import { searchNeedList } from '@/api/search.js'
	export default {
		components: {
			needList,
			needData,
			homeInfo,
			swiperTabHead,
			loadMore,
			noThing,
			myNavBarNeed,
			card,
			uniCol,
			uniRow,
			platformCreate,
			uniNavBar,
			uniDataSelect,
			uniPopup,
			wLoading
		},
		computed: { 
			items_classified:  {
				get: 	function() {
							if(this.field !== this.field_items.length) {
								let val = []
								for(let item of this.items) {
									if(item.field === this.field) {
										val.push(item)
									}
								}
								return val.length === 0 ? this.items : val
							} else {
								return this.items
							}
						},
				set:    function(newValue) {
							if (newValue.length === 0) {
								this.items_show = false
							} else {
								this.items_show = true
							}
						}
			},
			...mapState(['userInfo']) 
		},
		
		
		watch: {
			field: function(newValue) {
				let that = this
				var f = function(that) {
					if(newValue !== that.field_items.length - 2) {
						let val = []
						for(let item of that.items) {
							if(item.field === newValue) {
								val.push(item)
							}
						}
						console.log(val.length)
						that.items_classified = val
					} else {
						that.items_classified = that.items
					}
				}
				f(that)
			}
		},
		data() {
			return {
				swiperheight: 500,
				islogin: false,
				tabIndex: 0,
				needRefresh: true,
				shoNo: false,
				items: [],
				items_show:true,
				field: 9,
				inputText: '',
				show: false,
				refreshing: false,
				homeinfo: () => {},
				tabBars: [{
						name: '我的',
						id: 'wode',
						page: 1
					},
					{
						name: '发现',
						id: 'faxian',
						page: 1
					},
				],
				needdata:[
					{ name:'全部', num:0 },
					{ name:'待处理', num:0 },
					{ name:'进行中', num:0 },
					{ name:'已完成', num:0 },
				],
				// 三个Icon格式
				extraIcon_fabu: {
					color: '#27a4da',
					size: '20',
					type: 'paperplane-filled'
				},
				extraIcon_weifabu: {
					color: '#27a4da',
					size: '20',
					type: 'locked-filled'
				},
				extraIcon_wancheng: {
					color: '#27a4da',
					size: '20',
					type: 'flag-filled'
				},
				field_items: [
					'信息技术', '装备制造', '新材料', '新能源', '节能环保', '生物医药', '科学创意', '检验检测', '其他', 'ALL', 'Test'
				],
			}
		},
		
		onLoad() {
			// console.log(this.userInfo.enterprise_name)
			//this.tabIndex=1
			if (this.userInfo.type === 4) {
				this.tabBars[0].name = '订单'
			} else {
				this.tabBars[0].name = '我的'
			}
			this.homeinfo = this.userInfo
			uni.getSystemInfo({
				success: res => {
					let height = res.windowHeight - uni.upx2px(100)
					this.swiperheight = height
				}
			})
			if (this.userInfo.type === 5 || this.userInfo.type === 4) {
				this.requestData()
			}
		},
		
		onShow() {
			
			if (this.userInfo.type === 4) {
				this.tabIndex=1
				this.tabBars[0].name = '订单'
			} else {
				this.tabBars[0].name = '我的'
			}
			this.homeinfo = this.userInfo
			if (this.userInfo.type === 5 || this.userInfo.type === 4) {
				this.requestData()
			}
		},
		
		// 监听导航按钮点击事件
		onNavigationBarButtonTap(e) {
			if (!this.userInfo.id) {
				uni.navigateTo({ url: '../login/login', })
			}
		},
		
		onPullDownRefresh() {
			this.onrefresh()
			uni.stopPullDownRefresh()
		},
		
		methods: {
			//获取需求数据
			async requestData(GoPage, Gotype) {
				
				let type = this.tabBars[this.tabIndex].id
				try {
					if(this.tabIndex === 1){
						if (this.needRefresh) {
							// this.$refs.loading.open()
						}
						let that = this
						let items = await getAllNeed()
						// setTimeout(function() {
						// 	that.$refs.loading.close()
						// 	that.needRefresh = false
						// }, 500)
						this.items = items
					}
				} catch (e) {
					console.log(e)
					return
				}
			},
			openLogin() {
				uni.navigateTo({ url: '../login/login' })
			},
			openDetail(item) {
				//console.log("-----------------------------------openDetail")
				console.log(item.need_id)
				uni.navigateTo({ url: '../need-detail/detail?id=' + item.need_id })
			},
			openOrderDetail(order_id) {
				uni.navigateTo({ url: '../order-detail/order-detail?id=' + order_id })
			},
			async onrefresh() {
				if (this.refreshing) return
				this.refreshing = true
				// this.$refs.loading.open()
				await this.requestData()
			},
			tabtap(index) {
				this.tabIndex = index
				this.requestData()
			},
			// 滑动事件
			tabChange(e) {
				this.tabIndex = e.detail.current
				this.requestData(this.tabBars[this.tabIndex].page, this.tabBars[this.tabIndex].id)
			},
			initNavigation(e) {
				this.opcity = e.opcity
				this.top = e.top
			},
			hidepopup() {
				this.show = false
			},
			showpopup() {
				this.show = true
			},
			addneed() {
				uni.navigateTo({ url: '../add-need/need' })
				this.hidepopup()
			},
			manageorder() {
				uni.navigateTo({ url: '../manage-order/manage-order' })
				// this.hidepopup()
			},
			managefinishedneed() {
				uni.navigateTo({ url: '../manage-need/managefinishedneed' })
				// this.hidepopup()
			},
			manageunfinishedneed() {
				uni.navigateTo({ url:'../manage-need/manageunfinishedneed' })
				// this.hidepopup()
			},
			manageunissuedneed() {
				uni.navigateTo({ url:'../manage-need/manageunissuedneed' })
				// this.hidepopup()
			},
			async searchNeed() {
				this.needRefresh = true
				if (this.inputText) {
					console.log(this.inputText)
					let data = await searchNeedList(this.inputText)
					this.items = data
					// this.$refs.loading.open()
					// let that = this
					// setTimeout(function() {
					// 	that.$refs.loading.close()
					// }, 500)
				} else {
					this.requestData()
					// this.$refs.loading.open()
					// let that = this
					// setTimeout(function() {
					// 	that.$refs.loading.close()
					// }, 500)
				}
				let that = this
				that.needRefresh = false
			},
			showNeedType() {
				this.$refs.popup.open('bottom')
			},
			
			changeNeedType(value) {
				this.$refs.popup.close()
				this.field = value
				this.needRefresh = true
				this.requestData()
				console.log(this.field)
			},
			
			async mounted() {
				this.initDat()
				if (this.userInfo.id) {
					if (!this.islogin) {
						this.initDat()
					}
				} else {
					this.needdata[0].num = 0
					this.needdata[1].num = 0
					this.needdata[2].num = 0
					this.islogin = false
				}
			},
			async initDat() {
				if (this.userInfo && this.userInfo.id) {
					let userProfile = await getUserProfile()
					console.log(userProfile)
					this.needdata[0].num = userProfile.total_post
					this.needdata[1].num = userProfile.total_comment
					this.needdata[2].num = userProfile.total_mycollect
					this.islogin = true
				}
			},

			//跳转到各种类订单list
			goToNeedInfo(index) {
				console.log(index)
				switch (index) {
					case 0:
						console.log(this.userInfo)
						uni.navigateTo({ url: '../user-space/user-space?uid=' + this.userInfo.id })
						break
					case 1:
						uni.navigateTo({ url: '../user-comment/user-comment?uid=' + this.userInfo.id })
						break
					case 2:
						uni.navigateTo({ url: '../user-collect/user-collect?uid=' + this.userInfo.id })
						break
				}
			},
			//去逛逛
			goToExplore(){
				console.log('tabindex change to 1.')
				this.tabIndex = 1
			},
			//跳转到“最近评价”
			naviToMyevaluations(){
				uni.navigateTo({ url: '../my-evaluations/my-evaluations?id='+this.userInfo.id })
				console.log('To Myevaluations.')
			},
			//跳转到“我的反馈”
			naviToMyfeedbacks(){
				uni.navigateTo({ url: '../my-feedbacks/my-feedbacks' })
			},
		}
	}
</script>

<style>	/* 什么破玩意？？加lang="scss"会让搜索框文字错位 */
/* 隐藏scroll-view滚动条 */
::-webkit-scrollbar {
	width: 0;
	height: 0;
	color: transparent;
}
/* need数据的style样式 */
.need-statistic-data{
	background: #FFFFFF;
	position: relative;
	z-index: 10;
	border-top-left-radius: 20upx;
	border-top-right-radius: 20upx;
	margin-top: -15upx;
}
.info {
	height:80upx;
	text-align: center;
	box-shadow: 0 0 1upx rgba(0, 0, 0, .12), 1upx 0 0 rgba(0, 0, 0, .04)
}
.info-text {
	text-decoration: blink;
}
.notice {
	font-size: x-small;
	font-weight: 100;
	float: right;
	margin-top: 20upx;
}
$nav-height: 30px;

.box-bg {
	background-color: #F5F5F5;
	padding: 5px 0;
}

.left-head {
	flex-direction: row;
	align-items: center;
	justify-content: flex-start;
	width: 160rpx;
	margin-left: 4px;
	padding-top: 18upx;
}
.uni-nav-bar-text {
	font-size: 20upx;
	padding-left: 0upx;
	text-decoration: underline;
}
.right-head {
	flex-direction: row;
	align-items: center;
	justify-content: flex-start;
	width: 160rpx;
	margin-left: 4px;
	padding-top: 18upx;
}
.nav-bar-text-right {
	padding-left: 0upx;
	font-size: 20upx;
}

.input-view {
	/* #ifndef APP-PLUS-NVUE */
	display: flex;
	/* #endif */
	flex-direction: row;
	background-color: #f8f8f8;
	height: $nav-height;
	border-radius: 15px;
	padding: 0 15px;
	flex-wrap: nowrap;
	margin: 7px 0;
	line-height: $nav-height;
}

.input-uni-icon {
	line-height: $nav-height;
}

.nav-bar-input {
	height: $nav-height;
	line-height: $nav-height;
	/* #ifdef APP-PLUS-NVUE */
	/* #endif */
	padding-top: 15upx;
	padding-left: 5upx;
	font-size: 12px;
	background-color: #f8f8f8;
}

</style>