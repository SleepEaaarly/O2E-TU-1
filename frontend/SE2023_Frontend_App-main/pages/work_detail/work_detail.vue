<template>
	<view >
		<u-row>
			<text style="margin-left:50rpx;font-size: 20px;font-weight: 550;text-align:center;
			text-overflow:ellipsis;
			overflow:hidden;
			white-space:nowrap;">
			
			
			
			{{ work_info.workName }}</text>
		</u-row>
		
		<author-card
			:name="work_info.expert_name" 
			:title="work_info.expert_title" :institution="work_info.expert_organization"
			:mail="work_info.expert_mail"
			:logoPath="work_info.expert_logoPath"></author-card>
		
		<view style="
		margin-top: 2%;background-color: aliceblue;width:90%;margin-left: 3%;height: auto;
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
		
		<u-row style="margin-top: 20rpx;margin-left: 5%;margin-right: 5%;">
			<u-line></u-line>
		</u-row>
		<!-- <view style="
		margin-top: auto;background-color: aliceblue;width: 650rpx;margin-left: 35rpx;height: auto;
		border-left:8rpx solid cornflowerblue;
		background-color: aliceblue;padding-top: 10rpx;padding-left: 20rpx;padding-bottom: 10rpx;">
			<text class="intro">{{ work_info.work_content }}</text>
			
		</view> -->
		<view style = "margin-left: 5%;margin-right: 5%;margin-top: 15rpx;">
			<text class = "text-mixed">{{ work_info.work_content }}</text>
		</view>
		<u-row style="margin-top: 20rpx;margin-left: 5%;margin-right: 5%;">
			<u-line></u-line>
		</u-row>
		</view>
		  <!-- <scroll-view :style="{height:height+'px'}" scroll-y> -->
			  <scroll-view  scroll-y>
			<view v-for="(item, index1) in work_info.work_detail_pics" :key="index1">
				<image :src="picUrl + item" style="width: 100%;" mode="widthFix"></image>
			</view>
		  </scroll-view>
		<uni-row >
			<view v-if="!isSelf">
				<uni-col :span="8">
					<button type="primary" @click="goToExpertSpace" class="fix-button-left">专家详情</button>
				</uni-col>
				<uni-col :span="8" :offset="8">
					<button type="primary" @click="generateWorkReport" class="fix-button-right">生成报告</button>
				</uni-col>
			</view>
			<view v-if="isSelf">
				<uni-col :span="6">
					<button type="primary" @click="goToExpertSpace" class="fix-button-left">专家详情</button>
				</uni-col>
				<uni-col :span="6" :offset="3">
					<button type="primary" @click="generateWorkReport" class="fix-button-middle">生成报告</button>
				</uni-col>
				<uni-col :span="6" :offset="2">
					<button type="primary" @click="resultDelete" class="fix-button-right-del">删除成果</button>
				</uni-col>
			</view>
		</uni-row>
	</view>
	
</template>

<script>
	import { mapState, mapMutations } from 'vuex'
	import authorCard from"../../components/author_display_card.vue"
	import { getWork, resDel } from "@/api/work_detail.js"
	import { workGenerateCard } from '@/api/work_report.js'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import {
		picUrl
	} from '@/api/common.js'
	export default {
		computed: {
			...mapState(['userInfo']),
		},
		data() {
			return {
				work_id: 1,
				height: 500,
				isSelf: false,
				picUrl: '',
				work_info: {
					// "workName": 'A Summary of Machine Learning123123',
					// "expert_name": '占瑞乙',
					// "expert_title": '本科生',
					// "work_abstract": 'Here is a summary of some of the most commonly used methods in machine learning.',
					// "expert_organization": '北京航空航天大学',
					// "expert_logoPath": '/static/head_zry_fox.jpg',
					// "work_id": '',
					// "expert_id": '',
					// "user_id": '',
					// "work_pic": '/static/ML_Notes.png' ,
					// "expert_mail": "iszry@foxmail.com",
					// "work_period": "实验室",
					// "work_field": "科学创意",
					// "work_content":"大家好，我叫sunny11111111111111111111112222222222",
				}
			}
		},
		onLoad(data) {
			// console.log(data)
			// console.log('data should be:' + data.rid)
			this.work_id = data.rid
			this.loadData()
			this.picUrl = picUrl
		},
		methods: {
			async loadData(){
				// console.log('get work detail')
				this.work_info = await getWork(this.work_id)
				console.log(this.work_info)
				if(this.work_info.user_id == this.userInfo.id){
					this.isSelf = true
				}
				// console.log(this.work_info)
			},
			goToExpertSpace() {
				uni.navigateTo({ url:'../user-space/user-space?uid='+this.work_info.user_id })
			},
			async generateWorkReport() {
				// 调用生成报告的 api，后端负责将报告插入到对应的用户-系统聊天之中
				// console.log(this.userInfo.id)
				// console.log(this.work_info.work_id)
				await workGenerateCard(this.userInfo.id, this.work_info.work_id)
			},
			resultDelete(){
				let params = {
					"id": this.work_info.work_id
        		}
				console.log(this.work_info.work_id)
				resDel(params)
					.then((res) => {
						this.$message.info("删除成功！");
						// this.loadResult();
						console.log(res)
					}).then((res) => {
						that.reload()
					})
					.catch((error) => {
						console.log(error);
					});
				setTimeout(() => {
					uni.navigateBack({
						delta: 1
					});
    			}, 1000);

			}
		},
		components: {
			authorCard,
			uniCol,
			uniRow,
		},
		
	}
</script>

<style>

	.fix-button {
		background-color: white;
		position: fixed;
		bottom: 0upx;
		/* right: 10upx; */
		width: 100%;
		height: 120upx;
		z-index: 2;
	}
	.fix-button-left {
		margin: 20upx;
		font-size: 25upx;
		/* float: left; */
		left: 5upx;
		background-color: orange;
		/* float: left; */
	}
	.fix-button-middle {
		margin: 20upx;
		font-size: 25upx;
		/* float: left; */
		/* float: left; */
	}
	.fix-button-right-del {
		margin: 20upx;
		font-size: 25upx;
		right : 5upx;
		/* float: right; */
		background-color: red;
	}
	.fix-button-right {
		margin: 20upx;
		font-size: 25upx;
		right : 5upx;
		/* float: right; */
	}
	
	.text-mixed {
	 /* font-size: 18px; */
	  line-height: 1.5;
	  width: 90rpx;
	  white-space: normal;/*设置自动换行*/
	  /* overflow: hidden; */
	  /* text-overflow: ellipsis; */
	  word-wrap: break-word;
	  word-break: break-all;
	  
	}
	
	/* .text-mixed span {
	  display: inline-block;
	  vertical-align: middle;
	} */
	
	.text-mixed .chinese {
	  text-align: right;
	  margin-left: 5px;
	}
	
	.text-mixed .english {
	  text-align: left;
	  margin-right: 5px;
	}
	
	
</style>
