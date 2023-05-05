<template>
	<!-- <view class="animated fadeIn">
		<image style="width: 200px; height: 200px;" src="/static/images/toast/no-found-1.jpg"></image>
	</view> -->
	<view class="nothing u-f-ajc animated fadeIn">
		<image src="/static/images/toast/not-found-1.jpg" 
		mode="widthFix"></image>
		<text>该用户已设置内容不可见</text>
	</view>
</template>

<script>
	
	export default {
		data() {
			return {}
		},
		methods: {}
	}
</script>

<style>
	.nothing{
		background: #FFFFFF;
		/* position: absolute; */
		display: flex;
		flex-direction: column;
		align-items: center;
		/* top: 0;
		left: 0;
		right: 0;
		bottom: 0; */
	}
	.nothing image{
		width: 75%;
	}
</style>
