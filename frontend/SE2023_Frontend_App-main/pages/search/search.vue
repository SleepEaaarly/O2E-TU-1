<template>
		<view class="search-view">
			<template v-if="list.length>0">
				<block v-for="(item,index) in list" :key="index">
					<index-list 
						@likeOrTread="likeOrTread"
						@share="share"
						@opendDetail="opendDetail"
						:userInfo="userInfo"
						:item="item" :index="index"></index-list>
				</block>
				<load-more :loadtext="loadtext"></load-more>
			</template>
			<template v-else-if=" list.length<1">
				<no-thing></no-thing>
			</template>
		</view>
</template>

<script>
	import indexList from '../../components/index/index-list.vue'
	import noThing from '../../components/common/no-thing.vue'
	import loadMore from '../../components/common/load-more.vue'
	import { searchTopicList } from '@/api/search.js'
	import { giveLike } from '@/api/common.js'
	import { mapState } from 'vuex'
	export default {
		components:{
			indexList,
			noThing,
			loadMore
		},
		computed:{ ...mapState(['userInfo']) },
		data() {
			return {
				issearch:false,
				loadtext:'',
				list:[],
				searchtext:'',
				page:0
			}
		},
		// 监听原生标题导航按钮点击事件(取消按钮)
		onNavigationBarButtonTap(e){
			if(e.index===0){
				uni.navigateBack({ delta: 1 })
			}
		},
		// 监听搜索框文本变化
		onNavigationBarSearchInputChanged(e){
			this.searchtext=e.text
		},
		// 监听点击搜索按钮事件
		onNavigationBarSearchInputConfirmed(e){
			if(e.text){ this.getdata() }
		},
		// 监听页面触底事件
		onReachBottom() {
			this.loadmore()
		},
		// 监听下拉刷新
		onPullDownRefresh() {
			this.getdata()
			uni.stopPullDownRefresh()
		},
		methods:{
			// 搜索事件
			async getdata(){
				// 请求服务器 post keyword:this.searchtext
				let data
				if(this.searchtext.length===0){
					uni.showToast({
						title:'搜索内容不能为空!',
						icon:'none'
					})
					return
				}
				try{
					data = await searchTopicList(this.page+1,this.searchtext,'')
					console.log(data)
					if(data.length===0){
						this.issearch=true
						this.list = []
						this.loadtext='没有更多数据了'
						return 
					}else{
						this.page = this.page+1
						this.list = data
					}
				}catch(e){
					console.log(e)
					return 
				}

			},
			async likeOrTread(data) {
				giveLike(data.id)
				if(data.is_like){
					this.$http.toast('你已取消点赞!')
				}else{
					this.$http.toast('点赞成功!')
				}
			},
			share() {
				this.$http.toast('敬请期待~')
			},
			opendDetail(item) {
				uni.navigateTo({ url: '../../pages/detail/detail?id=' + item.id, })
			},
			// 上拉加载
			 loadmore(){
				if(this.loadtext!=='上拉加载更多'){ return }
				// 修改状态
				this.loadtext='加载中...'
				// 获取数据
				this.getdata()
				
			},
		}
	}
</script>

<style scoped>

	.search-view{
		background-color: #F9F9F9;
		height: 100vh;
		padding-top: 2upx;
	}
</style>
