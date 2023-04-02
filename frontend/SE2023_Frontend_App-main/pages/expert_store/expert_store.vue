<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon @click="navToEntry" name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">专家库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="institution_list" placeholder="请选择机构" v-model="chosen_institution" class="expert_combox" :border="false"></uni-combox>
			<uni-combox :candidates="area_list" placeholder="请选择领域" v-model="chosen_area" class="expert_combox" :border="false"></uni-combox>
			<uni-combox :candidates="title_list" placeholder="请选择职称" v-model="chosen_title" class="expert_combox" :border="false"></uni-combox>
		</u-row>
		
<!-- 		<view style="background-color: #f2f2f2;margin-top: 10px;padding-top: 10px;padding-bottom: 10px;">
			<expert-card :name="'段姐废物'" 
			:title="'小废物'" :institution="'北京航空航天大学'"
			:mail="'duansangni@hhhhh.com'"
			:logoPath="'/static//logo.png'"></expert-card>
		</view> -->
		<expert-card :name="'段姐废物'"
		:title="'小废物'" :institution="'北京航空航天大学'"
		:mail="'duansangni@hhhhh.com'"
		:logoPath="'/static//logo.png'"></expert-card>
		<block v-for="(item, index1) in recommendList.list" :key="index1">
			<expert-card
			@click.native="expertDetail(item)"  
			:logoPath="item['authorLogoPath']" 
			:name="item['author']"
			:title="item['title']"
			:mail="item['mail']"
			:institution="item['institution']"
			:index="index1"></expert-card>
		</block> 
	</view>
	
</template>

<script>
	import expertCard from "@/components/expert_display_card.vue"
	export default {
		props: {
			chosen_institution: String,
			chosen_area: String,
			chosen_title: String
		},
		data() {
			return {
				institution_list: [
					'北航'
				],
				area_list: [
					'信息技术'
				],
				title_list: [
					'副教授'
				],
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					list: [
						{
							'authorLogoPath': '/static/head.jpg',
							'author': 'Expert1',
							'mail': 'iszry@foxmail.com',
							'title': '副教授',
							'institution': '北京航空航天大学',
							'intro': '一种线型结构的具有优异综合性能的热塑性工程塑料',
							'workLogoPath': '/static//logo.png',
						},
						{
							'authorLogoPath': '/static/head.jpg',
							'author': 'Expert2',
							'mail': 'iszry@foxmail.com',
							'title': '副教授',
							'institution': '北京航空航天大学',
							'intro': '该项目通过与其他生物可降解材料的共混，以及与纳米粒子的复合来得到廉价、加工性能良好、力学及防水性能改善的大豆蛋白质环境友好材料。',
							'workLogoPath': '/static//logo.png',
						}
					]
				},
			}
		},
		methods: {
			navToEntry(){
				console.log('back to entry')
				uni.switchTab({
					url: '../entry/entry',
				})
			},
			expertDetail(expert){
				console.log(expert['author'])
			}
		},
		components : {
			expertCard
		}
	}
</script>

<style>
	.expert_combox {
		width: 95px;
		border-radius: 15px;
		background-color: #f2f2f2;
		margin-right: 5px;
		
	}

</style>
