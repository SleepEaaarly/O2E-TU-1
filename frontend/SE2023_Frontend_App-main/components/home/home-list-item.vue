<template>
	<view class="home-list-item u-f-ac u-f-jsb animated fadeIn fast" 
	hover-class="home-list-hover"
	@tap="clickevent">
		<view class="u-f-ac">
			<view v-if="item.icon"
				class="icon iconfont"
				:class="['icon-'+item.icon]">
			</view>
			{{item.name}}
		</view>
		<view class="icon iconfont icon-jinru"></view>
	</view>
</template>

<script>
	export default {
		props:{
			item:Object,
			index:Number,
			userInfo:Object
		},
		methods:{
			clickevent(){
				switch (this.item.clicktype){
					case 'navigateTo':
						if(this.item.url){ 
							uni.navigateTo({ url:this.item.url }) 
						}
						break
					case 'switchTab':
						if(this.item.url){ 
							uni.switchTab({ url:this.item.url }) 
						}
						break
					case 'showImage':
						 uni.previewImage({
							urls: ['../../static/images/shit/dashangimg.jpg'],
							longPressActions: {
								itemList: ['发送给朋友', '保存图片', '收藏'],
								success: function(data) {
									console.log('选中了第' + (data.tapIndex + 1) + '个按钮,第' + (data.index + 1) + '张图片')
								},
								fail: function(err) {
									console.log(err.errMsg)
								}
							}
						})
						break
					case 'contactme':
						 uni.previewImage({
							urls: ['../../static/images/shit/contactme.jpg'],
							longPressActions: {
								itemList: ['发送给朋友', '保存图片', '收藏'],
								success: function(data) {
									console.log('选中了第' + (data.tapIndex + 1) + '个按钮,第' + (data.index + 1) + '张图片')
								},
								fail: function(err) {
									console.log(err.errMsg)
								}
							}
						})
						break
					case 'clear':
						uni.showModal({
							title: '提示',
							content: '是否要清除缓存？',
							confirmText: '立刻清除',
							success: res => {
								if(res.confirm){
									// let tmp_token = uni.getStorage('token')
									// let tmp_userInfo = uni.getStorage('userInfo')
									// uni.clearStorage()
									// uni.setStorage('token',tmp_token)
									// uni.setStorage('userInfo', tmp_userInfo)
									uni.showToast({ title: '清除缓存成功！', })
								}
							},
						})
						break
				}
			}
		}
	}
</script>

<style scoped>
.home-list-item{
	padding: 20upx;
	border-top: 1upx solid #F4F4F4;
	border-bottom: 1upx solid #F4F4F4;
}
.home-list-item>view:first-child{
	color: #333333;
}
.home-list-item>view:first-child>view{
	margin-right: 10upx;
}
.home-list-item>view:last-child{
	color: #CCCCCC;
}
.home-list-hover{
	background: #f4f4f4;
}
</style>
