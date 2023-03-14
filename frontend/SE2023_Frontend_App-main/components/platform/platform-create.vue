<template>
	<view>
		<!-- 悬浮按钮 -->
		<uni-fab ref="fab" :pattern="pattern" :content="content" :horizontal="horizontal" :vertical="vertical"
					:direction="direction" @trigger="trigger" @fabClick="fabClick" />
		
		<!-- 操作菜单 -->
		<view class="papar-left-popup-mask" v-show="show" @tap="hide"></view>
		<view class="papar-left-popup" v-show="show">
			<view class="u-f-ac" hover-class="papar-left-popup-h" @tap="addneed">
				<view class="icon iconfont icon-sousuo"></view> 
				发布需求
			</view>
			<!-- <view class="u-f-ac" hover-class="papar-left-popup-h" @tap="clear">
				<view class="icon iconfont icon-qingchu"></view> 
				清除列表
			</view> -->
			<view class="u-f-ac" hover-class="papar-left-popup-h" @tap="manageorder">
				<view class="icon iconfont icon-sousuo"></view> 
				订单管理
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'uni-fab',		//此部分设置uni-fab悬浮按钮的属性
				directionStr: '垂直',
				horizontal: 'right',	//水平对齐方式。left:左对齐，right：右对齐
				vertical: 'bottom',		//垂直对齐方式。bottom:下对齐，top：上对齐
				direction: 'vertical',	//展开菜单显示方式。horizontal:水平显示，vertical：垂直显示
				pattern: {
					//color: '#7A7E83',
					color: '#000000',			//文字默认颜色
					backgroundColor: '#fff',	//背景色
					selectedColor: '#030c4f',	//文字选中时的颜色
					buttonColor: '#030c4f',		//按钮背景色
					iconColor: '#fff'
				},
				is_color_type: false,
				content: [{	//展开菜单内容配置项
						iconPath: '/static/images/icon/post.png',
						selectedIconPath: '/static/images/icon/post-active.png',
						text: '发布',
						active: false
					},
					{
						iconPath: '/static/images/icon/manage.png',
						selectedIconPath: '/static/images/icon/manage-active.png',
						text: '订单',
						active: false
					},
				]
			}
		},
		props:{
			show:Boolean
		},
		methods:{
			hide(){
				this.$emit('hide');
			},
			addneed(){
				this.$emit('addneed');
			},
			manageorder() {
				this.$emit('manageorder');
			},
			//点击fab后的动作
			trigger(e) {
				console.log(e)
				switch(e.index){
					case 0:	//发布
						this.$emit('addneed');
						break;
					case 1:	//管理
						this.$emit('manageorder');
						break;
					default:
						break;
				}
			},
			//点击fab悬浮按钮
			fabClick() {
				// uni.showToast({
				// 	title: '点击了悬浮按钮',
				// 	icon: 'none'
				// })
			},
		}
	}
</script>

<style lang="scss" scoped>
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
	top: 10upx;
	background: #FFFFFF;
	z-index: 2000;
	width: 55%;
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

