<template>
	<view>
		<!-- 选择筛选内容
		<view class="sameline uni-px-5 uni-pb-5">
			筛选标签：
			<uni-data-checkbox class="sameline" mode="tag" multiple 
			v-model="checkbox" 
			:localdata="outcome"
			@change="generateDList()"></uni-data-checkbox>
		</view> -->
		
		<!-- 具体数据卡片 -->
		<uni-card v-for="(item, index) in datalist" :key="index" @click="openResultDetail(item)">
			<uni-row :span="24" class="title">
				<uni-col class="title">
					<uni-tag custom-style="background-color: #d6d6d6; border-color: #d6d6d6; color: #000000;"
					:circle="true" :text="item.strType" type="warning" size="small"/>

					<text>{{item.title}}</text>
				</uni-col>
			</uni-row>
			<uni-row class="detail">
				<uni-col :span="12" class="detail">
					<text class="detail-money">{{item.scholars}}</text>
				</uni-col>
				<uni-col :span="12" class="detail">
					年份：<text class="detail-field">{{item.pyear}}</text>
				</uni-col>
			</uni-row>
			<uni-row class="description">
				<uni-col class="description-text" :span="23">
					{{item.description}}
				</uni-col>
			</uni-row>
		</uni-card>
		<expert-create-achievement v-if="userInfo.type=='4'&&isSelf" :show="show" @hide="hidepopup" @addachievement="addachievement" @manageachievement="manageachievement">
		</expert-create-achievement>
	</view>
</template>

<script>
	import { getExpertInfo } from '@/api/expert.js'
	import { mapState } from 'vuex'
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniFav from '@/components/uni-fav/uni-fav.vue'
	import uniCard from '@/components/uni-card/uni-card.vue'
	import expertCreateAchievement from '@/components/user-space/expert-create-achievement.vue'
	
	export default{
		components:{
			uniRow,
			uniCol,
			expertCreateAchievement,
			uniFav,
			uniCard
		},
		computed:{ ...mapState(['userInfo']) },
		mounted() {		//页面显示,每次打开页面都会调用一次
			this.initData()
			console.log('Achievement onLoad')
		},
		props: { id: { type: Number, }, isSelf:{type: Boolean}},
		data() {
			return {
				paperlist:[],	//论文列表
				patentlist:[],	//专利列表
				projectlist: [],	//项目列表
				achievementList: [], //成果列表
				datalist:[],	//最终呈现数据的总列表
				show: false,
				
				checkbox: [0, 1, 2],	//筛选标签的初始值=全选
				outcome: [{
					text: '论文',
					value: 0
				}, {
					text: '专利',
					value: 1
				}, {
					text: '项目',
					value: 2
				}],
			}
		},
		methods: {
			async initData(){		
				this.paperlist = await getExpertInfo(this.id, 'papers')
				this.patentlist = await getExpertInfo(this.id, 'patents')
				this.projectlist = await getExpertInfo(this.id, 'projects')
				this.achievementList = await getExpertInfo(this.id, 'results')
				this.generateDList()
			},
			hidepopup() {
				this.show = false
			},
			showpopup() {
				this.show = true
			},
			addachievement() {
				uni.navigateTo({ url: '../add-achievement/achievement' })
				this.hidepopup()
			},
			manageachievement() {
				uni.navigateTo({ url: '../manage-achievement/manage-achievement' })
				// this.hidepopup()
			},
			generateDList(){	//刷新datalist
				this.datalist = []
				this.datalist.push.apply(this.datalist, this.achievementList)
				console.log(this.achievementList)
				// TODO 获取成果列表
				// this.datalist.push.apply(this.datalist, this.achievementList)
				console.log(this.datalist)
			},
			openResultDetail(work){
				// console.log(work['result_id'])
				// getExpertByID
				uni.navigateTo({
				 	url: '../../pages/work_detail/work_detail?rid=' + work['rid'],
				 })
			}
		},
	}
</script>

<style>
	/* 筛选标签样式 */
	.uni-px-5 {
		padding-left: 15px;
		padding-right: 10px;
	}
	.uni-pb-5 {
		padding-bottom: 5px;
	}
	.sameline {	/* 设定元素在同一行 */
		display: inline-block
	}
	
	.title {
		font-size: 30upx;
		font-weight: 600;
		color: #0A98D5;
	}
	/* .title-tag {
		background-color: #4335d6;
		border-color: #4335d6; 
		color: #fff;
	} */
	.detail {
		font-weight: 200;
		font-size: 20upx;
	}
	.detail-field {
		font-weight: bold !important;
	}
	.description {
		border-radius: 20upx 20upx 20upx 20upx;
		background-color: #F5FFF0;
	}
	.description-text {
		margin: 10upx;
		font-size: 25upx;
		font-weight: 100;
	}
	/* 抄的card部分 */
	.location {
		font-size: 20upx;
	}
	.buttons {
		margin-top: 75upx;
	}
	.buttons-text {
		font-size: 20upx;
	}
</style>