<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon @click="navToEntry" name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">专家库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" v-model="searchText" :showAction = "false" ></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="institution_list" placeholder="机构" v-model="chosen_institution" class="expert_combox" :border="false"></uni-combox>
			<uni-combox :candidates="area_list" placeholder="领域" v-model="chosen_area" class="expert_combox" :border="false"></uni-combox>
			<uni-combox :candidates="title_list" placeholder="头衔" v-model="chosen_title" class="expert_combox" :border="false"></uni-combox>
		</u-row>
		
<!-- 		<view style="background-color: #f2f2f2;margin-top: 10px;padding-top: 10px;padding-bottom: 10px;">
			<expert-card :name="'段姐废物'" 
			:title="'小废物'" :institution="'北京航空航天大学'"
			:mail="'duansangni@hhhhh.com'"
			:logoPath="'/static//logo.png'"></expert-card>
		</view> -->
		<!-- <expert-card :name="'名字'"
		:title="'职称'" :institution="'机构'"
		:mail="'邮箱'"
		:logoPath="'/static//logo.png'"></expert-card> -->
		<block v-for="(item, index1) in recommendList.list" :key="index1">
			<expert-card
			@click.native="expertDetail(item)"  
			:logoPath="item['userpic']" 
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
import { getExpertList } from "@/api/expert_store.js"
	export default {
		data() {
			return {
				chosen_institution: '',
				chosen_area: '',
				chosen_title: '',
				searchText: '',
				institution_list: [
					'北航',
					'复旦大学'
				],
				area_list: [
					"信息技术", "装备制造", "新材料", "新能源", "节能环保", "生物医药", "科学创意", "检验检测", "其他"
				],
				title_list: [
					'教授',
					'副教授',
					'博导',
					'硕导'
				],
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					list: [
					// 	{
					// 		'userpic': '/static/head.jpg',
					// 		'author': 'Expert1',
					// 		'mail': 'iszry@foxmail.com',
					// 		'title': '副教授',
					// 		'institution': '北京航空航天大学',
					// 		'intro': '一种线型结构的具有优异综合性能的热塑性工程塑料',
					// 		'workLogoPath': '/static//logo.png',
					// 	},
					// 	{
					// 		'userpic': '/static/head.jpg',
					// 		'author': 'Expert2',
					// 		'mail': 'iszry@foxmail.com',
					// 		'title': '副教授',
					// 		'institution': '北京航空航天大学',
					// 		'intro': '该项目通过与其他生物可降解材料的共混，以及与纳米粒子的复合来得到廉价、加工性能良好、力学及防水性能改善的大豆蛋白质环境友好材料。',
					// 		'workLogoPath': '/static//logo.png',
					// 	}
					]
				},
			}
		},
		onShow() {		//页面加载,一个页面只会调用一次
			console.log('experts-onShow()')
			this.requestData()
		},
		onLoad() {		//页面显示,每次打开页面都会调用一次
			console.log('experts-onLoad()')
			// uni.getSystemInfo({
			// 	success: res => {
			// 		let height = res.windowHeight - uni.upx2px(100)
			// 		this.swiperheight = height
			// 	}
			// })
			//this.requestData() 不能刷新，防止点进文章再出来跳飞了
		},
		watch: {
			chosen_institution(newVal, oldVal) {
				this.requestData()
			},
			chosen_area(newVal, oldVal) {
				this.requestData()
			},
			chosen_title(newVal, oldVal) {
				this.requestData()
			},
			searchText(newVal, oldVal) {
				this.requestData()
			}
		},
		methods: {
			navToEntry(){
				// console.log('back to entry')
				uni.switchTab({
					url: '../entry/entry',
				})
			},
			expertDetail(expert){
				console.log(expert['author'])
				console.log(expert['uid'])
				// getExpertByID
				uni.navigateTo({
					url: '../../pages/user-space/user-space?uid=' + expert['uid'],
				})
			},
			async requestData() {
				try {
					let paras = {
						"organization": this.chosen_institution,
						"field": this.chosen_area,
						"title": this.chosen_title,
						"key_word": this.searchText
					}
					this.recommendList.list = await getExpertList(paras)
				} catch (e) {
					console.log(e)
					return
				}
			},
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
