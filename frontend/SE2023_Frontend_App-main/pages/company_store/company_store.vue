<template>
	<view>
		<u-row style="margin-top: 10rpx;margin-left: 5px;margin-right: 20px;margin-bottom: 10px;">
			<u-icon @click="navToEntry" name="arrow-left" size="28" ></u-icon>
			<text style="margin: auto;font-size: 20px;">企业库</text>
			<!-- <u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search> -->
		</u-row>
		<u-row style="margin-left: 10px;margin-right: 10px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</u-row>
		<u-row style="margin-top: 10px;margin-left: 10px;">
			<uni-combox :candidates="address_list" placeholder="地区" v-model="chosen_address" class="company_combox" :border="false"></uni-combox>
			<uni-combox :candidates="area_list" placeholder="领域" v-model="chosen_area" class="company_combox" :border="false"></uni-combox>
			
		</u-row>
		
<!-- 		<view style="background-color: #f2f2f2;margin-top: 10px;padding-top: 10px;padding-bottom: 10px;">
			 <expert-card></expert-card> </view> -->
		<block v-for="(item, index1) in recommendList.list" :key="index1">
			<company-card @click.native="companyDetail(item)"
			:title="item['title']"
			:address="item['address']" 
			:logoPath="item['logoPath']"
			:area="item['area']"
			:index="index1"></company-card>
		</block> 
		
	</view>
</template>

<script>
	import companyCard from "@/components/company_display_card.vue"
	import { getCompanyList } from "@/api/company_store.js"
	export default {
		data() {
			return {
				chosen_area: '',
				chosen_address: '',
				address_list: [
					'北京','上海','深圳'
				],
				area_list: [
					"信息技术", "装备制造", "新材料", "新能源", "节能环保", "生物医药", "科学创意", "检验检测", "其他"
				],
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					list: [
							//{
					 		// 'area': '信息技术',
					 		// 'address': '北京市朝阳区',
					 		// 'title': '中航工业'
							//}
					]
				},
			}
		},
		onShow() {		//页面加载,一个页面只会调用一次
			console.log('companies-onShow()')
			this.requestData()
		},
		onLoad() {		//页面显示,每次打开页面都会调用一次
			console.log('companies-onLoad()')
		},
		watch: {
			chosen_address(newVal, oldVal) {
				this.requestData()
			},
			chosen_area(newVal, oldVal) {
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
			companyDetail(company){
				console.log(company['address'])
				console.log(company['title'])
				console.log(company['area'])
				// getExpertByID
				uni.navigateTo({
					url: '../../pages/user-space/user-space?uid=' + company['uid'],
				})
				// pages/user-space/user-space?uid=10
			},
			async requestData() {
				try {
					let paras = {
						"field": this.chosen_area,
						"address": this.chosen_address,
						"key_word": this.searchText
					}
					this.recommendList.list = await getCompanyList(paras)
				} catch (e) {
					console.log(e)
					return
				}
			},
		},
		components : {
			companyCard
		}
	}
</script>

<style>
	.company_combox {
		width: 152px;
		border-radius: 15px;
		background-color: #f2f2f2;
		margin-right: 10px;
		
	}

</style>
