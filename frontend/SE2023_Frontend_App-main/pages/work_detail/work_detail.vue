<template>
	<view >
		<u-row>
			<text style="margin-left:50rpx;font-size: 20px;font-weight: 550;text-align:center;">{{ work_info.workName }}</text>
		</u-row>
		
		<author-card
			:name="work_info.expert_name" 
			:title="work_info.expert_title" :institution="work_info.expert_organization"
			:mail="work_info.expert_mail"
			:logoPath="work_info.expert_logoPath"></author-card>
		
		<view style="
		margin-top: auto;background-color: aliceblue;width: 650rpx;margin-left: 35rpx;height: auto;
		border-left:8rpx solid cornflowerblue;
		background-color: aliceblue;padding-top: 10rpx;padding-left: 20rpx;padding-bottom: 10rpx;">
			<text class="intro">{{ work_info.work_abstract }}</text>
		</view>
		
		<view>
		<u-row>
			<u-tag text="成果简介"  plain plainFill size = "mini"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="work_info.work_period"  plain plainFill size = "mini" type="warning"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="work_info.work_field"  plain plainFill size = "mini" type="success"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			
		</u-row>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		</view>
		  <scroll-view :style="{height:height+'px'}" scroll-y>
			<image :src="work_info.work_pic" style="width: 100%;" mode="widthFix"></image>
		  </scroll-view>
		<uni-row >
			<!-- <view v-if="userInfo.type==4&&order.order_id==0"> -->
			<view>
				<uni-col :span="8">
					<button type="primary" @click="goToExpertSpace" class="fix-button-left">专家详情</button>
				</uni-col>
				<uni-col :span="8" :offset="8">
					<button type="primary" @click="generateWorkReport" class="fix-button-right">生成报告</button>
				</uni-col>
			</view>
		</uni-row>
	</view>
	
</template>

<script>
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import { mapState, mapMutations } from 'vuex'
	import authorCard from"../../components/author_display_card.vue"
	import { getWork } from "@/api/work_detail.js"
	import workGenerateCard from '@/api/work_report.js'
	export default {
		computed: {
			...mapState(['userInfo']),
		},
		data() {
			return {
				work_id: 1,
				height: 500,
				work_info: {
					"workName": 'A Summary of Machine Learning',
					"expert_name": '占瑞乙',
					"expert_title": '本科生',
					"work_abstract": 'Here is a summary of some of the most commonly used methods in machine learning.',
					"expert_organization": '北京航空航天大学',
					"expert_logoPath": '/static/head_zry_fox.jpg',
					"work_id": '',
					"expert_id": '',
					"user_id": '',
					"work_pic": '/static/ML_Notes.png' ,
					"expert_mail": "iszry@foxmail.com",
					"work_period": "实验室",
					"work_field": "科学创意"
				}
			}
		},
		onLoad(data) {
			// console.log(data)
			// console.log('data should be:' + data.rid)
			this.work_id = data.rid
			this.loadData()
		},
		methods: {
			async loadData(){
				// console.log('get work detail')
				this.work_info = await getWork(this.work_id)
				// console.log(this.work_info)
			},
			goToExpertSpace() {
				uni.navigateTo({ url:'../user-space/user-space?uid='+this.work_info.user_id })
			},
			generateWorkReport() {
				// 调用生成报告的 api，后端负责将报告插入到对应的用户-系统聊天之中
				// console.log(this.userInfo.id)
				// console.log(this.work_info.work_id)
				workGenerateCard(this.userInfo.id, this.work_info.work_id)
			}
		},
		components: {
			authorCard,
			uniCol,
			uniRow,
		},
		
	}
</script>

<style>

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
