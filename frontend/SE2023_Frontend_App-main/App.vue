<script>
    import {mapMutations,mapActions} from 'vuex'
	import {
		tokenRefresh
	} from "@/api/login.js";
	import{
		picUrl
	} from '@/api/common.js'
	export default {
		async onLaunch() {
			// 网路监听（用户目前断网，切换wifi）
			this.lib.NetWork.On();
			let data;
			let chatList;
			try{
				 chatList =JSON.parse(uni.getStorageSync('chatList'))
				 if(!uni.getStorageSync("fuid")){
					 uni.setStorageSync('fuid',Math.random()+"")
				 }
				 	this.setChatList(chatList||[])
			}catch(e){
			
			}
			
			// 更新检测
		},
		async onShow () {
			console.log('App Show')
			let res ={};
			if(uni.getStorageSync('refresh_token')){
				res = await tokenRefresh()
			}
			if(res && res.code==401){
				uni.clearStorageSync('token')
				uni.clearStorageSync('chatList')
				this.setChatList([])
				this.setUserInfo({})
				this.$http.href("pages/login/login")
			}else{
				if(res&&res.access_token){
					uni.setStorageSync('token',res.access_token)
					res.userInfo.userpic=picUrl+res.userInfo.userpic
					this.setUserInfo(res.userInfo)
					//this.$store.dispatch('setSocketV',res.userInfo.id)
					this.$http.href("pages/home/home")
				}else{
					// this.$http.href("pages/login/login")
				}		
			}
		},
		// 解决刷新页面vuex内数据丢失
		created(){
			//在页面加载时读取sessionStorage里的状态信息
			let sessionStorage = window.sessionStorage;
			if (sessionStorage.getItem("store") ) {
			  this.$store.replaceState(Object.assign({}, this.$store.state,JSON.parse(sessionStorage.getItem("store"))))
			}

			//在页面刷新时将vuex里的信息保存到sessionStorage里
			window.addEventListener("beforeunload",()=>{
			  sessionStorage.setItem("store",JSON.stringify(this.$store.state))
			})
		},
		onHide: function () {
			console.log('App Hide')
		},
		methods:{
			...mapMutations(['setUserInfo','setChatList'])
		}
	}
</script>

<style>
	/*每个页面公共css */
	/* 引入官方css库 */

	@import './common/uni.css';
	/* 引入自定义图标库 */
	@import './common/icon.css';
	/* 引入自定义图标库 */
	@import './common/ssk.css';
	/* 引入动画库 */
	@import './common/animate.css';
	/* 公共样式 */
	@import './common/common.css';
	@import './static/style/thorui-extend.css';
	
	/* 迭代:引入自定义图标库。wqnmlgbctnndsbwy根本不好使 */
	/* @import "./static/font2/iconfont.css"; */
</style>
