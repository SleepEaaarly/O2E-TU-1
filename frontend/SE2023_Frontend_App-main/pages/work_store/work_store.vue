<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon @click="navToEntry" name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">成果库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="area_list" placeholder="领域" v-model="area" class="work_combox" :border="false"></uni-combox>
			<uni-combox :candidates="period_list" placeholder="技术成熟度" v-model="period" class="work_combox" :border="false"></uni-combox>
		</u-row>
		
		<block v-for="(item, index1) in recommendList.list" :key="index1">
			<work-card
			@click.native="workDetail(item)"  
			:authorLogoPath="item['authorLogoPath']" 
			:workLogoPath="item['workLogoPath']" 
			:author="item['author']"
			:title="item['title']"
			:date="item['date']"
			:area="item['area']"
			:intro="item['intro']"
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

					]
				},
			}
		},
		onShow() {		//页面加载,一个页面只会调用一次
			console.log('works-onShow()')
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
		methods: {
			navToEntry(){
				console.log('back to entry')
				uni.switchTab({
					url: '../entry/entry',
				})
			},
			maskClick(){
				
			},
			workDetail(work) {
				console.log(work['author'])
				console.log(work['uid'])
				// getExpertByID
				// uni.navigateTo({
				// 	url: '../../pages/user-space/user-space?uid=' + work['uid'],
				// })
			},
			async requestData() {
				try {
					let paras = {
						"field": this.chosen_area,
						"period": this.chosen_period,
						"key_word": this.searchText
					}
					this.recommendList.list = await getWorkList(paras)
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
