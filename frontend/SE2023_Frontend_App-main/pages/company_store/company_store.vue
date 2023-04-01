<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">企业库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="candidates" placeholder="请选择地区" v-model="city" class="company_combox" :border="false"></uni-combox>
			<uni-combox :candidates="candidates" placeholder="请选择领域" v-model="city" class="company_combox" :border="false"></uni-combox>
			
		</u-row>
		
		<view style="background-color: #f2f2f2;margin-top: 10px;padding-top: 10px;padding-bottom: 10px;">
			<!-- <expert-card></expert-card> -->
			<company-card :title="'段姐的家'" :address="'北京市朝阳区'" :logoPath="'/static//logo.png'" :area="'摆烂学'"></company-card>
		</view>
		
	</view>
</template>

<script>
	import companyCard from "@/components/company_display_card.vue"
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			
		},
		components : {
			companyCard
		}
	}
</script>

<style>
	.company_combox {
		width: 152px;
		border-radius: 15px;
		background-color: #f2f2f2;
		margin-right: 10px;
		
	}

</style>
