<template>
	<view>
		<!-- 未登录 -->
		<template  v-if="userInfo && !userInfo.id">
			<view class="u-f-ajc">登陆PaperDaily，体验更多功能</view>
			<!-- 第三方登陆 -->
			<view class="u-f-ajc" @tap="openLogin">账号密码登陆 <view class="icon iconfont icon-jinru"></view>
			</view>
		</template>
		
		<template v-else>
			<template v-if="userInfo.type=='0'">
				<!-- 普通用户 -->
				<view class="u-f-ajc" @tap="openLogin">您目前是普通用户，认证后可体验更多功能</view>
				<tui-button :size="30" height="70rpx" @click="openExpertCertificate" :plain="true" type="blue">专家认证 <tui-icon name="arrowright" :size="30" :bold="true"></tui-icon></tui-button>
				<tui-button :size="30" height="70rpx" @click="openEnterpriseCertificate" :plain="true" type="green">企业认证 <tui-icon name="arrowright" :size="30" :bold="true"></tui-icon></tui-button>
			</template>
			
			<!-- 个人头像、信息 -->
			<home-info :homeinfo="homeinfo"></home-info>
			
			<!-- (主页+评论+收藏)数据 -->
			<home-data @goToSpace="goToSpace" :homedata="homedata"></home-data>
			
			<uni-section title="探索" type="circle">
				<uni-list :border="false">
					<uni-list-item class="explore" v-if='userInfo.type==4' :border="false" :show-extra-icon="true" clickable :extra-icon="rateIcon" title="最近收到的评价" link @click="clickRate" />
					<uni-list-item class="explore" v-else-if='userInfo.type==5' :border="false" :show-extra-icon="true" clickable :extra-icon="rateIcon" title="最近评价" link @click="clickRate" />
					
					<uni-list-item class="explore" :border="false" :show-extra-icon="true" clickable link :extra-icon="inviteIcon" title="邀请好友享福利" rightText="立享首单补贴" @click="clickLink"/>
					
					<uni-list-item class="explore" :border="false" :show-extra-icon="true" clickable :extra-icon="feedbackIcon" title="帮助与反馈" link to="/pages/feedback/feedback" @click="onClick"/>
					
					<uni-list-item class="explore" :border="false" :show-extra-icon="true" clickable :extra-icon="myFeedbackIcon" title="反馈查收" 
					rightText="查看反馈信息" link to="/pages/feedback/feedback_return" @click="onClick" />
						
					<uni-list-item class="explore" :border="false" :show-extra-icon="true" clickable :extra-icon="questionIcon" title="常见问题" 
					rightText="常见问题解答" link to="/pages/common_question/common_question" @click="onClick" />
					
					<uni-list-item class="explore" :border="false" :show-extra-icon="true" clickable :extra-icon="aboutIcon" title="关于" link to="/pages/aboutus/aboutus" @click="onClick" />
					
					
				</uni-list>
			</uni-section>
			
			<button class="user-set-btn" type="primary" @tap="showActive" v-show="false">退出登陆</button>
			
			<!-- 分享链接弹窗 -->
			<uni-popup ref="shareLink" type="share">
				<uni-popup-share title="分享到" @select="select"></uni-popup-share>
			</uni-popup>
			
		</template>
	</view>
</template>

<script>
	import homeListItem from '../../components/home/home-list-item.vue'
	import homeInfo from '../../components/home/home-info.vue'
	import otherLogin from '../../components/home/other-login.vue'
	import homeData from '../../components/home/home-data.vue'
	import { getUserProfile, } from '@/api/home.js'
	
	import { picUrl } from '@/api/common.js'
	
	import { webUrl } from '../../common/config.js'
	import {
		mapState,
		mapMutations
	} from 'vuex'
	export default {
		components: {
			homeListItem,
			homeInfo,
			otherLogin,
			homeData
		},
		computed: { ...mapState(['userInfo']) },
		onShow() {
			console.log(this.userInfo.email)
			this.initDat()
		},
		onLoad(){
			
		},
		onReady() {
			//this.initDat()
		},
		created() {

		},
		async mounted() {
			this.initDat()
			if (this.userInfo.id) {
				this.homeinfo.userpic = this.userInfo.userpic
				this.homeinfo.username = this.userInfo.username
				this.homeinfo.email = this.userInfo.email
				this.homeinfo.type = this.userInfo.type
				if (!this.islogin) {
					this.initDat()
				}
			} else {
				this.homedata[0].num = 0
				this.homedata[1].num = 0
				this.homedata[2].num = 0
				this.islogin = false
			}
		},
		data() {
			return {
				rateUrl:'',
				islogin: false,
				homeinfo: {
					userpic: this.userInfo ? this.userInfo.userpic : '',
					username: this.userInfo ? this.userInfo.username : '',
					totalnum: 0,
					todaynum: 0,
					type: 0,
				},
				homedata: [
					{
						name: '主页',
						num: 0
					},
					{
						name: '评论',
						num: 0
					},
					{
						name: '收藏',
						num: 0
					},
				],
				//此处使用配色方案:https://coolors.co/palette/ff595e-ffca3a-8ac926-1982c4-6a4c93
				rateIcon: {
					color: '#ff595e',
					size: '22',
					type: 'chat-filled'
				},
				inviteIcon: {
					color: '#ffca3a',
					size: '22',
					type: 'gift-filled'
				},
				feedbackIcon: {
					color: '#8ac926',
					size: '22',
					type: 'paperplane-filled'
				},
				myFeedbackIcon: {
					color: '#1982c4',
					size: '22',
					type: 'redo-filled'
				},
				questionIcon: {
					color: '#6a4c93',
					size: '22',
					type: 'help-filled'
				},
				aboutIcon: {
					color: '#242423',
					size: '22',
					type: 'gear-filled'
				},
				showSuccess: false
			}
		},
		// 监听下拉刷新
		async onPullDownRefresh() {
			await this.initDat()
			uni.stopPullDownRefresh()
		},
		onNavigationBarButtonTap(e) {
			if (this.userInfo.id) {
				if (e.index === 0) {
					uni.navigateTo({ url: '../user-set/user-set', })
				}
			} else {
				uni.navigateTo({ url: '../login/login', })
			}
		},
		methods: {
			...mapMutations(['setUserInfo']),
			openLogin() {
				uni.navigateTo({ url: '../login/login' })
			},
			openEnterpriseCertificate() {
				uni.navigateTo({ url: '../certificate-enterprise/certificate-enterprise?uid=' + this.userInfo.id })
			},
			openExpertCertificate() {
				uni.navigateTo({ url: '../certificate-expert/certificate-expert?uid=' + this.userInfo.id })
			},
			async initDat() {
				//console.log(this.homeinfo.userpic)
				if (this.userInfo && this.userInfo.id) {
					let userProfile = await getUserProfile()
					
					let temp = this.userInfo
					temp.type = userProfile.type
					this.setUserInfo(temp)
					//console.log(userProfile.userpic)
					this.homeinfo.username=userProfile.username
					this.homeinfo.total_like = userProfile.total_like
					this.homeinfo.total_post = userProfile.total_post
					this.homeinfo.total_collect = userProfile.total_mycollect
					this.homeinfo.userpic = picUrl+userProfile.userpic
					this.homeinfo.email = userProfile.email
					this.homeinfo.type = userProfile.type
					this.homedata[0].num = userProfile.total_post
					this.homedata[1].num = userProfile.total_comment
					this.homedata[2].num = userProfile.total_mycollect
					this.islogin = true
					this.rateUrl='/pages/my-evaluations/my-evaluations?id='+this.userInfo.id
					//console.log(this.homeinfo.userpic)
				}
			},
			print(){
				console.log(this.userInfo.id)
			},
			goToSpace(index) {
				switch (index) {
					case 0:
						this.$http.href('../../pages/user-space/user-space?uid=' + this.userInfo.id)
						break
					case 1:
						this.$http.href('../../pages/user-comment/user-comment?uid=' + this.userInfo.id)
						break
					case 2:
						this.$http.href('../../pages/user-collect/user-collect?uid=' + this.userInfo.id)
						break
				}
			},
			
			onClick(){
				
			},
			clickLink(){	//点击分享链接
				this.$refs.shareLink.open('center')
			},
			clickRate(){	//点击评价链接
				uni.navigateTo({ url: this.rateUrl })
			},
		}
	}
</script>

<style lang="scss" scoped>
	@import "../../common/form.css";	//引入主题色
	
	.yanse{
		color: #ff0000;
	}
	.home-list {
		padding: 20upx;
	}

	.home-adv {
		padding: 20upx;
	}

	.home-adv>image {
		border-radius: 20upx;
		height: 150upx;
	}
	.guanggao{
		width: 100%;
	}
	.explore {
		height: 110upx;
	}
</style>
