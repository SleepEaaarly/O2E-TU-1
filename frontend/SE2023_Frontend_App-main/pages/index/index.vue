<template>
	<view class="index-icontainer">

		<myNavBar @signIn="signIn"></myNavBar>
		<!-- <tui-fab bgColor="#FFE933" :width="98" :height="98" :bottom="150" :right="50" @click="publish"></tui-fab> -->
		
		<!-- "推荐-热榜"滑动tabbar -->
		<swiper-tab-head :tabBars="tabBars" :tabIndex="tabIndex" @tabtap="tabtap">
		</swiper-tab-head>

		<template v-if="recommendList.list.length > 0 && tabIndex == 0">
			<block v-for="(item, index1) in recommendList.list" :key="index1">
				<index-list 
				@likeOrTread="likeOrTread" @opendDetail="opendDetail" @share="share" :item="item" :userInfo="userInfo"
				 :index="index1"></index-list>
			</block> 
			<load-more :loadtext="recommendList.loadtext"></load-more>
		</template>
		
		<!-- 热榜 -->
		<template v-if="hotList.list.length > 0 && tabIndex == 1">
			<view class="topic-list">
				<block v-for="(list, index1) in hotList.list" :key="index1">
					<card @opendDetail="opendDetail" :cardinfo="list" :index="index1"></card>
				</block>
			</view>
		</template>

		<!--底部分享弹窗-->
		<tui-bottom-popup :show="popupShow" @close="popup">
			<view class="tui-share">
				<view class="tui-share-title">分享到</view>
				<scroll-view scroll-x style="padding-right:20rpx">
					<view class="tui-share-top">
						<view class="tui-share-item" :class="[shareList[0].share.length-1===index?'tui-item-last':'']" v-for="(item,index) in shareList[0].share"
						 :key="index" @tap="popup">
							<view class="tui-share-icon" hover-class="tui-hover" :hover-stay-time="150">
								<tui-icon :name="item.icon" :color="item.color" :size="item.size?item.size:36"></tui-icon>
							</view>
							<view class="tui-share-text">{{item.name}}</view>
						</view>
						<view class="tui-empty">!</view>
					</view>

				</scroll-view>
				<scroll-view scroll-x class="tui-mt">
					<view class="tui-share-bottom">
						<view class="tui-share-item" :class="[shareList[1].operate.length-1===index?'tui-item-last':'']" v-for="(item,index) in shareList[1].operate"
						 :key="index" @tap="popup">
							<view class="tui-share-icon" hover-class="tui-hover" :hover-stay-time="150">
								<tui-icon :name="item.icon" color="#404040" :size="item.size" :bold="index===2"></tui-icon>
							</view>
							<view class="tui-share-text">{{item.name}}</view>
						</view>
					</view>
				</scroll-view>
				<view class="tui-btn-cancle" @tap="popup">取消</view>
			</view>
		</tui-bottom-popup>
		<!--底部分享弹窗-->
		<view>
			<uni-calendar :start-date="'2019-3-2'" :end-date="'2019-5-20'" @change="change" ref="calendar" :insert="false"
			 @confirm="confirm" />
		</view>
	</view>
</template>


<script>
	import indexList from '../../components/index/index-list.vue'
	import swiperTabHead from '../../components/index/swiper-tab-head.vue'
	import loadMore from '../../components/common/load-more.vue'
	import noThing from '../../components/common/no-thing.vue'
	import myNavBar from '../../components/common/my-nav-bar.vue'
	import uniCalendar from '@/components/uni-calendar/uni-calendar.vue'
	import card from '../../components/list-card/list-card-1.vue'
	import {
		getTopicList,
		getRecommendList
	} from '@/api/index.js'
	import { giveLike } from '@/api/common.js'
	import {
		mapState,
		mapMutations
	} from 'vuex'
	export default {
		components: {
			indexList,
			swiperTabHead,
			loadMore,
			noThing,
			uniCalendar,
			myNavBar,
			card,
		},
		data() {
			return {
				swiperheight: 500,
				tabIndex: 1,
				start:0,
				remain:3,
				end: 5,
				size: 400,
				// list 偏移量
				offset: 0,
				refreshing: false,
				shoNo: false,
				popupShow: false,
				shareList: [{
					share: [{
						name: 'QQ',
						icon: 'qq',
						color: '#07BDFD',
						size: 68
					}, {
						name: '微信',
						icon: 'wechat',
						color: '#80D640',
						size: 68
					}, {
						name: '朋友圈',
						icon: 'moments',
						color: '#80D640',
						size: 68,
					}]
				}, {
					operate: [{
						name: '刷新',
						icon: 'refresh',
						size: 56
					}, {
						name: '搜索内容',
						icon: 'search-2',
						size: 56
					}]
				}],
				tabBars: [{
						name: '推荐',
						id: 'tuijian',
						page: 1
					},
					{
						name: '热榜',
						id: 'hanfu',
						page: 1
					},
				],
				newslist: [{
						loadtext: '没有更多数据了',
						id: 'recommend',
						list: []
					},
					{
						loadtext: '没有更多数据了',
						id: 'hotList',
						list: []
					},
				],
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					list: []
				},
				hotList: {
					loadtext: '没有更多数据了',
					id: 'hotList',
					list: []
				},
			}
		},
		onShow() {		//页面加载,一个页面只会调用一次
			console.log('index-onShow()')
			this.requestData()
		},
		onLoad() {		//页面显示,每次打开页面都会调用一次
			console.log('index-onLoad()')
			uni.getSystemInfo({
				success: res => {
					let height = res.windowHeight - uni.upx2px(100)
					this.swiperheight = height
				}
			})
			//this.requestData() 不能刷新，防止点进文章再出来跳飞了
		},
		computed: {
			...mapState(['userInfo']),
			// 预留项
			preCount(list) {
				return list.map(item=>{
					return Math.min(this.start, this.remain)
				})
			},
			nextCount(list) {
				return list.map(item=>{
					return Math.min(item.list.length - this.end, this.remain)
				})
			},

		},
		
		methods: {
			// async requestData(GoPage, Gotype) {
			async requestData() {
				// let currentPage = GoPage || this.tabBars[this.tabIndex].page;
				let type = this.tabBars[this.tabIndex].id
				let items
				//let curList = this.tabIndex == 0 ? this.recommendList: this.hotList
				
				try {
					if(this.tabIndex === 0){
						items = await getRecommendList()
					} else {
						items = await getTopicList()
					}
					//console.log(items)
				} catch (e) {
					console.log(e)
					return
				}
				
				if (items && items.length === 0) {
					this.tabBars[this.tabIndex].page = page
					// this.newslist[this.tabIndex].loadtext = "没有更多数据了"
					if(this.tabIndex === 0){
						this.recommendList.loadtext = '没有更多数据了'
					} else {
						this.hotList.loadtext = '没有更多数据了'
					}
					
					return
				}
				// this.tabBars[this.tabIndex].page = page
				// if(this.tabIndex === 1){
				// 	this.newslist[this.tabIndex].list = items
				// }else{
				// 	this.newslist[this.tabIndex].list = this.newslist[this.tabIndex].list.concat(items)
				// }
				
				if(this.tabIndex === 0){
					this.recommendList.list = items
				} else {
					this.hotList.list = items
				}
				
				// this.newslist[this.tabIndex].list.splice(indexOfItem, , newValue)
				
				if (items) {
					if(this.tabIndex === 0){
						this.recommendList.loadtext = '没有更多数据了'
					} else {
						this.hotList.loadtext = '没有更多数据了'
					}
				} else {
					if(this.tabIndex === 0){
						this.recommendList.loadtext = '上拉加载更多'
					} else {
						this.hotList.loadtext = '上拉加载更多'
					}
				}
			},
			publish() {
				// 打开发布页面
				this.$http.href('../add-input/add-input')
			},
			searchInfo() {
				console.log('searchInfo')
				// uni.navigateTo({
				// 	url: '../search/search',
				// });
			},
			share() {
				this.popupShow = !this.popupShow
			},
			popup: function() {
				this.popupShow = !this.popupShow
				this.$http.toast('敬请期待~')
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
			loadmore(index) {
				// if (this.newslist[index].loadtext != "上拉加载更多") {
				// 	return;
				// }
				// // 修改状态
				// this.newslist[index].loadtext = "加载中...";
				// const scrollTop = ev.detail.scrollTop;
				// // 开始位置
				// const start = Math.floor(scrollTop / this.size)
				// this.start = start < 0 ? 0 : start;
				// // 结束位置
				// this.end = this.start + this.remain;
				// // 计算偏移
				// const offset = scrollTop - (scrollTop % this.size) - this.preCount * this.size
				// this.offset = offset < 0 ? 0 : offset;
				// 获取数据
				// this.requestData(this.tabBars[this.tabIndex].page + 1)

			},
			handleScroll(ev) {
				// let curList = this.tabIndex == 0 ? this.recommendList: this.hotList 
				
				// const scrollTop = ev.detail.scrollTop;
				// console.log(scrollTop)
				// // console.log(this.newslist[this.tabIndex])
				// // 开始位置
				// const start = Math.floor(scrollTop / this.size)
				// this.start = start < 0 ? 0 : start;
				// // 结束位置
				// this.end = this.start + this.remain;
				// // 计算偏移
				// const offset = scrollTop - (scrollTop % this.size) - this.preCount(curList) * this.size
				// this.offset = offset < 0 ? 0 : offset;
			},
			// tabbar点击事件
			tabtap(index) {
				console.log('tabtap')
				this.tabIndex = index
				this.requestData()
			},
			// 滑动事件
			tabChange(e) {
				console.log('tabexchange')
				this.tabIndex = e.detail.current
				//this.requestData(this.tabBars[this.tabIndex].page, this.tabBars[this.tabIndex].id)
				this.requestData()
			},
			async likeOrTread(data) {
				giveLike(data.id)
				console.log(data)
				if(data.is_like){
					this.$http.toast('你已取消点赞!')
				}else{
					this.$http.toast('点赞成功!')
				}
			},
			opendDetail(item) {
				console.log('before jump to the detailed value, the id is ' + item.id)
				uni.navigateTo({
					//用@居然还不行？？
					url: '../../pages/detail/detail?id=' + item.id,
				})
			},
			change(e) {
				console.log(e)
			},
			confirm(e) {
				console.log(e)
			},
			initNavigation(e) {
				this.opcity = e.opcity
				this.top = e.top
			},
			async signIn(){
				this.$http.href('../../pages/check-in/check-in')
			}
		},

	}
</script>

<style>
	/* 隐藏scroll-view滚动条*/
	::-webkit-scrollbar {
		width: 0;
		height: 0;
		color: transparent;
	}

	.search-wrp {
		display: flex;
		position: relative;
		background: #FFFFFF;
		justify-content: space-between;
		height: 80upx;
		align-items: center;
		padding: 8upx 16upx 0 16upx;
	}

	.index-icontainer {
		background-color: #F9F9F9;
	}

	.font-x {
		font-size: 44upx;
	}

	.uni-input {
		background: #F9F9F9;
		text-align: center;
		margin-right: 20upx;
		margin-left: 20upx;
	}

	.serach {
		position: absolute;
		top: 10upx;
		left: 280upx;
		font-size: 40upx;
	}

	/* 隐藏scroll-view滚动条*/
	::-webkit-scrollbar {
		width: 0;
		height: 0;
		color: transparent;
	}

	/*header*/
	.tui-header {
		width: 100%;
		padding-top: 34upx;
		/* box-shadow: 0 15rpx 10rpx -15rpx #f2f2f2; */
		box-sizing: border-box;
		background-color: #fff;
		position: fixed;
		z-index: 1000;
	}

	.tui-header-top,
	.tui-header-bottom {
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: 26rpx;
		color: #333;
	}

	.tui-top-item {
		height: 26rpx;
		line-height: 26rpx;
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.tui-topitem-active {
		position: relative;
		font-weight: bold;
	}

	.tui-topitem-active::after {
		content: '';
		position: absolute;
		width: 44rpx;
		height: 6rpx;
		background: #5677fc;
		border-radius: 6rpx;
		bottom: -10rpx;
		left: 50%;
		-webkit-transform: translateX(-50%);
		transform: translateX(-50%);
	}

	.tui-price-arrow {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 20rpx;
	}

	.tui-bottom-item .tui-icon-class,
	.tui-screen .tui-icon-class {
		margin-left: 6rpx;
	}

	.tui-icon-box {
		line-height: 12px !important;
		padding: 0 !important;
		display: block !important;
		position: relative;
	}

	.tui-arrow-up {
		top: 5px;
	}

	.tui-arrow-down {
		top: -3px;
	}

	.tui-header-bottom {
		margin-top: 56rpx;
		height: 108rpx;
		padding: 0 30rpx;
		box-sizing: border-box;
		font-size: 24rpx;
		align-items: flex-start;
		overflow: hidden;
	}

	.tui-bottom-text {
		line-height: 24rpx;
	}

	.tui-bottom-item {
		flex: 1;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 18rpx 12rpx;
		border-radius: 40rpx;
		box-sizing: border-box;
		background: #f2f2f2;
		margin-right: 20rpx;
		white-space: nowrap;
	}

	.tui-bottom-item:last-child {
		margin-right: 0;
	}

	.tui-btmItem-active {
		padding-bottom: 60rpx;
		border-bottom-left-radius: 0;
		border-bottom-right-radius: 0;
	}

	.tui-bold {
		font-weight: bold;
	}

	.tui-active {
		color: #5677fc;
	}

	.tui-ml {
		margin-left: 6rpx;
	}

	.tui-seizeaseat-20 {
		height: 20rpx;
	}

	.tui-seizeaseat-30 {
		height: 30rpx;
	}

	.tui-middle {
		vertical-align: middle;
	}

	.tui-drop-item .tui-icon-class {
		vertical-align: middle;
	}

	/*header*/

	/*header 下拉选择*/

	.tui-scroll-box {
		width: 100%;
		height: 480rpx;
		box-sizing: border-box;
		position: relative;
		z-index: 99;
		color: #fff;
		font-size: 30rpx;
		word-break: break-all;
	}

	.tui-drop-item {
		color: #333;
		height: 80rpx;
		font-size: 28rpx;
		padding: 20rpx 40rpx 20rpx 40rpx;
		box-sizing: border-box;
		display: inline-block;
		width: 50%;
	}

	.tui-drop-btnbox {
		width: 100%;
		height: 100rpx;
		position: absolute;
		left: 0;
		bottom: 0;
		box-sizing: border-box;
		display: flex;
	}

	.tui-drop-btn {
		width: 50% !important;
		border-radius: 0 !important;
		font-size: 32rpx !important;
		text-align: center;
		height: 100rpx;
		line-height: 100rpx;
		border: 0;
	}


	/*header 下拉选择*/

	.top-dropdown {
		margin-top: 360rpx;
		padding: 0 40rpx;
		box-sizing: border-box;
	}

	.tui-share-box {
		padding: 0 50rpx;
		box-sizing: border-box;
	}

	.tui-drop-input-box {
		padding: 50rpx;
		box-sizing: border-box;
	}

	.tui-animation {
		display: inline-block;
		transform: rotate(0deg);
		transition: all 0.2s;
	}

	.tui-animation-show {
		transform: rotate(180deg);
	}

	.tui-selected-list {
		background-color: #fff;
		border-radius: 20rpx;
		overflow: hidden;
		transform: translateZ(0);
	}

	.tui-dropdown-scroll {
		height: 400rpx;
	}

	.tui-cell-class {
		display: flex;
		align-items: center;
		padding: 26rpx 30rpx !important;
	}

	.tui-ml-20 {
		margin-left: 20rpx;
	}

	.tui-share {
		background: #e8e8e8;
		position: relative;
		padding-bottom: env(safe-area-inset-bottom);
	}

	.tui-share-title {
		font-size: 26rpx;
		color: #7E7E7E;
		text-align: center;
		line-height: 26rpx;
		padding: 20rpx 0 50rpx 0;
	}

	.tui-share-top,
	.tui-share-bottom {
		min-width: 101%;
		padding: 0 20rpx 0 30rpx;
		white-space: nowrap;
	}

	.tui-mt {
		margin-top: 30rpx;
		padding-bottom: 150rpx;
	}

	.tui-share-item {
		width: 126rpx;
		display: inline-block;
		margin-right: 24rpx;
		text-align: center;
	}

	.tui-item-last {
		margin: 0;
	}

	.tui-empty {
		display: inline-block;
		width: 30rpx;
		visibility: hidden;
	}

	.tui-share-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		background: #fafafa;
		height: 126rpx;
		width: 126rpx;
		border-radius: 32rpx;
	}

	.tui-share-text {
		font-size: 24rpx;
		color: #7E7E7E;
		line-height: 24rpx;
		padding: 20rpx 0;
		white-space: nowrap;
	}

	.tui-btn-cancle {
		width: 100%;
		height: 100rpx;
		position: absolute;
		left: 0;
		bottom: 0;
		background: #f6f6f6;
		font-size: 36rpx;
		color: #3e3e3e;
		display: flex;
		align-items: center;
		justify-content: center;
		padding-bottom: env(safe-area-inset-bottom);
	}

	.tui-hover {
		background: rgba(0, 0, 0, 0.2)
	}
	
	.topic-list{
		box-sizing: border-box;
		background-color: #F9F9F9;
		padding: 5upx 20upx 0 30upx;
	}
</style>
