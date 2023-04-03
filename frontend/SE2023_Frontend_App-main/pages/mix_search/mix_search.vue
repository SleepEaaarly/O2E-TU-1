<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;">
			<u-icon name="arrow-left" size="28" ></u-icon>
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</u-row>
		
		
		<view style="background-color: #F7F7F7;margin-top: 10px; margin-bottom: 0px;padding-top: 8px;">
			<!-- 专家和企业结果 -->
			<u-scroll-list>
				 <u-col span="4">
					 <personCard :name="'甜胖妮'" :logoPath="'/static//head.jpg'" :type="'专家'"></personCard>
				    
				</u-col>
				<u-col span="4">
					<personCard></personCard>
				    
				</u-col>
				<u-col span="4">
					<personCard></personCard>
				    
				</u-col>
<!-- 				<personCard></personCard>
				<personCard></personCard>
				<personCard></personCard>
				<personCard></personCard> -->
			</u-scroll-list>
			
			
			
			
		</view>
		<view style="background-color: #F7F7F7; margin-bottom: 0%; padding-bottom: 10px">
			<!-- 专家和企业结果 -->
			
			
			<work-card :authorLogoPath="'/static/head.jpg'" :author="'佛系甜胖妮'"
			:date="'2023-3-30 21:41'" :title="'如何一个月速成雅思'"
			:area="'英语学习'"
			:intro="'其实一个月速成不了，我感觉我要寄了。还是多花点时间准备吧。'"
			:workLogoPath="'/static//logo.png'"></work-card>
			
			
			
			
		</view>

	</view>
</template>

<script>
	import personCard from "@/components/search_person_card.vue"
	import workCard from '@/components/work_display_card.vue'
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			
		},
		components: {
			personCard,
			workCard
		}
	}
</script>

<style>

</style>
