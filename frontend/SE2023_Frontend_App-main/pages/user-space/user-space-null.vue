<template>
</template>

<script>
</script>

<style>
</style>
<template>
	<view>
		<!-- 背景图 + 用户基本信息 -->
		<user-space-head 
			@userActive="userActive"
			@refreshData="refreshData"
			:userinfo="info"></user-space-head>、
		
		<!-- 数据统计 -->
		<view class="user-space-data">
			<home-data :homedata="spacedata"></home-data>
		</view>
		<view style="height: 20upx; background: #F4F4F4;"></view>
		
		<!-- tab导航 -->
		<swiper-tab-head 
		:tabBars="tabBars" 
		:tabIndex="tabIndex"
		@tabtap="tabtap"
		scrollItemStyle="width:25%;"
		scrollStyle="border-bottom:0;">
		</swiper-tab-head>
		<view style="margin-bottom: 5upx;"></view>
		
		<!-- 主页 -->
		<template v-if="tabIndex==0">
			<user-space-userinfo 
				:userinfo="info"
				:authInfo="userInfo"
				></user-space-userinfo>
		</template>
		
		<!-- 成果 -->
		<template v-if="tabIndex==1 && info.type==4">
			<userAchievement></userAchievement>	
		</template>
	</view>
</template>

<script>
	import userSpaceHead from '../../components/user-space/user-space-head.vue'
	import homeData from '../../components/home/home-data.vue'
	import swiperTabHead from '../../components/index/swiper-tab-head.vue'
	import userSpaceUserinfo from '../../components/user-space/user-space-userinfo.vue'
	import commonList from '../../components/common/common-list.vue'
	import card from '../../components/list-card/list-card.vue'
	import loadMore from '../../components/common/load-more.vue'
	import userSpacePopup from '../../components/user-space/user-space-popup.vue'
	import { mapMutations, mapState } from 'vuex'
	import topicList from '../../components/news/topic-list.vue'
	import time from '../../common/time.js'
	import { saveUserAccess,getUserInfo,getTopicListByUid,getTopicTitleByUid } from '@/api/user-space.js'
	import userRate from './user-rate.vue'
	
	import { picUrl } from '@/api/common.js'
	
	import wordCloud from './wordCloud.vue'
	import userAchievement from './user-achievement.vue'
	
	export default {
		components:{
			userSpaceHead,
			homeData,
			swiperTabHead,
			userSpaceUserinfo,
			commonList,
			loadMore,
			userSpacePopup,
			card,
			topicList,
			wordCloud,
			userAchievement,
			userRate,
		},
		computed:{ ...mapState(['userInfo']), },
		onShow() {		//页面加载,一个页面只会调用一次
		  //   if (this.ifOnShow == true) {
				// this.initData(this.info.id)
				// window.location.reload();//返回当前页面强制书哈辛
		  //   } 
		},
		onLoad(data) {		//页面显示,每次打开页面都会调用一次
			if (data) {
				console.log(data.expert)
				console.log(data.expert.id)
				// console.log(answer.id)
				// console.log(answer)
				console.log("?")
				this.initData(data.expert)
			} else {
				console.log("error! no values are loaded")
			}
		},
		onHide() {
		    uni.hideLoading() 
		    this.ifOnShow = true
		},
		
		provide () {
		    // return { reload: this.initData(this.info.id) }
		},
		data() {
			return {
				ifOnShow: false,//首先设置ifOnShow不然会一直循环刷新
				show: false,	//控制右上角菜单是否显示
				field_items: [
					'信息技术', '装备制造', '新材料', '新能源', '节能环保', '生物医药', '科学创意', '检验检测', '其他'
				],
				info:{
					currentId: -1,
					bgimg:1,
					userpic:'',
					username:'',
					email:'',
					institution:'',
					sex:0,
					age:0,
					isguanzhu:0,
					id:0,
					job:'',
					path:'',
					type:-1,
					state:-1,
					enterprise_name:'',
					enterprise_address:'',
					enterprise_website:'',
					enterprise_instruction:'',
					enterprise_phone:'',
					enterprise_legal_representative:'',
					enterprise_register_capital:0,
					enterprise_field:'',
				},
				topicList:[],
				titleList:[],
				spacedata:[
					{ name:'获赞', num:0 },
					{ name:'关注', num:0 },
					{ name:'粉丝', num:0 },
				],
				tabIndex:0,
				tabBars:[
					{ name:'主页', id:'homepage' },
					{ name:'成果', id:'masterpiece' },
				],
				tablist:[ {},
					{
						loadtext:'',
						list:[
						]
					},
					{
						loadtext:'',
						// 上拉加载更多
						list:[
						]
					},
				],
			}
		},
		// 上拉触底事件
		onReachBottom() {
			// 上拉加载
			//this.loadmore()
		},
		onNavigationBarButtonTap(e) {
			if(e.index === 0){
				this.togleShow() 
			}
		},
		methods: {
			initData(data){
				console.log(data.username)
				if(data){
					this.spacedata = []
					this.info.userpic = picUrl+data.userpic
					this.info.username = data.username
					this.info.email = data.email
					this.info.institution=data.institution
					this.info.isguanzhu = data.is_following
					this.info.id = data.id
					this.info.type = data.type
					this.info.state = data.state
					this.info.enterprise_name= data.enterprise_name
					this.info.enterprise_address= data.enterprise_address
					this.info.enterprise_website= data.enterprise_website
					this.info.enterprise_instruction= data.enterprise_instruction
					this.info.enterprise_phone= data.enterprise_phone
					this.info.enterprise_legal_representative= data.enterprise_legal_representative
					this.info.enterprise_register_capital= data.enterprise_register_capital
					this.info.enterprise_field = data.enterprise_field
					
					
					
					
					this.info.expert_name = data.expert_name
					this.info.expert_organization = data.expert_organization
					this.info.expert_field = data.expert_field
					this.info.expert_scholarprofile = data.expert_scholarprofile
					this.info.expert_phone = data.expert_phone
				}
				if (this.info.expert_field) {
					let str = ''
					let s = this.info.expert_field
					for (let i = 0; i < s.length; i++) {
						if (s[i] === '1') {
							str = str + this.field_items[i] + ' '
						}
					}
					this.info.expert_field = str
				}
			},
			getFiled(data) {
				let str = ''
				for (let i = 0; i < data.expert_field.length; i++) {
					console.log(data.expert_filed[i])
					// if (data.expert_filed[i] == '1') {
					// 	str = str + this.field_items[i] + " ";
					// }
				}
				console.log('get field ' + str)
				return str
			},
			userActive(){
				this.info.isguanzhu = !this.info.isguanzhu
			},
			refreshData(){
				
			},
			togleShow(){
				this.show = !this.show
			},
			loadmore(){
				if(this.tablist[this.tabIndex].loadtext !== '上拉加载更多'){ return }
				// 修改状态
				this.tablist[this.tabIndex].loadtext='加载中...'
				// 获取数据
				// this.tablist[this.tabIndex].loadtext="没有更多数据了";
			},
			tabtap(index){
				this.tabIndex=index
			},
			openResultDetail(){
				uni.showToast({
					icon:'loading',
					title:'功能开发中，敬请期待...',
					duration:500,
				})
			}
		}
	}
</script>

<style>
.user-space-margin{
	margin: 10upx 10upx 0  10upx;
}
.topic-view{
	padding: 20upx;
}
.topic-list{
	box-sizing: border-box;
	background-color: #F9F9F9;
	padding: 5upx 20upx 0 30upx;
}
.user-space-data{
	background: #FFFFFF;
	position: relative;
	z-index: 10;
	border-top-left-radius: 20upx;
	border-top-right-radius: 20upx;
	margin-top: -15upx;
}
</style>
