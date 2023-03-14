<template>
	<view>
		<uni-card is-full :is-shadow="false">
			<text class="uni-h6"> 这里是常见问题解答，如果在使用过程中有任何疑问，请与我们反馈！</text>
		</uni-card>
		
		<uni-section title="企业端" subTitle="企业端常见问题" type="line">
			<view class="example-body">
				<view class="uni-box">
					<uni-title class="h2" type="h2" title="1、我发布了需求，但是不想展示到需求平台上？"></uni-title>
				</view>
				<view class="uni-box">
					<text class="uni-text">
						当您不想展示在需求平台上时，可以在发布时选择“保存”选项。
					</text>
					<image src="../../static/question/index_1.png" class="uni-image" 
					mode="widthFix" lazy-load style="width: 100%;"/>
					<text class="uni-text">
						如果您需要发布到需求平台，可以选择直接发布。
					</text>
				</view>
				<view class="uni-box">
					<uni-title class="h2" type="h2" title="2、我如何管理需求的进度呢？"></uni-title>
				</view>
				<view class="uni-box">
					<text class="uni-text">
						对于需求，我们设置了三种状态：已完成、已发布、未发布。其中只有第一种状态下需求代表着结束，后面两种状态分别是需求发布到需求平台-未完成，需求未发布到需求平台-未完成。您可以在需求管理中修改需求状态信息。
					</text>
					<text class="uni-text">
						对于订单信息，您需要根据需求进行跟踪。进入需求管理后，点击需求进入需求详情：
					</text>
					<image src="../../static/question/index_2.png" class="uni-image"
					mode="widthFix" lazy-load style="width: 100%;"/>
					<text class="uni-text">
						然后在需求详情中找到订单信息，从而就可以对订单进行管理，即对需求的整体进度进行管理。
					</text>
					<image src="../../static/question/index_3.png" class="uni-image"
					mode="widthFix" lazy-load style="width: 100%;"/>
				</view>
				<view class="uni-box">
					<uni-title class="h2" type="h2" title="3、我对同一个专家有多个需求怎么处理？"></uni-title>
				</view>
				<view class="uni-box">
					<text class="uni-text">
						对于多个需求，您需要通过上述过程精准定位到与专家对应的特定需求，直接通过聊天界面寻找专家得到的最近一次的需求订单信息哦~
					</text>
				</view>
				<view class="uni-box">
					<uni-title class="h2" type="h2" title="4、我怎么和管理人员联系呢？"></uni-title>
				</view>
				<view class="uni-box">
					<text class="uni-text">
						您可以通过点击“我的”中“帮助与反馈”，和我们取得联系，欢迎您的来信！
					</text>
				</view>
			</view>
		</uni-section>
		
		<uni-section title="专家端" subTitle="专家端常见问题" type="line">
			<load-more loadtext="正在整理中---"></load-more>
		</uni-section>
	</view>
</template>

<script>
	import Index1 from '../../static/question/index_1.png'
	import Index2 from '../../static/question/index_2.png'
	import Index3 from '../../static/question/index_3.png'
	import uniSection from '@/components/uni-section/uni-section.vue'
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniTitle from '@/components/uni-title/components/uni-title/uni-title.vue'
	import loadMore from '@/components/common/load-more.vue'
	export default {
		components: {
			uniSection,
			uniRow,
			uniCol,
			uniTitle,
			loadMore
		},
		
		data() {
			return {
				
			}
		},
		
		methods: {
			
		}
	}
</script>

<style>
	.example-body {
			/* #ifndef APP-NVUE */
			display: block;
			/* #endif */
			padding: 10px;
		}
	
		.uni-text {
			font-size: 14px;
			line-height: 22px;
			color: #333;
		}
</style>
