<template>
	<view style="margin-bottom: 10px;">
		<fui-card :padding="['5rpx','20rpx']" full :src = "authorLogoPath" 
		:title="author" :tag="date">
			<u-row>
				
				<text class = "workTitle">{{title}}</text>
				<u-tag v-if="area" :text="area" plain plainFill size="mini" style="margin-left: 10px;"> </u-tag>
				<u-tag :text="period" plain plainFill size="mini" type="success" style="margin-left: 10px;"> </u-tag>
			</u-row>
			
			<u-row style="margin-bottom: 10px;">
				<text class = "workSummary">{{intro}}</text>
				<image class="logo" :src="workLogoPath" style = "height: 80px;width: 80px;">
				</image>
				
			</u-row>
			
			<!-- <view class="fui-card__content fui-padding">这是一个基础卡片的示例，此处为自定义内容区域，自行控制内容样式。</view> -->
		
		</fui-card>
		
		<!-- <fui-card :src="'/static/head.jpg'"></fui-card> -->
		
	</view>
</template>

<script>
	export default {
		name:"work_display_card",
		data() {
			return {
				
			};
		},
	props:['authorLogoPath','author','date','title','area','intro','workLogoPath', 'period']
	}
</script>

<style>
	
	.workTitle {
		font-weight: 600;
		margin-left: 20px;
		margin-top: 5px;
		margin-bottom: 5px;
	}
	.workSummary{
		margin-left: 10px;
		font-size: 10px;
		color:#333333;
		width: 70%;
	}

</style>