<template>
	<view>
	<template v-if="userInfo&&userInfo.id">
		
		<!--导航栏-->
		<swiper-tab-head :tabBars="tabBars" :tabIndex="tabIndex" @tabtap="tabtap" scrollItemStyle="width:33%;"></swiper-tab-head>
		<scroll-view
		 scroll-y class="list">
			<!--搜索框-->
			<view v-if="tabIndex === 1 ">
				<view v-for="(item, index) in unfinisheditems" :key="index">
					<need-list :item="item" :index="index" :showExpert="resolveIndex === index && tabIndex === 1" :expertList="resolveIndex === index && tabIndex === 1 ? expertList : []"
					@goToRecommend="goToRecommend(arguments)" @openDetail="openDetail" :edit="1" @contact="contact(arguments)"
					@editneed="editneed" @deleteneed="deleteneed" @endneed="endneed">
					</need-list>
				</view>
			</view>
			
			<view v-else-if="tabIndex === 2 ">
				<view v-for="(item, index) in unissueditems" :key="index">
					<need-list :item="item" :index="index" :showExpert="resolveIndex === index && tabIndex === 2" :expertList="resolveIndex === index && tabIndex === 2 ? expertList : []"
					@goToRecommend="goToRecommend(arguments)" @openDetail="openDetail" :edit="2" @contact="contact(arguments)"
					@editneed="editneed" @deleteneed="deleteneed" @issue="issue">
					</need-list>
				</view>
			</view>
			
			<!-- 需求订单统计 -->
			<view v-else-if="tabIndex === 0" >
				<view v-for="(item, index) in finisheditems" :key="index">
					<need-list :item="item" :index="index" @openDetail="openDetail">
					</need-list>
				</view>
			</view>
			<template v-else>
				<view class="u-f-ajc">
					登陆PaperDaily，体验更多功能
				</view>
				<view class="u-f-ajc" @tap="openLogin">
					账号密码登陆 
					<view class="icon iconfont icon-jinru">
						
					</view>
				</view>
			</template>
		</scroll-view>
		
		<view>
			<!-- 提示窗示例 -->
			<uni-popup ref="alertDialog" type="dialog">
				<uni-popup-dialog :type="msgType" confirmText="同意" cancelText="关闭" title="提示" :content="msg" @confirm="dialogConfirm(msgType)"
					@close="dialogClose"></uni-popup-dialog>
			</uni-popup>
		</view>
	</template>
	</view>
</template>

<script>
	import needList from '@/components/platform/need-list.vue'
	import needData from '@/components/platform/need-data.vue'
	import swiperTabHead from '@/components/index/swiper-tab-head.vue'
	import myNavBar from '@/components/common/my-nav-bar.vue'
	import uniCalendar from '@/components/uni-calendar/uni-calendar.vue'
	import card from '@/components/list-card/list-card-1.vue'
	import loadMore from '@/components/common/load-more.vue'
	import time from '@/common/time.js'
	import noThing from '@/components/common/no-thing.vue'
	import uniSwipeAction from '@/components/uni-swipe-action/uni-swipe-action.vue'
	import uniSwipeActionItem from '@/components/uni-swipe-action-item/uni-swipe-action-item.vue'
	import platformCreate from '@/components/platform/platform-create.vue'
	import uniPopup from '@/components/uni_popup_modules/uni-popup/components/uni-popup/uni-popup.vue'
	import uniPopupDialog from '@/components/uni_popup_modules/uni-popup/components/uni-popup-dialog/uni-popup-dialog.vue'
	import { mapState } from 'vuex'
	import { getUserProfile, } from '@/api/home.js'
	import {
		manageFinishedNeed,
		manageUnfinishedNeed,
		manageUnissuedNeed,
		deleteNeed,
		endNeed,
		expertRecommend,
		transformNeed
	} from '@/api/manage-need.js'
	import { createContact } from '@/api/need-detail.js'
	import Vue from 'vue'
	export default {
		components: {
			needList,
			needData,
			swiperTabHead,
			loadMore,
			noThing,
			myNavBar,
			card,
			platformCreate,
			uniPopup,
			uniPopupDialog
		},
		computed: { ...mapState(['userInfo']) },
		data() {
			return {
				islogin: false,
				swiperheight: 500,
				tabIndex: 0,
				shoNo: false,
				unfinisheditems: [],
				finisheditems: [],
				unissueditems: [],
				show: false,
				refreshing: false,
				msg: '',
				msgType: 'success',
				resolveId: '',
				resolveIndex: -1,
				expertList: [],
				tabBars: [{
						name: '已完成',
						id: 'wode',
						page: 1
					},
					{
						name: '未完成',
						id: 'faxian',
						page: 1
					},
					{
						name: '未发布',
						id: 'weifabu',
						page: 1
					}
				],
				
			}
		},
		
		onLoad() {
			console.log(this.userInfo)
			uni.getSystemInfo({
				success: res => {
					let height = res.windowHeight - uni.upx2px(100)
					this.swiperheight = height
				}
			})
			console.log('-------------------Requesting')
			this.msg = ''
			this.requestData()
			console.log('-------------------Request Success')
		},
		
		onShow() {
			console.log(this.userInfo)
			console.log('-------------------Requesting')
			this.requestData()
			console.log('-------------------Request Success')
		},
		
		// 监听导航按钮点击事件
		onNavigationBarButtonTap(e) {
			if (!this.userInfo.id) {
				uni.navigateTo({ url: '../login/login', })
			}
			switch (e.index) {
				case 0:
					this.show = true
					break
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
						let unfinisheditems = await manageUnfinishedNeed(this.userInfo.id)
						this.unfinisheditems = unfinisheditems
					} else if (this.tabIndex === 0){
						let finisheditems = await manageFinishedNeed(this.userInfo.id)
						this.finisheditems = finisheditems
					} else {
						let unissueditems = await manageUnissuedNeed(this.userInfo.id)
						this.unissueditems = unissueditems
						console.log(this.unissueditems.length)
					}
					// console.log(items)
				} catch (e) {
					console.log(e)
					return
				}
			},
			openLogin() {
				uni.navigateTo({ url: '../login/login' })
			},
			openDetail(item) {
				console.log('-----------------------------------openDetail')
				uni.navigateTo({ url: '../need-detail/detail?id=' + item.need_id })
			},
			editneed(item) {
				console.log('------------------------------------rewrite need')
				uni.navigateTo({ url: '../edit-need/edit-need?id=' + item.need_id })
			},
			deleteneed(item) {
				this.msgType = 'error'
				this.resolveId = item.need_id
				this.msg = '确认删除需求吗？此操作无法复原'
				this.$refs.alertDialog.open()
				console.log('------------------------------------ready to delete need')
			},
			endneed(item) {
				this.msgType = 'warn'
				this.resolveId = item.need_id
				this.msg = '确认结束需求吗？此操作无法复原'
				this.$refs.alertDialog.open()
				console.log('------------------------------------ready to end need')
			},
			async issue(item) {
				console.log('issue')
				try {
					let result = await transformNeed(this.userInfo.id, item.need_id)
				} catch (e) {
					console.log(e)
					return 
				}
				this.onrefresh()
			},
			goToRecommend(msg) {
				let item = msg[0]
				let index = msg[1]
				this.recommend(item, index)
				// console.log("length is " + result.length)
				// if (!(result&& result.code)) {
				// 	this.expertList = result.data
				// 	// console.log(this.expertList.length)
				// 	if (this.resolveIndex === index) {
				// 		this.resolveIndex = -1
				// 	} else {
				// 		this.resolveIndex = index
				// 	}
				// 	// console.log("father is:" + this.expertList.length)
				// }
			},
			contact(msg) {
				console.log(msg[0] + ' ' + msg[1])
				this.contactExpert(msg[0], msg[1])
			},
			dialogConfirm(type) {
				console.log('点击确认')
				// this.messageText = `点击确认了 ${this.msgType} 窗口`
				// this.$refs.message.open()
				if (type === 'warn') {
					this.end()
				} else if (type === 'error') {
					this.delete()
				}
			},
			async end() {
				if (this.resolveId) {
					try {
						let result = await endNeed(this.userInfo.id, this.resolveId)
					} catch (e) {
						console.log(e)
						return
					}
				}
				this.onrefresh()
			},
			async delete() {
				if (this.resolveId) {
					try {
						let result = await deleteNeed(this.userInfo.id, this.resolveId)
					} catch (e) {
						console.log(e)
						return
					}
				}
				this.onrefresh()
			},
			async recommend(item, index) {
				let id = item.need_id
				try {
					let result = await expertRecommend(id)
					this.expertList = result.data
					// console.log(this.expertList.length)
					// console.log(this.expertList[0].id)
					console.log(this.tabIndex)
					if (this.resolveIndex === index) {
						this.resolveIndex = -1
					} else {
						this.resolveIndex = index
					}
					console.log(this.resolveIndex)
					// return result
				} catch (e) {
					console.log(e)
					return
				}
			},
			dialogClose() {
				console.log('点击关闭')
			},
			async onrefresh() {
				if (this.refreshing) return
				this.refreshing = true
				await this.requestData()
				setTimeout(() => {
					this.refreshing = false
					uni.showToast({ title:'已更新',duration:500 })
				}, 200)
			},
			tabtap(index) {
				console.log('change index to ' + index)
				this.tabIndex = index
				this.resolveIndex = -1
				this.requestData(this.tabBars[this.tabIndex].page, this.tabBars[this.tabIndex].id)
			},
			// 滑动事件
			tabChange(e) {
				this.tabIndex = e.detail.current
				this.resolveIndex = -1
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
			contactExpert(item, expert){
				let temp={
					expert_id:expert.expert_id,
					enterprise_id:this.userInfo.id,
					need_id:item.need_id,
				}
				let s =createContact(temp)
				console.log(temp)
				uni.navigateTo({ url:'../user-chat/user-chat?fid='+expert.expert_id })
			},
		}
	}
</script>

<style>
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
</style>
