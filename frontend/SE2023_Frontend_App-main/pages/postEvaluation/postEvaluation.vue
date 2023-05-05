<template>
	<view class="post">
		<!-- 评分字数大闯关 -->
		<uni-card :is-shadow="false" is-full>
			<tui-steps :items="items" spacing="250rpx" :activeSteps="activeSteps"></tui-steps>
		</uni-card>
		<view>
		<uni-section>
			<uni-forms ref="form" :rules="myRules" :modelValue="formData" @submit="onSubmit">
				<uni-forms-item label="合作体验" name="ratestar">
					<uni-rate v-model="formData.rate_taste" @change="onChange"/>
				</uni-forms-item>
				<uni-forms-item label="完成速度" name="ratestar">
					<uni-rate v-model="formData.rate_speed" @change="onChange"/>
				</uni-forms-item>
				<uni-forms-item label="专业水准" name="ratestar">
					<uni-rate v-model="formData.rate_level" @change="onChange"/>
				</uni-forms-item>
				<uni-forms-item label="详细评价" name="description">
					<uni-easyinput type="textarea" :disabled='flag==1'
						v-model="formData.description" 
						placeholder="详细描述您的订单合作体验,可以帮助更多想要与企业合作的人~" 
						@input="inputArea()"/>
				</uni-forms-item>
				<uni-forms-item label="评价时间">
					<uni-datetime-picker type="datetime" 
						return-type="timestamp" 
						v-model="formData.datetime"
						:disabled="true"/>
				</uni-forms-item>
				
				
				<button type="default" v-if='flag==0' plain="true" form-type="submit" @click="onSubmit">提交评价</button>
				<button type="default" v-else-if='flag==1' plain="true" :disabled="true" form-type="submit" @click="onSubmit">评价已存在</button>
			</uni-forms>

			
			
		</uni-section>
		</view>

	</view>
</template>

<script>
	import tuiSteps from '@/components/thorui/tui-steps/tui-steps'
	import { mapState } from 'vuex'
	import {postEvaluation,orderToEvaluation,} from '@/api/postEvaluation.js'
	export default {
		async onLoad(data){
			this.formData.order_id=data.oid
			this.init()
		},
		computed: { ...mapState(['userInfo']) },
		data() {
			return {
				point: [Math.floor(Math.random()*10)+10, Math.floor(Math.random()*10)+110],
				items: [{
						title: '评价',
						desc: '',
					}, {
						title: '满15字',
						desc: '',
						// 什么jb傻逼玩意,加一个random，v-model直接爆炸螺旋原地起飞绑定不上了
						// desc: '获'.concat(str(this.point[0])).concat('积分')
					}, {
						title: '满80字',
						desc: ''
						// desc: '获'.concat(str(this.point[1])).concat('积分')
					}],
				activeSteps: 0,
				
				// 基础表单数据
				formData: {
					rate_taste: 0,
					rate_speed: 0,
					rate_level: 0,
					description: '',
					datetime: Date(),
					order_id:0,
					
				},
				flag:-1,
				// 自定义表单校验规则
				myRules: {
					description: {
						rules: [{
							required: true,
							errorMessage: '问题描述不能为空'
						}]
					},
				},
			}
		},

		methods: {
			onChange(e){
				console.log('rate发生改变:' + JSON.stringify(e))
			},
			async init(){
				let result = await orderToEvaluation(this.formData.order_id)
				this.flag = result.flag
				if(this.flag==1){
					this.formData = result.data
					console.log("rate exist!")
				}else{
					
				}
			},
			
			// 全局导航栏发布按钮
			onNavigationBarButtonTap:function(e){
				uni.showToast({
					title: '评价成功！',
					duration: 1250,
				})
				setTimeout(function(){	//延迟跳转
					uni.navigateBack()	//回到上一界面
				}, 1500)
			 },
			 
			 switchChange(){
				 console.log('拨动switch')
			 },
			 // 监听文本字数
			 inputArea(){
				 let len = this.formData.description.length
				 if(len > 80){
					 this.activeSteps = 2
				 }
				 else if(len > 15){
					 this.activeSteps = 1
				 }
				 else{
					 this.activeSteps = 0
				 }
			 },
			 async onSubmit(e){
				 if(this.formData.rate_level && this.formData.rate_speed && this.formData.rate_taste){
					 let result = await postEvaluation(this.formData)
					 console.log(result)
					 uni.showToast({
					 	title: '评价成功！',
					 	duration: 1250,
					 })
					 setTimeout(function(){	//延迟跳转
					 	uni.navigateBack()	//回到上一界面
					 }, 1500)
				 }
				 
				 console.log(this.formData.order_id)
			 }
		}
	}
</script>

<style>

	.post {
		min-height: 1000upx;
		background-color: #F1F1F1;
		
		margin-left: 15upx;
		margin-right: 15upx;
	}
</style>
