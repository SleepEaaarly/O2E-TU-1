<template>
	<view class="user-chat-item animated fadeIn fast">
		
		<view v-if="item.gstime" class="user-chat-time u-f-ajc">{{item.gstime}}</view>
		<view class="user-chat-list u-f" :class="{'user-chat-me':item.isme}">
			<!-- 点击头像跳转到对方主页 -->
			<image v-if="!item.isme" :src="item.userpic" @tap="navUserInfo" mode="widthFix" lazy-load></image>
			<view class="user-chat-list-body">
				<!-- 文字 -->
				<text v-if="item.type=='text'">{{item.message}}</text>
				<!-- 图片 -->
				<image v-if="item.type=='img'" :src="item.message" mode="widthFix" lazy-load></image>
				<!-- 卡片 -->
				<order_message_card v-if="item.type=='report' && item.reportInfo.reportType=='order'"
					:id="item.reportInfo.reportId"
					:title="item.reportInfo.reportTitle"
					:intro="item.reportInfo.reportInfo"
					:time="item.reportInfo.time"
					@click.native="clickOrderReport(12)"
				></order_message_card>
			</view>
			<!-- 点击头像跳转到自己主页 -->
			<image v-if="item.isme" :src="item.userpic" @tap="navUserInfo" mode="widthFix" lazy-load></image>
		</view>
		
	</view>
</template>

<script>
	import order_message_card from '../order_message_card.vue';
	export default {
		components: {
			order_message_card
		},
		props:{
			item:Object,
			index:Number
		},
		methods:{
			clickOrderReport(id) {
				console.log(id)
			},
			navUserInfo(){
				console.log(this.item)
				this.$emit('goToUserInfo',this.item.uid)
			}
		}
	}
</script>

<style scoped>
.user-chat-list{
	padding: 20upx 0;
}
.user-chat-list>image{
	width: 80upx!important;;
	height: 80upx!important;
	/* border-radius: 100%; */
	flex-shrink: 0;
	margin: 0 10upx;
}
.user-chat-list-body{
	position: relative;
	background: #F4F4F4;
	padding: 25upx;
	margin-left: 20upx;
	border-radius: 20upx;
	margin-right: 100upx;
}
.user-chat-list-body:after{
	position: absolute;
	left: -30upx;
	right: 0;
	top: 30upx;
	content: '';
	width: 0;
	height: 0;
	border: 16upx solid #F4F4F4;
	border-color: transparent #F4F4F4 transparent transparent;
}
.user-chat-me{
	justify-content: flex-end;
}
.user-chat-me .user-chat-list-body{
	margin-right: 20upx;
	margin-left: 100upx;
}
.user-chat-me .user-chat-list-body:after{
	left: auto;
	right: -30upx;
	border-color: transparent transparent transparent #F4F4F4;
}
.user-chat-list-body>image{
	max-width: 150upx;
	max-height: 200upx;
}
.user-chat-time{
	padding: 50upx 0;
	color: #a2a2a2;
	font-size: 24upx;
}
</style>
