<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon @click="navToEntry" name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">成果库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" v-model="searchText"></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="area_list" placeholder="领域" v-model="chosen_area" class="work_combox" :border="false"></uni-combox>
			<uni-combox :candidates="period_list" placeholder="技术成熟度" v-model="chosen_period" class="work_combox" :border="false"></uni-combox>
		</u-row>
		
		<block v-for="(item, index1) in recommendList.list" :key="index1">
			<work-card
			@click.native="workDetail(item)"  
			:authorLogoPath="item['authorLogoPath']" 
			:workLogoPath="item['workLogoPath']" 
			:author="item['author']"
			:title="item['title']"
			:date="item['date']"
			:area="item['field']"
			:intro="item['abstract']"
			:period="item['period']"
			:index="index1"></work-card>
		</block> 
	</view>
</template>

<script>
import workCard from "@/components/work_display_card.vue"
import { getWorkList } from "@/api/work_store.js"
	export default {
		data() {
			return {
				chosen_period: '',
				chosen_area: '',
				searchText: '',
				cur_page: 1,
				finish_getting: false,
				area_list: [
					"信息技术", "装备制造", "新材料", "新能源", "节能环保", "生物医药", "科学创意", "检验检测", "其他"
				],
				period_list: [
					"实验室", "样品", "中试", "产业化"
				],
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					list: [
						{
							'authorLogoPath': '/static/expert_test_head_logo (2).png',
							'author': 'Expert1',
							'date': '2023-3-30 21:41',
							'title': '超高分子量聚乙烯的研发制备',
							'field': '新材料',
							'abstract': '一种线型结构的具有优异综合性能的热塑性工程塑料',
							'workLogoPath': '/static/super_quantity_material.png',
							"period": "中试",
						},
						{
							'authorLogoPath': '/static/expert_test_head_logo (1).png',
							'author': 'Expert2',
							'date': '2023-3-30 21:50',
							'title': '环境友好大豆蛋白质材料改性开发',
							'field': '生物医药',
							'abstract': '该项目通过与其他生物可降解材料的共混，以及与纳米粒子的复合来得到廉价、加工性能良好、力学及防水性能改善的大豆蛋白质环境友好材料。',
							'workLogoPath': '/static/soybean_improvement.png',
							"period": "产业化",
						},
						{
							"title": 'A Summary of ML',
							"author": '占瑞乙',
							'field': '科学创意',
							"expert_title": '本科生',
							"abstract": 'Here is a summary of some of the most commonly used methods in machine learning.',
							"expert_organization": '北京航空航天大学',
							"authorLogoPath": '/static/head_zry_fox.jpg',
							"work_id": '',
							"expert_id": '',
							"user_id": '',
							'workLogoPath': '/static/work_logo_test_zry.png',
							"work_pic": '/static/ML_Notes.png' ,
							"expert_mail": "iszry@foxmail.com",
							'date': '2023-4-4 16:32',
							"period": "实验室里",
						}
					]
				},
			}
		},
		onShow() {		//页面加载,一个页面只会调用一次
			console.log('works-onShow()')
			this.finish_getting = false
			this.recommendList.list = []
			this.requestData()
		},
		onLoad() {		//页面显示,每次打开页面都会调用一次
			console.log('works-onLoad()')
		},
		watch: {
			chosen_area(newVal, oldVal) {
				this.requestData()
			},
			chosen_period(newVal, oldVal) {
				this.requestData()
			},
			searchText(newVal, oldVal) {
				this.requestData()
			}
		},
		onReachBottom(res) {
			// console.log("页面滚动了")
			this.requestData()
			uni.$emit('onReachBottom', res.scrollTop);
		},
		methods: {
			navToEntry(){
				// console.log('back to entry')
				uni.switchTab({
					url: '../entry/entry',
				})
			},
			maskClick(){
				
			},
			workDetail(work) {
				// console.log(work['result_id'])
				// getExpertByID
				uni.navigateTo({
				 	url: '../../pages/work_detail/work_detail?rid=' + work['result_id'],
				 })
			},
			async requestData() {
				if(this.finish_getting){
					console.log('finish getting data')
					return
				}
				try {
					let paras = {
						"field": this.chosen_area,
						"period": this.chosen_period,
						"key_word": this.searchText,
						"page": this.cur_page
					}
					var work_list = await getWorkList(paras)
					if(work_list.length===0||work_list==null||work_list==[]||work_list=={}){
						this.finish_getting = true
					}
					this.recommendList.list = this.recommendList.list.concat(work_list)
					this.cur_page = this.cur_page + 1
				} catch (e) {
					console.log(e)
					return
				}
			},
		},
		components : {
			workCard
		}
	}
</script>

<style>
	.work_combox {
		width: 152px;
		border-radius: 15px;
		background-color: #f2f2f2;
		margin-right: 10px;
		
	}

</style>
