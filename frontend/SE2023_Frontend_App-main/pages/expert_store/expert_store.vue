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
		<view>
			<block
			 v-for="(item, index1) in recommendList.list" :key="index1">
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

	</view>
</template>

<script>
import expertCard from "@/components/expert_display_card.vue"
import { getExpertList } from "@/api/expert_store.js"
import loadMore from '../../components/common/load-more.vue'
	export default {
		data() {
			return {
				chosen_institution: '',
				chosen_area: '',
				chosen_title: '',
				searchText: '',
				cur_page: 1,
				loadtext:'',
				windowHeight: 100,
				finish_getting: false,
				institution_list: ['北京大学', '北京航空航天大学', '北京理工大学', '北京师范大学', '重庆大学', '大连理工大学', '电子科技大学', '东北大学', '东南大学', '复旦大学', '国防科技大学', '哈尔滨工业大学', '湖南大学', '华东师范大学', '华南理工大学', '华中科技大学', '吉林大学', '兰州大学', '南京大学', '南开大学', '清华大学', '山东大学', '上海交通大学', '四川大学', '天津大学', '同济大学', '武汉大学', '西安交通大学', '西北工业大学', '西北农林科技大学', '厦门大学', '浙江大学', '中国海洋大学', '中国科学技术大学', '中国农业大学', '中国人民大学', '中南大学', '中山大学', '中央民族大学'],
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
					list: []
				},
			}
		},
		onShow() {		//页面加载,一个页面只会调用一次
			console.log('experts-onShow()')
			this.finish_getting = false
			this.recommendList.list = []
			this.requestData()
		},
		onLoad() {		//页面显示,每次打开页面都会调用一次
			console.log('experts-onLoad()')
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
		onReachBottom() {
			// this.loadmore()
		},
		onPageScroll(res) {
			// console.log("页面滚动了")
			this.requestData()
			uni.$emit('onPageScroll', res.scrollTop);
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
				if(this.finish_getting){
					console.log('finish getting data')
					return
				}
				try {
					let paras = {
						"organization": this.chosen_institution,
						"field": this.chosen_area,
						"title": this.chosen_title,
						"key_word": this.searchText,
						"page": this.cur_page
					}
					let ret = await getExpertList(paras)
					this.cur_page = this.cur_page + 1
					if(ret.length===0||ret==null||ret==[]||ret=={}){
						this.finish_getting = true
						return 
					}else{
						this.recommendList.list = this.recommendList.list.concat(ret)
					}
				} catch (e) {
					console.log(e)
					return
				}
			},
			loadMore(){
				console.log('loadMore')
				
				// 获取数据
				this.requestData()
			},
			upper(){
				console.log('scroll upper')
			},
			lower(){
				console.log('scroll lower')
			}
		},
		components : {
			expertCard,
			loadMore
		}
	}
</script>

<style>
	.expert_combox {
		width: 95px;
		border-radius: 15px;
		background-color: #f2f2f2;
		margin-right: 5px;
		/* font-size: 10rpx; */
	}
	
	/* .uni-combox .uni-combox-list .uni-combox-item {
	    font-size: 6rpx;
	} */
</style>
