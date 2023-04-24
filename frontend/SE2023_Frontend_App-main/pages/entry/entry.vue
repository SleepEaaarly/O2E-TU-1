<template>
	
	<view>
		<!-- 搜索栏 -->
		<view class = "search_view" style="margin-top: 10rpx;margin-left: 20px;margin-right: 20px;margin-top: 30px;">
			<u-search placeholder="请输入搜索内容" :showAction = "true" v-model="searchText" @custom="mixSearch"></u-search>
		</view>
		
		
		<view>
			<u-grid
			:border="false"
			col="3"
			style="margin-top: 20px;"
			>
			    <u-grid-item>
					<view style="background-color: aliceblue;border-radius: 30px;height: 110px;width: 110px;">
						<u-row style="margin-bottom: 0%">
							<image class="logo" @click="navToExperts"
							src="/static//Designer _Flatline.png" 
							style = "height: 90px;width: 90px;margin-left: 10px;">
						</image>
						</u-row>
						<u-row style="margin-bottom: 10px;">
							<text class="grid-text">专家库</text>
						</u-row>
						
					</view>
			        
			    </u-grid-item>
				
				<u-grid-item>
					<view style="background-color:#F0E4F8;border-radius: 30px;height: 110px;width: 110px;">
						<u-row style="margin-bottom: 0%">
							<image class="logo" @click="navToCompanies"
							src="/static//company.png" 
							style = "height: 90px;width: 90px;margin-left: 10px;">
						</image>
						</u-row>
						<u-row style="margin-bottom: 10px;">
							<text class="grid-text">企业库</text>
							
						</u-row>
						
					</view>
				    
				</u-grid-item>
				
				<u-grid-item>
					<view style="background-color:#F8E4E8;border-radius: 30px;height: 110px;width: 110px;">
						<u-row style="margin-bottom: 0%">
							<image class="logo" @click="navToWorks"
							src="/static//Data organization_Flatline.png" 
							style = "height: 90px;width: 90px;margin-left: 10px;">
						</image>
						</u-row>
						<u-row style="margin-bottom: 10px;">
							<text class="grid-text">成果库</text>
							
						</u-row>
						
					</view>
				    
				</u-grid-item>
				
				
			</u-grid>
		</view>
		<view style="background-color: #F7F7F7;margin-top: 10px; margin-top:15px;padding-bottom: 20px;padding-top: 8px;height: 100%;">
			<u-row style="margin-left: 5px;margin-bottom: 8px;">
				<u-icon name="reload" size="20" ></u-icon>
				<text style="color: dimgrey;font-weight: 600;margin-left: 5px;">推荐成果</text>
			</u-row>
			
			<!-- 列表形式导入 -->
			<template>
				<block v-for="(item, index1) in recommendList.list" :key="index1">
					<work-card
					@click.native="workDetail(item)"  
					:authorLogoPath="item['authorLogoPath']" 
					:workLogoPath="item['workLogoPath']" 
					:author="item['author']"
					:title="item['title']"
					:date="item['date']"
					:intro="item['abstract']"
					:period="item['period']"
					:area="item['field']"
					:index="index1"></work-card>
				</block> 
				<uni-load-more :loadtext="recommendList.loadtext"></uni-load-more>
			</template>
		</view>
		
<!-- 		<u-tabbar
			:value="value1"
			@change="change1"
			:fixed="true"
			:placeholder="false"
			:safeAreaInsetBottom="true"
		>
			<u-tabbar-item text="首页" icon="home" @click="click1" ></u-tabbar-item>
			<u-tabbar-item text="社区" icon="share" @click="click1" ></u-tabbar-item>
			<u-tabbar-item text="消息" icon="chat" @click="click1" ></u-tabbar-item>
			<u-tabbar-item text="平台" icon="order" @click="click1" ></u-tabbar-item>
			<u-tabbar-item text="我的" icon="account" @click="click1" ></u-tabbar-item>
		</u-tabbar> -->
		
		
	</view>
	
	
	
	
</template>

<script>
	import workCard from '@/components/work_display_card.vue'
	import { getWorkRec } from "@/api/work_recommend.js"
	import { mapState } from 'vuex'
	import { getWorkList } from "@/api/work_store.js"
	export default {
		data() {
			return {
				searchText:'',
				cur_page: 1,
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					list: [
						// {
						// 	'authorLogoPath': '/static/expert_test_head_logo (2).png',
						// 	'author': 'Expert1',
						// 	'date': '2023-3-30 21:41',
						// 	'title': '超高分子量聚乙烯的研发制备',
						// 	'area': '新材料',
						// 	'intro': '一种线型结构的具有优异综合性能的热塑性工程塑料',
						// 	'workLogoPath': '/static/super_quantity_material.png',
						// 	"period": "中试",
						// },
						// {
						// 	'authorLogoPath': '/static/expert_test_head_logo (1).png',
						// 	'author': 'Expert2',
						// 	'date': '2023-3-30 21:50',
						// 	'title': '环境友好大豆蛋白质材料改性开发',
						// 	'area': '生物医药',
						// 	'intro': '该项目通过与其他生物可降解材料的共混，以及与纳米粒子的复合来得到廉价、加工性能良好、力学及防水性能改善的大豆蛋白质环境友好材料。',
						// 	'workLogoPath': '/static/soybean_improvement.png',
						// 	"period": "产业化",
						// },
						// {
						// 	"title": 'A Summary of ML',
						// 	"author": '占瑞乙',
						// 	'area': '科学创意',
						// 	"expert_title": '本科生',
						// 	"intro": 'Here is a summary of some of the most commonly used methods in machine learning.',
						// 	"expert_organization": '北京航空航天大学',
						// 	"authorLogoPath": '/static/head_zry_fox.jpg',
						// 	"work_id": '',
						// 	"expert_id": '',
						// 	"user_id": '',
						// 	'workLogoPath': '/static/work_logo_test_zry.png',
						// 	"work_pic": '/static/ML_Notes.png' ,
						// 	"expert_mail": "iszry@foxmail.com",
						// 	'date': '2023-4-4 16:32',
						// 	"period": "实验室",
						// }
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
		onReachBottom(res) {
			// console.log("页面滚动了")
			this.requestData()
			uni.$emit('onReachBottom', res.scrollTop);
		},
		computed: { 
			items_classified:  {
				get: 	function() {
							if(this.field !== this.field_items.length) {
								let val = []
								for(let item of this.items) {
									if(item.field === this.field) {
										val.push(item)
									}
								}
								return val.length === 0 ? this.items : val
							} else {
								return this.items
							}
						},
				set:    function(newValue) {
							if (newValue.length === 0) {
								this.items_show = false
							} else {
								this.items_show = true
							}
						}
			},
			...mapState(['userInfo']) 
		},

		watch: {
			// searchText(newVal, oldVal) {
			// 	console.log(oldVal)
			// 	console.log(newVal)
			// },
			field: function(newValue) {
				let that = this
				var f = function(that) {
					if(newValue !== that.field_items.length - 2) {
						let val = []
						for(let item of that.items) {
							if(item.field === newValue) {
								val.push(item)
							}
						}
						console.log(val.length)
						that.items_classified = val
					} else {
						that.items_classified = that.items
					}
				}
				f(that)
			}
		},
		methods: {
			
			mixSearch(){
				uni.navigateTo({
					url: `../mix_search/mix_search?search_text=${this.searchText}`,
				})
			},
			navToExperts() {
				// console.log('Jump to detail of the Experts')
				uni.navigateTo({
					url: '../expert_store/expert_store',
				})
			},
			navToWorks() {
				// console.log('Jump to detail of the Works')
				uni.navigateTo({
					url: '../work_store/work_store',
				})
			},
			navToCompanies() {
				// console.log('Jump to detail of the companies')
				uni.navigateTo({
					url: '../company_store/company_store',
				})
			},
			
			workDetail(work) {
				console.log(work['result_id'])
				// getExpertByID
				uni.navigateTo({
				 	url: '../../pages/work_detail/work_detail?rid=' + work['result_id'],
				 })
			},
			async requestData() {
				try {
					let paras = {
						"id": this.userInfo.id,
						"type": this.userInfo.type,
					}
					var rec_list = {}
					
					// TODO 成果推荐 Debug
					rec_list = await getWorkRec(paras)
					// TODO 成果推荐 Debug
					
					if(rec_list == null){
						rec_list = {}
					}
					paras = {
						"field": '',
						"period": '',
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
	.grid-text{
		margin-top: 0%;
		margin-left:35px;
		font-size: 13px;
		/* font-weight: 400; */
	}
	
</style>
