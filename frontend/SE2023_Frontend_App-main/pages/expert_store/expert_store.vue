<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">专家库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="candidates" placeholder="请选择机构" v-model="city" class="expert_combox" :border="false"></uni-combox>
			<uni-combox :candidates="candidates" placeholder="请选择领域" v-model="city" class="expert_combox" :border="false"></uni-combox>
			<uni-combox :candidates="candidates" placeholder="请选择职称" v-model="city" class="expert_combox" :border="false"></uni-combox>
		</u-row>
		
		<view style="background-color: #f2f2f2;margin-top: 10px;padding-top: 10px;padding-bottom: 10px;">
			<expert-card :name="'段姐废物'" 
			:title="'小废物'" :institution="'北京航空航天大学'"
			:mail="'duansangni@hhhhh.com'"
			:logoPath="'/static//logo.png'"></expert-card>
		</view>
		
	</view>
	
</template>

<script>
	import expertCard from "@/components/expert_display_card.vue"
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			
		},
		components : {
			expertCard
		}
	}
</script>

<style>
	.expert_combox {
		width: 95px;
		border-radius: 15px;
		background-color: #f2f2f2;
		margin-right: 5px;
		
	}

</style>
