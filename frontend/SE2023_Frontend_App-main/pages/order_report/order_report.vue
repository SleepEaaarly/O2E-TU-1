<template>
	<view>
		<u-row>
			<text class="title">需求信息</text>
		</u-row>
		<require-card
            :logoPath="'http://localhost:8080/static/img/need_contracted.b69b28cb.jpg'"
            :name="'请帮我写软工'"
            :area="'信息技术'"
            :intro="''"
            :keyword="'123'"
            @click.native="gotoNeedDetail"
		></require-card>
		<!-- <require-card
            :logoPath="needInfo.needLogoPath"
            :name="needInfo.needName"
            :area="needInfo.needfield"
            :intro="needInfo.needIntro"
            :keyword="needInfo.needKeywords"
            @click.native="gotoNeedDetail"
		></require-card> -->
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		
		<u-row>
			<text class = "title">专家信息</text>
		</u-row>
		<author-card
            :name="'专家zkg'"
            :title="''"
            :logoPath="'http://43.138.27.92:8000/api/images/202205/02/icons/zkg2.jpg'"
            :mail="'1793030808@qq.com'"
            :institution="'123'"
            @click.native="gotoExpertDetail"
		></author-card>
		<!-- <author-card
            :name="expertInfo.expertName"
            :title="expertInfo.expertTitle"
            :logoPath="expertInfo.expertLogoPath"
            :mail="expertInfo.expertEmail"
            :institution="expertInfo.expertOrganization"
            @click.native="gotoExpertDetail"
		></author-card> -->
		
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		
		<u-row>
			<text class = "title">企业信息</text>
		</u-row>
		<company-card
            :name="'企业zkg'"
            :area="'123'" 
            :address="'123'"
            :logoPath="'http://43.138.27.92:8000/api/images/202205/02/icons/zkg.jpg'"
            @click.native="goToEnterpriseDetail"
		></company-card>
		<!-- <company-card
            :name="enterpriseInfo.enterpriseName"
            :area="enterpriseInfo.enterpriseArea" 
            :address="enterpriseInfo.enterpriseAddress"
            :logoPath="enterpriseInfo.enterpriseLogoPath"
            @click.native="goToEnterpriseDetail"
		></company-card> -->
		<u-row style="margin-top: 20rpx;margin-left: 20rpx;margin-right: 20rpx;">
			<u-line></u-line>
		</u-row>
		<u-row>
			<text class = "title">订单追踪</text>
		</u-row>
		<time-axis :dataArray="dataArray" style="margin-left: 30px;margin-top: 10px;margin-right: 20px;"></time-axis>
	</view>
</template>

<script>
    import {
		mapState,
		mapMutations
	} from 'vuex'
    import { getOrderReport } from '../../api/order_report'
	import authorCard from "../../components/author_display_card.vue"
	import companyCard from "../../components/company_rep_display_card.vue"
	import requireCard from "../../components/require_display_card.vue"
	import timeAxis from "../../components/time_axis.vue"
	export default {
		data() {
			return {
                inReportId: 0, 
				dataArray:[
                    {
                        time:'2023-04-12 17:32:15',
                        title:'需求发布',
                        // content:'那就看你会计解决',
                        active:true
                    },{
                        time:'2023-04-17 15:31:15',
                        title:'专家接单',
                        // content:'顺丰到付的',
                        active:true
                    },{
                        time:'2023-04-19 11:31:52',
                        title:'订单完成',
                        // content:'大幅度发',
                        active:true
                    },
                ],
                needInfo: {	// 需求信息
                    needId: null,			// 需求id
                    needName: null,		// 需求名称
                    needKeywords: null,		// 需求关键词
                    needField: null,		// 需求领域
                    needLogoPath: null,	// 需求图片
                },
                expertInfo: {	// 专家信息
                    expertId: null,
                    expertLogoPath: null,		// 专家头像
                    expertTitle: null,			// 
                    expertName: null,			// 专家姓名	
                    expertOrganization: null,	// 专家机构
                    expertEmail: null			// 专家邮箱
                },
                enterpriseInfo: {	// 	企业信息
                    enterpriseId: null,	
                    enterpriseLogoPath: null,	// 企业头像
                    enterpriseName: null,		// 企业姓名
                    enterpriseAddress: null,	// 企业地区
                    enterpriseArea: null,		// 企业领域
                }
			}
		},
        onLoad(data) {
            console.log(data.reportId)
            this.inReportId = data.reportId
            this.expertInfo.expertId = 667
            this.enterpriseInfo.enterpriseId = 666
            this.needInfo.needId = 49
            this.getOrderDetailInfo()
        },
        computed: {
            ...mapState(['userInfo'])
        },
		methods: {
			async getOrderDetailInfo() {
                let output = await getOrderReport(this.inReportId)
                console.log(output)
                this.dataArray[0].time = output.orderInfo.needPostTime
                this.dataArray[1].time = output.orderInfo.orderStartTime
                this.dataArray[2].time = output.orderInfo.orderEndTime
                this.needInfo = output.needInfo
                this.expertInfo = output.expertInfo
                this.enterpriseInfo = output.enterpriseInfo
            },
            gotoNeedDetail() {
                uni.navigateTo({url: '../../pages/need-detail/detail?id=' + this.needInfo.needId})
            },
            gotoExpertDetail() {
                // console.log(this.expertInfo.expertId)
                uni.navigateTo({url: '../../pages/user-space/user-space?uid=' + this.expertInfo.expertId})
            },
            goToEnterpriseDetail() {
                uni.navigateTo({url: '../../pages/user-space/user-space?uid=' + this.enterpriseInfo.enterpriseId})
            }
		},
		components: {
			authorCard,
			companyCard,
			requireCard,
			timeAxis,
		}
	}
</script>

<style>
	.title {
		font-weight: 600;
		font-size: 18px;
		margin-top: 5px;
		margin-bottom: 5px;
		margin-left: 10px;
	}

</style>
