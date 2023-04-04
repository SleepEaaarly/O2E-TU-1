<template>
	<view>

		<u-row>
			<text style="margin-left:50rpx;font-size: 20px;font-weight: 550;">{{ work_info.workName }}</text>
		</u-row>
		
		<author-card
			:name="work_info.expert_name" 
			:title="work_info.expert_title" :institution="work_info.expert_organization"
			:logoPath="work_info.expert_logoPath"></author-card>
		
		<view style="
		margin-top: 30rpx;background-color: aliceblue;width: 650rpx;margin-left: 35rpx;height: 200px;
		border-left:8rpx solid cornflowerblue;
		background-color: aliceblue;padding-top: 30rpx;padding-left: 20rpx;">
			<text class="intro">{{ work_info.work_abstract }}</text>
		</view>
		
		<view>
		<u-row>
			<u-tag text="成果简介"  plain plainFill size = "mini"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			
		</u-row>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		</view>
		<view>
			<!-- PDF_upload -->
		</view>
	</view>
	
</template>

<script>
	import authorCard from"../../components/author_display_card.vue"
	export default {
		data() {
			return {
				work_info: {
					"workName": 'TestWork',
					"expert_name": '相关专家',
					"expert_title": '专家职称',
					"work_abstract": 'Introduction to the work',
					"expert_organization": '专家机构',
					"expert_logoPath": '/static/head.jpg',
					"work_id": '',
					"expert_id": '',
					"user_id": '',
					"work_pdf": '' 
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
