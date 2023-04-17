<template>
	<view>
		<u-row>
			<text class="title">需求信息</text>
		</u-row>
		<require-card
		:logoPath="'/static//logo.png'"
		:name="'帮我写软工吧'"
		:area="'软件工程'"
		:intro="'这是一个需求！'"
		:keyword="'soft engineering;computer science;company;expert'"
		></require-card>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		
		<u-row>
			<text class = "title">专家信息</text>
		</u-row>
		<author-card
		:name="'佛系甜胖妮'"
		:title="'废物'"
		:logoPath="'/static//head.jpg'"
		:mail="'duansangni@hhhhh.com'"
		:institution="'北京航空航天大学'"
		
		></author-card>
		
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		
		<u-row>
			<text class = "title">企业信息</text>
		</u-row>
		<company-card
		:name="'北京航空航天大学'"
		:area="'计算机科学与技术'" 
		:address="'北京市海淀区'"
		:logoPath="'/static//company.png'"
		
		></company-card>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		<u-row>
			<text class = "title">订单追踪</text>
		</u-row>
		<time-axis :dataArray="dataArray" style="margin-left: 30px;margin-top: 10px;margin-right: 20px;"></time-axis>
	</view>
</template>

<script>
	import authorCard from "../../components/author_display_card.vue"
	import companyCard from "../../components/company_rep_display_card.vue"
	import requireCard from "../../components/require_display_card.vue"
	import timeAxis from "../../components/time_axis.vue"
	export default {
		data() {
			return {
				dataArray:[
						{
							time:'2020-11-25 17:32:15',
							title:'需求发布',
							// content:'那就看你会计解决',
							active:true
						},{
							time:'2020-11-25 17:32:15',
							title:'专家接单',
							// content:'顺丰到付的',
							active:true
						},{
							time:'2020-11-25 17:32:15',
							title:'订单完成',
							// content:'大幅度发',
							active:true
						},
					]
			}
		},
		methods: {
			
		},
		components: {
			authorCard,
			companyCard,
			requireCard,
			timeAxis,
		}
	}
</script>

<style>
	.title {
		font-weight: 600;
		font-size: 18px;
		margin-top: 5px;
		margin-bottom: 5px;
		margin-left: 10px;
	}

</style>
