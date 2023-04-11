<template>
	<view>
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
	</view>
</template>

<script>
	import authorCard from"../../components/author_display_card.vue"
	export default {
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
		methods: {
			
		},
		components: {
			authorCard
		},
	}
</script>

<style>

</style>
