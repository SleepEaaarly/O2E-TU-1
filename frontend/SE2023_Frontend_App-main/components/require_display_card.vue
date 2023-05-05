<template>
	<view>
		<fui-card :footer-line="false" :showBorder="true" style ="height: 100px;">
			<u-row style="margin-bottom: 0%;">
				<u-col span="3">
				    <image class="logo" :src="logoPath" 
					style = "height: 70px;width: 70px;margin-left: 10px;margin-top: 15px;border-radius: 20px;">
				</u-col>
				<u-col span="9">
					<u-row style="margin-top: 20px;">
						<u-col span="7">
							<u-row><text class = "requireTitle">{{name}}</text></u-row>		
						</u-col>
						<u-col span="5"></u-col>
						</u-row>
						<u-row style="margin-top: 10px;margin-bottom: 0%;margin-left: 5px;">	
							<!-- <u-tag :text="address" plain size="mini" type="error"> </u-tag> -->
							<u-tag :text = "area" plain size="mini" style="margin-left: 20px;"> </u-tag>	
						</u-row>
				</u-col>
			</u-row>
			
			</fui-card>
			<view style="
			margin-top: 10px;background-color: aliceblue;width: 650rpx;margin-left: 35rpx;height: auto;
			border-left:8rpx solid cornflowerblue;
			background-color: aliceblue;padding-top: 10rpx;padding-left: 20rpx;padding-bottom: 10rpx;">
				<text class="intro">{{intro}}</text>
			</view>
			
			
			<u-row style="margin-top: 10px;margin-left: 15px;">
				<u-col span = "3">
					<u-row>
						<u-icon name="star-fill"></u-icon>
					<text class="keyword-title">关键词：</text>
					</u-row>
					
					
				</u-col>
				<u-col span = "9">
					<text class="keyword">{{keyword}}</text>
				</u-col>
				
				
			</u-row>
	</view>
</template>

<script>
	export default {
		name:"require_display_card",
		data() {
			return {
				
			};
		},
		props:['name','intro','logoPath','keyword','area']
	}
</script>

<style>
	.requireTitle {
			font-weight: 600;
			margin-left: 10px;
			margin-top: 5px;
			margin-bottom: 5px;
			
		}
	.keyword-title {
		font-size: 15px;
		color:dimgray;
	}
	.keyword {
		font-size: 13px;
		color:dimgray;
		width: 250px;
		/* background-color: aliceblue; */
	}

</style>