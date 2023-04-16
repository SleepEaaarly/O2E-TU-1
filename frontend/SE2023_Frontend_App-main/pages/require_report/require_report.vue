<template>
	<view>
		<u-row>
			<text style="margin-left:50rpx;font-size: 20px;font-weight: 550;text-align:center;">{{ require_info.requireName }}</text>
		</u-row>
		
		<company-card
		:name="require_info.company_name"
		:area="require_info.company_area" 
		:address="require_info.company_address"
		:logoPath="require_info.company_logoPath"
		
		></company-card>
		
		<view style="
		margin-top: auto;background-color: aliceblue;width: 650rpx;margin-left: 35rpx;height: auto;
		border-left:8rpx solid cornflowerblue;
		background-color: aliceblue;padding-top: 10rpx;padding-left: 20rpx;padding-bottom: 10rpx;">
			<text class="intro">{{ require_info.require_intro }}</text>
		</view>
		
		<view>
		<u-row>
			<u-tag text="需求简介"  plain plainFill size = "mini"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="require_info.require_keyword_1"  plain plainFill size = "mini" type="warning"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			<u-tag :text="require_info.require_keyword_2"  plain plainFill size = "mini" type="success"
			style="margin-left: 20rpx;margin-top: 20rpx;"></u-tag>
			
		</u-row>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<text>
				需求报告：请帮我写软工吧
				1. 项目背景
				该项目旨在为需要软工技术帮助的个人和企业提供一站式解决方案。许多人在软件开发过程中会遇到一些困难，而我们的目标是通过提供专业的软工服务来帮助他们克服这些困难。
				2. 用户需求
				我们的用户主要包括个人（如程序员、学生等）和企业。他们可能需要以下软工服务：
				·软件设计和开发
				·质量保证
				·需求调研和分析
				·系统架构设计
				·软件部署和维护
				·培训和咨询
				3. 解决方案 我们将建立一个团队，由经验丰富的软工专家组成。我们将提供以下服务：
				·线上咨询和支持：提供快速响应和贴心服务，为用户答疑解惑。
				·定制化服务：根据用户需求，制定相应的计划和流程，并根据实际情况进行数据分析和优化。
				·社群支持：建立讨论区和社区，为用户提供交流和互动的平台，增强用户对软工知识的学习和理解。
				4. 技术实现 我们将采用以下技术实现我们的服务：
				·ASP.NET MVC框架：利用成熟的软件架构来支持大规模并发。
				·安全性：我们将采用正式认证和授权机制，保证数据的安全性。
				·数据分析和学习：通过收集和处理大量的数据和反馈，我们会为用户提供更好的服务体验。
				5. 项目计划 我们将按以下步骤进行软工服务的交付：
				·需求调研和分析：确定客户需求和要解决的问题。
				·方案设计：根据客户需求设计定制化的软工方案，包括流程、时间表和预算。
				·设计开发：在设计阶段，开发团队将负责实施指定的程序建模、编码、测试等任务。
				·应用部署：经过测试确认后，在线上运行本程序。
				·训练和维护：在最终部署之前，用户将接受必要的培训，随后执行基本维护任务并获得技术支持。
				6. 结论 通过该项目，我们可以填补市场空白，打造一站式的软工解决方案。同时，我们也可以帮助用户克服困难，提升软件开发和维护的水平和效率，促进软件行业的发展。
			</text>
		</u-row>
		</view>
		
	</view>
</template>

<script>
	import companyCard from "../../components/company_rep_display_card.vue"
	import fuiCard from "@/components/firstui/fui-card/fui-card.vue"
	import require_message_card from 'components/require_message_card'
	export default {
		data() {
			return {
				work_id: 1,
				height: 500,
				require_info: {
					"requireName": '帮我写软工吧',
					"company_name": '北京航空航天大学',
					"require_intro": 'Here is a summary of some of the most commonly used methods in machine learning.',
					"company_address": '北京市海淀区',
					"company_logoPath": '/static/head.jpg',
					"company_area":'计算机',
					"require_id": '',
					"company_id": '',
					// "user_id": '',
					// "work_pic": '/static/ML_Notes.png' ,
					"require_keyword_1": "实验室",
					"require_keyword_2": "科学创意"
				}
				
			}
		},
		methods: {
			
		},
		components: {
			companyCard,
			fuiCard,
			require_message_card
		}
	}
</script>

<style>

</style>
