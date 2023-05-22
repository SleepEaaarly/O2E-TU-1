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
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<text>
				{{ content }}
			</text>
		</u-row>
		</view>
		
	</view>
</template>

<script>
	import {
		mapState,
		mapMutations
	} from 'vuex'
	import { getRequireReport } from '../../api/require_report'
	import companyCard from "../../components/company_rep_display_card.vue"
	import fuiCard from "@/components/firstui/fui-card/fui-card.vue"
	import require_message_card from 'components/require_message_card'
	import { picUrl } from '@/common.js'
	export default {
		data() {
			return {
				inRequireId: null,
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
				},
				content: "",
			}
		},
		onLoad(data) {
			this.inRequireId = data.reportId
			this.getRequireDetailInfo()
		},
		computed: {
			...mapState(['userInfo'])
		},
		methods: {
			async getRequireDetailInfo() {
				let output = await getRequireReport(this.inRequireId)
				console.log(output)
				this.require_info.requireName = output.requireInfo.requireName
				this.require_info.company_name = output.companyInfo.companyName 
				this.require_info.require_intro = output.requireInfo.requireIntro 
				this.require_info.company_address = output.companyInfo.companyAddress
				this.require_info.company_logoPath = "http://116.63.14.146:8000/api" + output.companyInfo.companyLogoPath
				this.require_info.company_area = output.companyInfo.companyArea
				this.require_info.require_id = output.requireInfo.requireId 
				this.require_info.company_id = output.companyInfo.companyId
				this.require_info.require_keyword_1 = output.requireInfo.requireKeywords 
				// this.require_info.require_keyword_2
				this.content = output.content
			},
			gotoCompanyDetail() {

			},
			gotoRequireDetail() {

			}
		},
		components: {
			companyCard,
			fuiCard,
			require_message_card
		}
	}
</script>

<style>

</style>
