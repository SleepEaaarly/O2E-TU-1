<template>
	<view>
		<fui-card :padding="['5rpx','20rpx']" :src="companyLogoPath" :title="companyName" :tag="time" @click.native="gotoRequireReport">
			<view style="margin-top: 20rpx;margin-bottom: 20rpx;">
				<u-row style="margin-left: 20rpx;">
					<text class = "info">
					
					请查收需求
					</text>
					
					
					<text class = "title">《{{title}}》</text>
					
					<text class = "info">的专属报告!</text>
					
				</u-row>
				<u-row>
					
					
					<u-col span = "8">
						
						<text class = "content">
							
							简介：{{intro.toString().replace(/#*.*#/g, '').replace(/[^a-z0-9\u4e00-\u9fa5]/, '').replace(/\n(\n)*( )*(\n)*\n/g, "\n").substring(0, 200)}}
							
						</text>
						
						
						
					</u-col>
					<u-col span = "4">
						
						<image class="logo" src="/static//company.png" style = "height: 90px;width: 90px;margin-left: 10rpx;">
						
					</u-col>
				</u-row>
				 
				
				
			</view>
			
		</fui-card>
		
	</view>
</template>

<script>
	import fuiCard from "@/components/firstui/fui-card/fui-card.vue"
	export default {
		name:"require_message_card",
		components: {
			fuiCard
		},
		data() {
			return {
				
			};
		},
		props:['title','companyName','companyLogoPath','intro','time', 'id'],
		methods: {
			gotoRequireReport() {
				uni.navigateTo({url: '../../pages/require_report/require_report?reportId=' + this.id})
			}
		},
	}
</script>

<style>
	.info {
		font-size: 30rpx;
		font-weight: 600;
	}
	.title {
		font-size: 30rpx;
		font-weight: 600;
		text-overflow:ellipsis;
		overflow:hidden;
		white-space:nowrap;
		max-width: 300rpx;
	}
	.content {
		font-size: 20rpx;
		margin-left: 20rpx;
		color: #606266;
		text-overflow:ellipsis;
		overflow:hidden;
		white-space:nowrap;
		display: -webkit-box;
		-webkit-line-clamp: 4;
		-webkit-box-orient: vertical;
		text-align: left;
		word-wrap: break-word;
		word-break: normal;
	}

</style>