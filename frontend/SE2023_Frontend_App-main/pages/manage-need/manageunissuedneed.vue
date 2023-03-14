<template>
	<view>
		<template v-if="userInfo&&userInfo.id">
			<!--导航栏-->
				<view v-if="unissueditems.length">
					<view v-for="(item, index) in unissueditems" :key="index">
						<need-list :item="item" :index="index" :showExpert="false" :expertList="[]"
						@goToRecommend="goToRecommend(arguments)" @openDetail="openDetail" :edit="2" :manage="true" @contact="contact(arguments)"
						@editneed="editneed" @deleteneed="deleteneed" @issue="issue">
						</need-list>
					</view>
				</view>
				<view v-else>
					<no-thing></no-thing>
				</view>
			<view>
				<!-- 提示窗示例 -->
				<uni-popup ref="alertDialog" type="dialog">
					<uni-popup-dialog :type="msgType" confirmText="同意" cancelText="关闭" title="提示" :content="msg" @confirm="dialogConfirm(msgType)"
						@close="dialogClose"></uni-popup-dialog>
				</uni-popup>
			</view>
		</template>
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
		<w-loading text="搬运数据中.." mask="true" click="true" ref="loading"></w-loading>
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
	import wLoading from '@/components/w-loading/w-loading.vue'	// 加载动画
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
			uniPopupDialog,
			wLoading
		},
		computed: { ...mapState(['userInfo']) },
		data() {
			return {
				islogin: false,
				swiperheight: 500,
				tabIndex: 2,
				shoNo: false,
				unissueditems: [],
				show: false,
				refreshing: false,
				msg: '',
				msgType: 'success',
				resolveId: '',
				resolveIndex: -1,
				expertList: [],
			}
		},
		
		onLoad() {
			this.requestData()
		},
		
		onShow() {	// 无语子，之前不行是因为写成onshow了
			// this.unissueditems = []
			this.requestData()
		},
		
		onReady() {
			// this.$refs.loading.open()
		},
		
		onPullDownRefresh() {
			this.onrefresh()
			uni.stopPullDownRefresh()
		},
		
		methods: {
			//获取需求数据
			async requestData(GoPage, Gotype) {
				try {
					let unissueditems = await manageUnissuedNeed(this.userInfo.id)
					this.unissueditems = unissueditems
					console.log(this.unissueditems.length)
						
					// console.log(items)
				} catch (e) {
					console.log(e)
					return
				}
				// let that = this
				// setTimeout(function() {
				// 		that.$refs.loading.close()
				// }, 500)
			},
			openLogin() {
				uni.navigateTo({ url: '../login/login' })
			},
			openDetail(item) {
				uni.navigateTo({ url: '../need-detail/detail?id=' + item.need_id })
			},
			editneed(item) {
				console.log('跳转到edit-need')
				uni.navigateTo({ url: '../edit-need/edit-need?id=' + item.need_id })
			},
			deleteneed(item) {
				this.msgType = 'error'
				this.resolveId = item.need_id
				this.msg = '确认删除需求吗？此操作无法复原'
				this.$refs.alertDialog.open()
			},
			async issue(item) {
				try {
					let result = await transformNeed(this.userInfo.id, item.need_id)
				} catch (e) {
					console.log(e)
					return 
				}
				this.onrefresh()
			},
			goToRecommend(msg) {
				const item = msg[0]
				let index = msg[1]
				// this.recommend(item, index)
				uni.navigateTo({ url:'../recommend/expert-recommend?item=' + encodeURIComponent(JSON.stringify(item)) })
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
			onrefresh() {
				if (this.refreshing) return
				this.refreshing = true
				// this.$refs.loading.open()
				this.requestData()
				// setTimeout(() => {
				// 	this.refreshing = false
				// 	uni.showToast({ title:'已更新',duration:500 })
				// }, 200)
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
