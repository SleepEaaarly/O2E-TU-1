<template>
	
	<view>
		<!-- 搜索栏 -->
		<view class = "search_view" style="margin-top: 10rpx;margin-left: 20px;margin-right: 20px;">
			<u-search placeholder="请输入搜索内容" :showAction = "false" ></u-search>
		</view>
		
		
		<view>
			<u-grid
			:border="false"
			col="3"
			style="margin-top: 10px;"
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
							<image class="logo" @click="navToNeeds"
							src="/static//company.png" 
							style = "height: 90px;width: 90px;margin-left: 10px;">
						</image>
						</u-row>
						<u-row style="margin-bottom: 10px;">
							<text class="grid-text">需求库</text>
							
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
					@click.native="workDetail"  
					:authorLogoPath="item['authorLogoPath']" 
					:author="item['author']"
					:date="item['date']" 
					:title="item['title']"
					:area="item['area']"
					:intro="item['intro']"
					:workLogoPath="item['workLogoPath']"
					:index="index1"></work-card>
				</block> 
				<load-more :loadtext="recommendList.loadtext"></load-more>
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
	export default {
		data() {
			return {
				recommendList: {
					loadtext: '没有更多数据了',
					id: 'recommend',
					list: [
						{
							'authorLogoPath': '/static/head.jpg',
							'author': 'Expert1',
							'date': '2023-3-30 21:41',
							'title': '超高分子量聚乙烯的研发制备',
							'area': '新材料',
							'intro': '一种线型结构的具有优异综合性能的热塑性工程塑料',
							'workLogoPath': '/static//logo.png',
						},
						{
							'authorLogoPath': '/static/head.jpg',
							'author': 'Expert2',
							'date': '2023-3-30 21:41',
							'title': '环境友好大豆蛋白质材料改性开发',
							'area': '生物医药',
							'intro': '该项目通过与其他生物可降解材料的共混，以及与纳米粒子的复合来得到廉价、加工性能良好、力学及防水性能改善的大豆蛋白质环境友好材料。',
							'workLogoPath': '/static//logo.png',
						}
					]
				},
			}
		},
		methods: {
			workDetail() {
				console.log('Jump to detail of the work')
			},
			navToExperts() {
				console.log('Jump to detail of the Experts')
				uni.navigateTo({
					url: '../../expert_store/expert_store/',
				})
			},
			navToWorks() {
				console.log('Jump to detail of the Works')
			},
			navToNeeds() {
				console.log('Jump to detail of the Needs')
			}
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
