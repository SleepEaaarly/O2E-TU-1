<template>
	<view>
		<!-- 个人主页右上方-操作菜单 -->
		<view class="papar-left-popup-mask" v-show="show" @tap="hidepopup"></view>
		<view class="papar-left-popup" v-show="show">
			<view class="u-f-ac" hover-class="papar-left-popup-h" @tap="sixin">
				<view class="icon iconfont icon-sousuo"></view> 
				私信
			</view>
			<view class="u-f-ac" hover-class="papar-left-popup-h" @tap="fenxiang">
				<view class="icon iconfont icon-qingchu"></view> 
				分享
			</view>
			<view class="u-f-ac" hover-class="papar-left-popup-h" @tap="heimingdan">
				<uni-icons type="eye-slash" size="22"></uni-icons>
				加入黑名单
			</view>
			<view class="u-f-ac" hover-class="papar-left-popup-h" @tap="jubao">
				<uni-icons type="trash" size="22"></uni-icons>
				举报
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		props:{
			show:Boolean
		},
		methods:{
			hidepopup(){
				this.$emit('hide');
			},
			// 私信
			sixin(){
				this.$emit('sixin');
			},
			// 分享
			fenxiang(){
				this.$emit('fenxiang');
			},
			// 加入黑名单
			heimingdan(){
				this.$emit('heimingdan');
			},
			// 举报
			jubao(){
				this.$emit('jubao');
			},
		}
	}
</script>

<style>
.papar-left-popup-mask{
	position: fixed;
	right: 0;
	left: 0;
	top: 0;
	bottom: 0;
	z-index: 1999;
}
.papar-left-popup{
	position: fixed;
	right: 0;
	top: 100upx;
	background: #FFFFFF;
	z-index: 2000;
	width: 45%;
	box-shadow: 1upx 1upx 20upx 2upx #CCCCCC;
}
.papar-left-popup>view{
	padding: 20upx;
	font-size: 35upx;
}
.papar-left-popup>view>view{
	margin-right: 10upx;
	font-weight: bold;
}
.papar-left-popup-h{
	background: #EEEEEE;
}
</style>
