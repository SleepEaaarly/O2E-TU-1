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
				<image class="logo" :src="workLogoPath" style = "max-height: 80px;max-width: 80px;">
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
		text-overflow:ellipsis;
		overflow:hidden;
		white-space:nowrap;
		
		
		width: 90%;
	}
	.workSummary{
		margin-left: 10px;
		font-size: 10px;
		color:#333333;
		width: 70%;
		
		/* text-overflow:ellipsis;
		overflow:hidden; */
		/* white-space:nowrap; */
		
		/* line-height: 1.5em; 
		max-height: 4.5em; 
		text-overflow:ellipsis;
		overflow:hidden;
		white-space: nowrap; */
		display: -webkit-box; /* 使用webkit内核的盒子布局 */
		-webkit-line-clamp: 3; /* 设置显示行数为4行 */
		-webkit-box-orient: vertical; /* 设置盒子垂直排列 */
		overflow: hidden; /* 超出部分隐藏 */
		text-overflow: ellipsis; /* 超出部分显示省略号 */
		
	}

</style>