<template>
	<view>
		<need-data :needdata="needdata" :userInfo="userInfo" @goToExplore="goToExplore" @goToNeedInfo="goToNeedInfo" @openOrderDetail="openOrderDetail">
		</need-data>
	</view>
</template>

<script>
	import needData from '@/components/platform/need-data.vue'
	import { mapState } from 'vuex'
	import { getUserProfile, } from '@/api/home.js'
	import Vue from 'vue'
	
	export default {
		components: {
			needData
		},
		computed: {
			...mapState(['userInfo']) 
		},
		data() {
			return {
				refreshing: false,
				needdata:[
					{ name:'全部', num:0 },
					{ name:'待处理', num:0 },
					{ name:'进行中', num:0 },
					{ name:'已完成', num:0 },
				],
			}
		},
		
		onLoad() {
			this.requestData()
		},
		
		onShow() {
			console.log(this.userInfo.type)
			this.requestData()
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
			requestData(GoPage, Gotype) {
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
			// openLogin() {
			// 	uni.navigateTo({ url: '../login/login' })
			// },
			openOrderDetail(order_id) {
				console.log('openOrderDetail')
				uni.navigateTo({ url: '../order-detail/order-detail?id=' + order_id })
			},
			async onrefresh() {
				if (this.refreshing) return
				console.log('here is refreshing!!!')
				this.refreshing = true
				await this.requestData()
				setTimeout(() => {
					this.refreshing = false
					uni.showToast({ title:'已更新',duration:500 })
				}, 200)
			},
			initNavigation(e) {
				this.opcity = e.opcity
				this.top = e.top
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
			async signIn(){
				this.$http.href('@/pages/search-need/search-need')
			},
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
			// //去逛逛
			goToExplore(){
				console.log('tabindex change to 1.')
				this.tabIndex = 1
			},
		}
	}
</script>

<style>
</style>
