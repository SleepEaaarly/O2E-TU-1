<template>
	
	<view>
		<swiper-tab-head
			:tabBars="tabBars" 
			:tabIndex="tabIndex"
			@tabtap="tabtap"
			scrollItemStyle="width:50%;"
			scrollStyle="border-bottom:0;">
		</swiper-tab-head>
		<template v-if="tabIndex==0">
			<uni-section  title="显示全部已回复反馈" type="circle" >
				<view class="u-f-ajc animated fadeIn" v-if="feeds0.length==0">
					<image src="/static/images/toast/no-data-03.jpg" 
						mode="widthFix"></image>
					<!-- <text>暂无数据</text> -->
				</view>
				<view v-else>
					<uni-card v-for='(feed,index) in feeds0' :key="index"
							  :is-shadow='false' :title="feed.name" 
							  :extra="feed.datatime" :sub-title="feed.email">
						
						<uni-list>
							<uni-list-item title="反馈内容" :note="feed.description" :border="false">
								
							</uni-list-item>
							<uni-list-item title="回复内容" :note="feed.message" :border="false">
								
							</uni-list-item>
						</uni-list>
						
					</uni-card>
				</view>
			</uni-section>
			
		</template>
		
		<template v-else-if="tabIndex==1">
			<uni-section title="显示全部未回复反馈" type="circle" >
				<view class="u-f-ajc animated fadeIn" v-if="feeds1.length==0">
					<image src="/static/images/toast/no-data-03.jpg" 
						mode="widthFix"></image>
					<!-- <text>暂无数据</text> -->
				</view>
				<view v-else>
					<uni-card v-for='(feed,index) in feeds1' :key="index"
							  :is-shadow='false' :title="feed.name" 
							  :extra="feed.datatime" :sub-title="feed.email">
						<uni-list>
							<uni-list-item title="反馈内容" :note="feed.description" :border="false" :extraIcon="extraIcon1">
								
							</uni-list-item>
							
						</uni-list>
					</uni-card>
				</view>
			</uni-section>
			
		</template>
		
		
	</view>
</template>

<script>
	import { mapState } from 'vuex'
	import{ picUrl, } from '@/api/common.js'
	import homeData from '../../components/home/home-data.vue'
	import { getUserInfo } from '@/api/user-space.js'
	import swiperTabHead from '../../components/index/swiper-tab-head.vue'
	import {getReplied,getUnreplied} from '@/api/feedback.js'
	
	export default {
		components:{
			swiperTabHead,
		},
		computed:{ ...mapState(['userInfo']) },
		onLoad(){
			
		},
		async onShow(){
			this.init()
		},
		data() {
			return {
				feeds0:[
					
				],
				feeds1:[
					
				],
				tabIndex:0,
				tabBars:[
					{ name:'已回复', id:'homepage' },
					{ name:'未回复', id:'dynamic' },
									
				],
				extraIcon1: {
					color: '#4cd964',
					size: '30',
					type: 'paperplane-filled'
				},
				extraIcon2: {
					color: '#4cd964',
					size: '22',
					type: 'redo-filled'
				},
			}
		},
		methods: {
			async init(){
				let id = this.userInfo.id
				let replied = await getReplied(id)
				let unreplied = await getUnreplied(id)
				this.feeds0 = replied.data
				this.feeds1 = unreplied.data
				console.log(this.feeds1[0])
			},
			tabtap(index){
				this.tabIndex=index
			},
		}
	}
</script>
	
<style>
	.mystyle image{
		width: 100%;
	}
</style>
