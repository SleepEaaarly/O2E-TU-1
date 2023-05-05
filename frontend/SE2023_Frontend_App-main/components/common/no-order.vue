<template>
	<view class="animated fadeIn">
		<tui-no-data imgUrl="/static/images/toast/no-data02.png" btnText="去逛逛" @click="goToExplore">
			<text class="tui-color__black">暂无订单~</text>
			<!--如果需要自定义按钮，可在插槽中自定义，不使用默认按钮-->
		</tui-no-data>
	</view>
</template>

<script>
	import tuiNoData from "@/components/thorui/tui-no-data/tui-no-data"
	
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			goToExplore(){
				//console.log("去！")
				this.$emit("goToExplore")
			},
			
		}
	}
</script>

<style scoped>
	@import "@/common/form.css";	/* 引入全局样式？ */
</style>
