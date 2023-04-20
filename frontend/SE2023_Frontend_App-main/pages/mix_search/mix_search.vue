<template>
	<view>
		<u-row style="margin-left: 20px;margin-right: 20px;margin-top: 20px;">
			<u-icon @click="navToEntry" name="arrow-left" size="28" ></u-icon>
			<u-search placeholder="请输入搜索内容" :showAction = "true" v-model="searchText" @custom="mixSearch"></u-search>
		</u-row>
		
		
		<view style="background-color: #F7F7F7;margin-top: 10px; margin-bottom: 0px;padding-top: 8px;">

			<u-scroll-list >
				 <u-col  v-for="(item, index1) in recommendList.exp_list" :key="'exp'+index1" span="4">
					 <personCard @click.native="expertDetail(item)"
					 :name="item['name']"
					 :logoPath="picUrl + item['userpic']"
					 :type="item['title']"></personCard>
				</u-col>
				<u-col  v-for="(item, index2) in recommendList.ent_list" :key="'ent'+index2" span="4">
					 <personCard @click.native="companyDetail(item)"
					 :name="item['name']"
					 :logoPath="picUrl + item['userpic']"
					 :type="item['field']"></personCard>
				</u-col>
			</u-scroll-list>
			
			
			
			
		</view>
		<block v-for="(item, index3) in recommendList.res_list" :key="'res'+index3">
			<work-card
			@click.native="workDetail(item)"  
			:authorLogoPath="picUrl + item['expert_icon']" 
			:workLogoPath="picUrl + item['result_pic']" 
			:author="item['scholars']"
			:title="item['title']"
			:date="item['pyear']"
			:area="item['field']"
			:intro="item['abstract']"
			:period="item['period']"
			:index="'res'+index3"></work-card>
		</block> 

	</view>
</template>

<script>
	import personCard from "@/components/search_person_card.vue"
	import workCard from '@/components/work_display_card.vue'
	import { getMixSearch } from '@/api/search.js'
	import {
		picUrl
	} from '@/api/common.js'
	export default {
		data() {
			return {
				searchText:'',
				picUrl: '',
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					res_list: [],
					ent_list: [],
					exp_list: []
				},
			}
		},
		onShow() {		//页面加载,一个页面只会调用一次
			this.requestData()
			this.picUrl = picUrl
		},
		onLoad(Options){
			// console.log(Options)
			this.searchText = Options.search_text
			// console.log(Options.search_text)
		},
		methods: {
			navToEntry(){
				// console.log('back to entry')
				uni.switchTab({
					url: '../entry/entry',
				})
			},
			workDetail(work) {
				// getExpertByID
				uni.navigateTo({
				 	url: '../../pages/work_detail/work_detail?rid=' + work['result_id'],
				 })
			},
			companyDetail(company){
				// getExpertByID
				uni.navigateTo({
					url: '../../pages/user-space/user-space?uid=' + company['user_id'],
				})
			},
			expertDetail(expert){
				// getExpertByID
				uni.navigateTo({
					url: '../../pages/user-space/user-space?uid=' + expert['user_id'],
				})
			},
			mixSearch(){
				this.requestData()
			},
			async requestData() {
				try {
					let paras = {
						"key_word": this.searchText
					}
					let ret = await getMixSearch(paras)
					this.recommendList.exp_list = ret[0]
					this.recommendList.res_list = ret[1]
					this.recommendList.ent_list = ret[2]

					console.log(this.recommendList)
				} catch (e) {
					console.log(e)
					return
				}
			},
		},
		components: {
			personCard,
			workCard
		}
	}
</script>

<style>

</style>
