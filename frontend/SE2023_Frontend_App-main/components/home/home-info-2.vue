<template>
	<view class="home-info u-f-ac animated fadeIn fast">
		
		<image :src="homeinfo.userpic" mode="widthFix" lazy-load></image>
		<view class="u-f1" @tap="goToSpace">
			<view>{{homeinfo.username}}</view>
			<template v-if="homeinfo.type=='4'">
				<view>
					<uni-icons type="checkbox" color="#0A98D5"></uni-icons>
					{{homeinfo.expert_name}}
				</view>
			</template>
			<template v-else-if="homeinfo.type=='5'">
				<view>
					<uni-icons type="checkbox" color="#0A98D5"></uni-icons>
					{{homeinfo.enterprise_name}}
				</view>
			</template>
			<template v-else-if="homeinfo.type=='1'">
				<view>专家身份认证中</view>
			</template>
			<template v-else-if="homeinfo.type=='2'">
				<view>企业身份认证中</view>
			</template>
			<template v-else-if="homeinfo.type=='3'">
				<view>封禁中</view>
			</template>
			<template v-else>
				<view>普通用户</view>
			</template>
			<view>
				<!-- <uni-icons type="email"></uni-icons>
				{{homeinfo.email}} -->
			</view>
			<view>
				<uni-icons type="location"></uni-icons>
				<text>属地：{{homeinfo.enterprise_address}}</text>
			</view>
		</view>
		
		<view class="icon iconfont icon-jinru"></view>
		
	</view>
	
</template>

	

<script>
	export default {
		props:{ homeinfo:Object },
		methods:{
			goToSpace(){
				uni.navigateTo({ url: '../user-space/user-space?uid=' + this.homeinfo.id, })
			},
			openEnterpriseCertificate() {
				uni.navigateTo({ url: '../certificate-enterprise/certificate-enterprise', })
			},
			openExpertCertificate(){
				uni.navigateTo({ url: '../certificate-expert/certificate-expert', })
			},
		}
	}
</script>

<style scoped>
.home-info{
	padding: 20upx 40upx;
}
.home-info>image{
	flex-shrink: 0;
	width: 100upx!important;
	height: 100upx !important;
	border-radius: 100%;
	margin-right: 15upx;
}
.home-info>view:first-of-type>view:first-child{
	font-size: 32upx;
}
.home-info>view:first-of-type>view:nth-of-type(2){
	font-size: 26upx;
	color: #0A98D5;
}
.home-info>view:first-of-type>view:nth-of-type(3){
	color: #000000;
}
.home-info>view:first-of-type>view:last-child{
	color: #BBBBBB;
}
.home-info>view:last-of-type{
	height: 100%;
}

</style>
