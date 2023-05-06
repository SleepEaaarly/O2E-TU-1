<template>
	<view class="user-space-userinfo">
		<view class="user-space-userinfo-item">
			<view>账号信息</view>
			<view>用户名：{{userinfo.username}}</view>
			<view>邮箱：{{userinfo.email}}</view>
			<view>ID：{{userinfo.id}}</view>
		</view>
		<view class="user-space-userinfo-item">
			
			<view v-if="userinfo.state=='0'">个人信息</view>
			<view v-if="userinfo.state=='4'">专家信息</view>
			<view v-if="userinfo.state=='5'">企业信息</view>
			<template v-if="userinfo.state=='0'">
				<view>身份：普通用户</view>
				
			</template>
			<template v-else-if="userinfo.state=='4'">
				<view>身份：专家</view>
				<view>姓名：{{userinfo.expert_name}}</view>
				<view>所属机构：{{userinfo.expert_organization}}</view>
				<view>职位：{{userinfo.expert_title}}</view>
				<view>擅长领域：{{userinfo.expert_field}}</view>
				<view>个人简介：{{userinfo.expert_scholarprofile}}</view>
				<view>电话：{{userinfo.expert_phone}}</view>
			</template>
			<template v-else-if="userinfo.state=='5'">
				<view>身份：企业</view>
				<view>企业名称：{{userinfo.enterprise_name}}</view>
				<view>企业地址：{{userinfo.enterprise_address}}</view>
				<view>企业官网：{{userinfo.enterprise_website}}</view>
				<view>联系电话：{{userinfo.enterprise_phone}}</view>
				<view>法人代表：{{userinfo.enterprise_legal_representative}}</view>
				<view>注册资本：{{userinfo.enterprise_register_capital/10000}}万元</view>
				<view>企业领域：{{userinfo.enterprise_field}}</view>
				<view>企业介绍：{{userinfo.enterprise_instruction}}</view>
			</template>
			<template v-else>
				<view>身份：普通用户</view>
			</template>
		</view>
	</view>
</template>

<script>
	import t from "../../common/time.js";
	export default {
		props:{
			userinfo:Object,
			authInfo:Object,
		},
		computed:{
			getRegAge(){
				return t.gettime.sumAge(this.userinfo.regtime)
			},
			getXingZuo(){
				return t.gettime.getHoroscope(this.userinfo.birthday)
			}
		},
		methods:{
			clickRate(){	//点击评价链接
				uni.navigateTo({ url: "/pages/my-evaluations/my-evaluations?id="+this.userinfo.id })
			},
		}
	}
</script>

<style scoped>
.user-space-userinfo{
	padding: 0 30upx;
}
.user-space-userinfo-item{
	padding: 20upx 0;
	border-bottom: 1upx solid #EEEEEE;
}
.user-space-userinfo-item>view{
	color: #AAAAAA;
}
.user-space-userinfo-item>view:first-child{
	color: #333333;
	font-size: 35upx;
	padding: 15upx 0;
}
</style>
