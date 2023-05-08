<template>
	<view>
		<view class="my-evaluations" v-if='this.flag==1'>
			<view v-if='this.type==4'>
				<uni-section subTitle="" title="专家信息" type="circle" >
					<uni-list>
						<uni-list-item link clickable :thumb="rateList[0].expert.expert_icon" :title="rateList[0].expert.expert_name" @click="gotospace()">
						</uni-list-item>
					</uni-list>
				</uni-section>
				<uni-section subTitle="" title="专家评分" type="circle" >
					<home-data :homedata="ratedata"></home-data>
					<view class="charts-box">
						<qiun-data-charts 
							type="radar"
							:opts="opts"
							:chartData="chartData"
						/>
					  </view>
				</uni-section>
			</view>
			<uni-section subTitle="显示最近的评价" title="全部评价" type="line" >
				<!-- 企业发布的评价 -->
				<view v-if="this.type==5">
				<uni-card v-for='(eva,index) in rateList' :key="index" 
						  :is-shadow='false' :title="eva.expert.expert_name" 
						  :extra="eva.rate.datetime" :sub-title="eva.order.order_name" 
						  :thumbnail='eva.expert.expert_icon'>
					<uni-collapse v-model="value">
						<uni-collapse-item :show-animation="true" title="评价详情">
						<view>
							<uni-forms-item label="合作体验">
								<uni-rate  :value="eva.rate.rate_taste" :readonly="true" :is-fill="false"/>
							</uni-forms-item>
							<uni-forms-item label="完成速度">
								<uni-rate  :value="eva.rate.rate_speed" :readonly="true" :is-fill="false"/>
							</uni-forms-item>
							<uni-forms-item label="专业水准">
								<uni-rate  :value="eva.rate.rate_level" :readonly="true" :is-fill="false"/>
							</uni-forms-item>
							<uni-forms-item label="具体评价">
								<text class='uni-body' v-if='eva.rate.description'>{{eva.rate.description}}</text>
								<text class='uni-body' v-else>无</text>
							</uni-forms-item>
						</view>
						</uni-collapse-item>
					</uni-collapse>
				</uni-card>
				</view>
				
				<!-- 专家收到的评价 -->
				<view v-else-if="this.type==4">
				<uni-card v-for='(eva,index) in rateList' :key="index" :is-shadow='false' :title="eva.enterprise.enterprise_name" :extra="eva.rate.datetime" :sub-title="eva.order.order_name" :thumbnail='eva.enterprise.enterprise_icon'>
					<uni-collapse v-model="value">
						<uni-collapse-item :show-animation="true" title="评价详情">
						<view>
							<uni-forms-item label="合作体验">
								<uni-rate  :value="eva.rate.rate_taste" :readonly="true" :is-fill="false"/>
							</uni-forms-item>
							<uni-forms-item label="完成速度">
								<uni-rate  :value="eva.rate.rate_speed" :readonly="true" :is-fill="false"/>
							</uni-forms-item>
							<uni-forms-item label="专业水准">
								<uni-rate  :value="eva.rate.rate_level" :readonly="true" :is-fill="false"/>
							</uni-forms-item>
							<uni-forms-item label="具体评价">
								<text class='uni-body' v-if='eva.rate.description'>{{eva.rate.description}}</text>
								<text class='uni-body' v-else>无</text>
							</uni-forms-item>
						</view>
						</uni-collapse-item>
					</uni-collapse>
				</uni-card>
				</view>
			</uni-section>
			
		</view>
		<view class="mystyle u-f-ajc animated fadeIn" v-else>
			<image src="/static/images/toast/no-data-03.jpg" 
				mode="widthFix"></image>
		</view>
		
		<!-- 数据加载时动画 -->
		<!-- <w-loading text="加载中.." mask="true" click="true" ref="loading"></w-loading> -->
	</view>
</template>

<script>
	import { mapState } from 'vuex'
	import { postEvaluation,orderToEvaluation,idToEvaluation } from '@/api/postEvaluation.js'
	import{ picUrl, } from '@/api/common.js'
	import homeData from '../../components/home/home-data.vue'
	import { getUserInfo } from '@/api/user-space.js'
	import wLoading from '@/components/w-loading/w-loading.vue'	// 加载动画
	
	export default {
		components: { homeData, },
		
		data() {
			return {
				value:true,
				rateList:[],
				flag:-1,
				id:0,
				type:0,
				ratedata: [
					{
						name: '合作体验',
						num: 0
					},
					{
						name: '完成速度',
						num: 0
					},
					{
						name: '专业水平',
						num: 0
					},
				],
				chartData: {},
				//可以通过修改 config-ucharts.js 文件中下标为 ['radar'] 的节点来配置全局默认参数，如都是默认参数，此处可以不传 opts 。实际应用过程中 opts 只需传入与全局默认参数中不一致的【某一个属性】即可实现同类型的图表显示不同的样式，达到页面简洁的需求。
				opts: {
					color: ['#1890FF','#91CB74','#FAC858','#EE6666','#73C0DE','#3CA272','#FC8452','#9A60B4','#ea7ccc'],
					padding: [5,5,5,5],
					dataLabel: false,
					legend: {
						show: true,
						position: 'right',
						lineHeight: 25
					},
					extra: {
						radar: {
							gridType: 'radar',
							gridColor: '#CCCCCC',
							gridCount: 3,
							opacity: 0.2,
							max: 5,
							border: true
						}
					},
				},
			}
		},
		async onLoad(data){
			this.id=data.id
			console.log('load')
			this.init()
			// this.getChartData()	//放此处会加载不出来
		},
		onReady(){
			// this.$refs.loading.open()	// 打开动画钩子
		},
		async mounted(){
			this.getChartData()
		},
		computed: { ...mapState(['userInfo']) },
		methods: {
			async init(){
				console.log(this.id)
				if(this.id>0){
					var result = { 'avg':{ 'rate_data':1 } }
					result = await idToEvaluation(this.id)
					console.log(result)
					var data = await getUserInfo({ 'user_id':this.id })
					this.type = data.type

					if(result && result.code){
						console.log('error')
					}else if(this.type===4 ||(this.type===5 && this.id===this.userInfo.id)){
						this.flag = result.flag
						this.rateList = result.data
						//console.log(result.rate[0])
						this.ratedata[0].num=result.avg.rate_taste
						this.ratedata[1].num=result.avg.rate_speed
						this.ratedata[2].num=result.avg.rate_level
						//console.log(this.ratedata[0].num)
						console.log(this.rateList[0].rate.rate_taste)
					}
					else{
						this.flag = result.flag
						this.rateList = result.data
					}
					if(this.type===5 && this.id!==this.userInfo.id){
						this.flag=0
					}
				}
				// this.$refs.loading.close()	// 关闭动画钩子
			},
			async getChartData() {
				//模拟服务器返回数据，如果数据格式和标准格式不同，需自行按下面的格式拼接
				// if(this.type===4){ 这里不能加，否则chartData为空渲染有问题
					let result = await idToEvaluation(this.id)
					let a = (result.avg.rate_taste+result.avg.rate_speed+result.avg.rate_level)/3
					let res = {
						categories: ['合作体验','完成速度','专业水平','活跃程度','平台信誉'],
						series: [
						  {
							name: '专家评分',
							// data: [90,110,165,195,187,172]
							// data: [5.0,4.5,5.0,3.9,4.0],
							
							//data: [5.0,4.5,5.0,3.9,4.0],
							data: [result.avg.rate_taste,
								   result.avg.rate_speed,
								   result.avg.rate_level,
								   3.9,a]
						  },
						  {
							name: '平均评分',
							// data: [190,210,105,35,27,102]
							data: [2.6,4.2,3.9,1.5,2.8]
						  }
						]
					}
					this.chartData = JSON.parse(JSON.stringify(res))
					
				// }
			},
			gotospace(){
				uni.navigateTo({ url: '../user-space/user-space?uid=' + this.id })
			},
			gotospace1(id){
				uni.navigateTo({ url: '../user-space/user-space?uid=' + id })
			},
		}
	}
</script>

<style scoped>
	.my-evaluations{
		background-color: #F1F1F1;
		margin-left: 10upx;
		margin-right: 10upx;
	}
	/* 请根据实际需求修改父元素尺寸，组件自动识别宽高 */
	.charts-box {
		width: 100%;
		height: 200px;
	}
</style>
