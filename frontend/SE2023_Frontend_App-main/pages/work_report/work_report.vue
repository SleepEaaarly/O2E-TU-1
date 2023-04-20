<template>
	<view>
		<u-row>
			<text style="margin-left:50rpx;font-size: 20px;font-weight: 550;text-align:center;">{{ work_info.workName }}</text>
		</u-row>
		
		<author-card
			:name="work_info.expert_name" 
			:title="work_info.expert_title" :institution="work_info.expert_organization"
			:mail="work_info.expert_mail"
			:logoPath="work_info.expert_logoPath"
			@click.native="gotoExpertDetail"></author-card>
		
		<view style="
		margin-top: auto;background-color: aliceblue;width: 650rpx;margin-left: 35rpx;height: auto;
		border-left:8rpx solid cornflowerblue;
		background-color: aliceblue;padding-top: 10rpx;padding-left: 20rpx;padding-bottom: 10rpx;">
			<text class="intro">{{ work_info.work_abstract }}</text>
		</view>
		
		<view>
		<u-row>
			<u-tag text="成果简介"  plain plainFill size = "mini"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="work_info.work_period"  plain plainFill size = "mini" type="warning"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="work_info.work_field"  plain plainFill size = "mini" type="success"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			
		</u-row>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line>
				
			</u-line>
		</u-row>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<text>
					成果报告：A summary of Machine Learning
				介绍机器学习
				机器学习是一种人工智能（AI）技术，通过使用数据和统计模型，让计算机系统自动改进和适应，从而实现高效的决策和预测。

				机器学习的类型
				机器学习可以分为三种类型：监督学习、无监督学习和强化学习。监督学习是在有标记数据下学习分类或回归模型；无监督学习是在没有标记的数据下进行学习因果关系、聚类等；强化学习是通过代理奖励系统的反馈来学习以最大化奖励的策略。

				机器学习的应用领域
				机器学习已经应用于很多领域，包括医疗保健、金融、电子商务、政府管理、智能制造等。它可以应用于预测、识别、聚类和推荐。

				机器学习的步骤和流程
				机器学习的流程包括数据收集和预处理、特征选择和转换、模型训练和评估、模型调优等步骤。

				海量数据与云端计算
				海量数据和云端计算是机器学习蓬勃发展的两个重要因素，它们提供了强大的计算能力和海量的数据存储。

				机器学习未来的发展趋势
				随着人工智能技术的不断成熟，机器学习将继续向深度学习、增强学习、自然语言处理和模式识别等方面发展。在快速发展的机器学习领域里，我们可以期待着更多有趣的进展和应用。

				结论
				作为一种强有力的人工智能技术，机器学习已经改变和重新定义了许多行业，对未来的社会和经济都将产生深远的影响。
				</text>
		</u-row>
		
	</view>
	</view>
</template>

<script>
	import {
			mapState,
			mapMutations
	} from 'vuex'
	import authorCard from"../../components/author_display_card.vue"
	import { getWorkReport } from "../../api/work_report"
	export default {
		data() {
			return {
				inWorkId: null, 
				work_id: 1,
				height: 500,
				work_info: {
					"workName": 'A Summary of Machine Learning',
					"expert_name": '占瑞乙',
					"expert_title": '本科生',
					"work_abstract": 'Here is a summary of some of the most commonly used methods in machine learning.',
					"expert_organization": '北京航空航天大学',
					"expert_logoPath": '/static/head_zry_fox.jpg',
					"work_id": '',
					"expert_id": '',
					"user_id": '',
					"work_pic": '/static/ML_Notes.png' ,
					"expert_mail": "iszry@foxmail.com",
					"work_period": "实验室",
					"work_field": "科学创意"
				},
				content: "",
			}
		},
		onLoad(data) {
			this.inWorkId = data.reportId
		},
		computed: {
			...mapState(['userInfo'])
		},
		methods: {
			getWorkDetailInfo() {
				let output = getWorkReport(this.inWorkId)
				this.work_info.workName = output.workInfo.workName
				this.work_info.expert_name = output.expertInfo.expertName
				this.work_info.expert_title = output.expertInfo.expertTitle 
				this.work_info.work_abstract = output.workInfo.workAbstract 
				this.work_info.expert_organization = output.expertInfo.expertOrganization 
				this.work_info.expert_logoPath = output.expertInfo.expertLogoPath 
				this.work_info.work_id = output.workInfo.workId 
				this.work_info.expert_id = output.workInfo.expertId 
				this.work_info.user_id = this.userInfo.id 
				this.work_info.work_pic = output.workInfo.workPic 
				this.work_info.expert_email = output.expertInfo.expertEmail 
				this.work_info.work_period = output.workInfo.workPeriod 
				this.work_info.work_field = output.workInfo.workPeriod
				this.content = output.content
			},
			gotoExpertDetail() {

			},
			gotoWorkDetail() {

			}
		},
		components: {
			authorCard
		},
	}
</script>

<style>

</style>
