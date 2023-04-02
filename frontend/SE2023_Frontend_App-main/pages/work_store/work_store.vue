<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon @click="navToEntry" name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">成果库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="candidates" placeholder="请选择类型" v-model="city" class="work_combox" :border="false"></uni-combox>
			<uni-datetime-picker type="date" :clear-icon="false" v-model="single" @maskClick="maskClick" class = "work_combox"/>
		</u-row>
		
		<view style="background-color: #f2f2f2;margin-top: 10px;padding-top: 10px;padding-bottom: 10px;">
			<!-- <expert-card></expert-card> -->
		</view>
		
	</view>
</template>

<script>
	import workCard from "@/components/work_display_card.vue"
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			navToEntry(){
				console.log('back to entry')
				uni.switchTab({
					url: '../entry/entry',
				})
			},
			maskClick(){
				
			}
		},
		components : {
			workCard
		}
	}
</script>

<style>
	.work_combox {
		width: 152px;
		border-radius: 15px;
		background-color: #f2f2f2;
		margin-right: 10px;
		
	}

</style>
