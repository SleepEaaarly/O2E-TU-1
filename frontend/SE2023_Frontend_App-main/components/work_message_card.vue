<template>
	<view>
		<fui-card :padding="['5rpx','20rpx']" :src="expertLogoPath" :title="expertName" :tag="time">
			<view style="margin-top: 20rpx;margin-bottom: 20rpx;">
				<u-row style="margin-left: 20rpx;">
					<text class = "info">
					
					请查收成果
					</text>
					
					
					<text class = "title">《{{title}}》</text>
					
					<text class = "info">的专属报告!</text>
					
				</u-row>
				<u-row>
					
					
					<u-col span = "8">
						
						<text class = "content">
							
							简介：{{intro}}
							
						</text>
						
						
						
					</u-col>
					<u-col span = "4">
						
						<image class="logo" src="/static///Designer _Flatline.png" style = "height: 90px;width: 90px;margin-left: 10rpx;">
						
					</u-col>
				</u-row>
				 
				
				
			</view>
			
		</fui-card>
	</view>
</template>

<script>
	export default {
		name:"work_message_card",
		data() {
			return {
				
			};
		},
		props:['title','expertName','expertLogoPath','intro','time']
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
	}

</style>