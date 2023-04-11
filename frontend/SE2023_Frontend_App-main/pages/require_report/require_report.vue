<template>
	<view>
		<u-row>
			<text style="margin-left:50rpx;font-size: 20px;font-weight: 550;text-align:center;">{{ require_info.requireName }}</text>
		</u-row>
		
		<company-card
		:name="require_info.company_name"
		:area="require_info.company_area" 
		:address="require_info.company_address"
		:logoPath="require_info.company_logoPath"
		
		></company-card>
		
		<view style="
		margin-top: auto;background-color: aliceblue;width: 650rpx;margin-left: 35rpx;height: auto;
		border-left:8rpx solid cornflowerblue;
		background-color: aliceblue;padding-top: 10rpx;padding-left: 20rpx;padding-bottom: 10rpx;">
			<text class="intro">{{ require_info.require_intro }}</text>
		</view>
		
		<view>
		<u-row>
			<u-tag text="需求简介"  plain plainFill size = "mini"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="require_info.require_keyword_1"  plain plainFill size = "mini" type="warning"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="require_info.require_keyword_2"  plain plainFill size = "mini" type="success"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			
		</u-row>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		</view>
		
	</view>
</template>

<script>
	import companyCard from "../../components/company_rep_display_card.vue"
	export default {
		data() {
			return {
				work_id: 1,
				height: 500,
				require_info: {
					"requireName": '帮我写软工吧',
					"company_name": '北京航空航天大学',
					"require_intro": 'Here is a summary of some of the most commonly used methods in machine learning.',
					"company_address": '北京市海淀区',
					"company_logoPath": '/static/head.jpg',
					"company_area":'计算机',
					"require_id": '',
					"company_id": '',
					// "user_id": '',
					// "work_pic": '/static/ML_Notes.png' ,
					"require_keyword_1": "实验室",
					"require_keyword_2": "科学创意"
				}
				
			}
		},
		methods: {
			
		},
		components: {
			companyCard,
		}
	}
</script>

<style>

</style>
