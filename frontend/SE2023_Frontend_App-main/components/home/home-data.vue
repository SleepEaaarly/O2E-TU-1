<template>
	<view class="home-data u-f-ac animated fadeIn fast" v-if="homedata">
		<block v-for="(item,index) in homedata" :key="index">
			<view class="u-f1 u-f-ajc u-f-column" @tap="goToInfo(index)">
				<view>{{item.num}}</view>{{item.name}}
			</view>
		</block>
	</view>
	<view class="home-data u-f-ac animated fadeIn fast" v-else>
		<block>
			<view class="u-f1 u-f-ajc u-f-column">
				<view>暂无用户交流信息</view>
			</view>
		</block>
	</view>
</template>

<script>
	export default {
		props:{
			homedata:Array
		},
		methods:{
			goToInfo(index){
				this.$emit("goToSpace",index)
			}
		}
	}
</script>

<style scoped>
.home-data{ 
	padding: 20upx 40upx;
}
.home-data>view{
	color: #989898;
}
.home-data>view>view{
	font-size: 32upx;
	color: #333333;
}
</style>
