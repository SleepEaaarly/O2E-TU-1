<template>
	<view class="body">
		<block v-for="(item,index) in list" :key="index">
			<home-list-item 
			:item="item"
			:userInfo="userInfo"
			:index="index"></home-list-item>
		</block>
		
		<!-- <view class="uni-list">
			<view class="uni-list-cell uni-list-cell-pd ">
				<view class="uni-list-cell-db">导航栏显示"平台"</view>
				<switch style="transform:scale(0.85)" checked @change="switchChange"/>
			</view>
		</view> -->
		
		<button class="user-set-btn" type="primary" @tap="showActive">退出登陆</button>
		<my-action-sheet :showActionSheet="showActionSheet" @toggleAction="toggleAction"></my-action-sheet>
	</view>
</template>

<script>
	import homeListItem from '../../components/home/home-list-item.vue'
	import myActionSheet from '@/components/common/myActionSheet.vue'
	import { mapMutations,mapState } from 'vuex'
	export default {
		components:{
			homeListItem,
			myActionSheet
		},
		computed:{ ...mapState(['userInfo']) },
		data() {
			return {
				list:[
					{ icon:'',name:'清除缓存',clicktype:'clear',url:'' },
					// { icon:'', name:'导航栏显示"平台"', clicktype:'switchTab' }
				],
				showActionSheet:false,
				button:[
					{	//是否空心
						text: '取消',
						type: 'blue',
						plain: true , 
					}, 
					{ 
						text: '确定',
						type: 'red',
						plain: false ,
					},
				]
			}
		},
		methods: {
			...mapMutations(['setUserInfo','setChatList']),

			showActive(){
				this.showActionSheet = true
			},
			toggleAction(index){
				if(index){
					this.setUserInfo({})
					uni.clearStorageSync('userInfo')
					uni.clearStorageSync('token')
					uni.clearStorageSync('refresh_token')
					this.setChatList([])
					uni.switchTab({ url:'../home/home' })
				}else{
					this.showActionSheet = false
				}
			},

			switchChange: function (e) {
				console.log('switch 发生 change 事件，携带值为', e.detail.value)
			},

		}
	}
</script>

<style>
	@import "../../common/form.css";
</style>
