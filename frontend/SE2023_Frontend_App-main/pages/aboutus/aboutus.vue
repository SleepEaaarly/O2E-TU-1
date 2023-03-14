<template>
	<view>
		<!-- 分享示例 -->
		
		<view class="uni-flex uni-column u-f-ajc">
			<image style="width: 120px; height: 120px" src="@/static/images/logo/PAPDaily.png" 
			></image>
			<view class="text-box" scroll-y="true">
				<text>版本信息：alpha 1.3.1</text>
			</view>
		</view>
		
		<uni-section title="关注我们" type="circle">
			<uni-list :border="false">
				<uni-list-item :border="false" title="关注微信公众号" thumb="/static/images/share/icon_wechat.png"
				 	 thumb-size="lg" rightText="PAPDaily"></uni-list-item>
				<uni-list-item :border="false" title="关注微博" thumb="/static/images/share/icon_sina.png"
				 	 thumb-size="lg" rightText="@PAPDaily"></uni-list-item>
				<uni-list-item :border="false" title="邮箱联系" thumb="/static/images/share/icon_mail.jpeg"
					 thumb-size="lg" rightText="paperdaily2022@163.com"></uni-list-item>
				<uni-list-item showArrow :border="false" title="关注Github" thumb="/static/images/share/icon_github.png"
				 	 thumb-size="lg" rightText="@SE-mcdb"></uni-list-item>
				
			</uni-list>
		</uni-section>
		
		<uni-section title="探索" type="circle">
			<uni-list>	
				<uni-list-item title="使用条款" link clickable @click="onClick('使用条款')"></uni-list-item>
				<uni-list-item title="隐私声明" link clickable @click="onClick('隐私声明')"></uni-list-item>
				<uni-list-item title="开源协议" link clickable @click="onClick('开源协议')"></uni-list-item>
				<uni-list-item title="致谢" link clickable @click="onClick('致谢')"></uni-list-item>
			</uni-list>
		</uni-section>
		
		<!-- 弹出框内容 -->
		<uni-popup ref="tiaokuan" type="dialog">施工中</uni-popup>
		<uni-popup ref="shengming" type="dialog">施工中</uni-popup>
		<uni-popup ref="xieyi" type="dialog">施工中</uni-popup>
		<uni-popup ref="zhixie" type="dialog">施工中</uni-popup>

	</view>
</template>

<script>
	export default {
		data() {
			return {}
		},
		methods: {
			onClick(str){
				switch(str){
					case '使用条款':
						// 通过组件定义的ref调用uni-popup方法 ,如果传入参数 ，type 属性将失效 ，仅支持 ['top','left','bottom','right','center']
					    this.$refs.tiaokuan.open('center')
						break
					case '隐私声明':
						this.$refs.shengming.open('center')
						break
					case '开源协议':
						this.$refs.xieyi.open('center')
						break
					case '致谢':
						this.$refs.zhixie.open('center')
						break
					default:
						break
				}
			}
			
		}
	}
</script>

<style>
	.u-f-ajc{
		justify-content: center;	/* 居中 */
	}
	
	.share {
			/* #ifndef APP-NVUE */
			display: flex;
			/* #endif */
			flex-direction: column;
		}
</style>
