<template>
	<view class="common-list u-f animated fadeIn fast">
			<view class="common-list-r">
				<view class="topic-title">
					<text style="font-weight: bold;font-size:x-large;">{{item.title}}</text>
					<view class="common-list-r-time">
						{{field_items[item.field]}}
					</view>
					<view class="common-list-right" style="color: red">
						{{emergencyItems[item.emergency].name}}
					</view>
				</view>
				<view>
				</view>
				<view>
					<view class="common-list-r-time">
						{{item.enterprise_name}}
					</view>
					<view class="common-list-r-time">
						开始时间：{{item.start_time}}
					</view>
					<view class="common-list-r-time">
						结束时间：{{item.end_time}}
					</view>
					<view>
						已接收<view style="color: #FF0000;">{{item.real}}/{{item.predict}}</view>
					</view>
					<view>
						金额:{{item.money}}
					</view>
				</view>
				
				<view>
					<rich-text v-html="item.description"></rich-text>
				</view>
				
				<view>
					{{item.address}}
				</view>
			</view>
			
			<view>
				<tui-button type="primary">
					联系企业
				</tui-button>
			</view>
		</view>
</template>

<script>
	import {
		mapState,
		mapMutations
	} from "vuex"
	import {
		getNeedDetail
	} from "@/api/need-detail.js"
	
	var graceRichText = require("../../components/common/richText.js");
	export default {
		components: {
		},
		props:{
			item:Object,
			userInfo:Object,
		},
		data() {
			return {
				field_items: [
					"信息技术", "装备制造", "新材料", "新能源", "节能环保", "生物医药", "科学创意", "检验检测", "其他"
				],
				emergencyItems: [
					{
						value: '0',
						name: '低'
					},
					{
						value: '1',
						name: '中'
					},
					{
						value: '2',
						name: '高'
					}
				]
			}
		},
		onLoad(data) {
			// try {
			// 	this.initData(data.id)
			// } catch (e) {

			// }
			this.item = data
		},
		onShow(){
			try {
				this.initData(this.detail.id)
			} catch (e) {
			
			}
		},
		// 监听导航右边按钮
		onNavigationBarButtonTap(e) {
			
		},
		computed: {
			...mapState(['userInfo'])
		},
		methods: {
			// 初始化数据
			// async initData(id) {
			// 	// 修改窗口标题
			// 	uni.setNavigationBarTitle({
			// 		title: "详情"
			// 	});
			// 	let detail = await getNeedDetail(id)
			// 	this.item = detail
			// },
			formatRichText (html) {
				// 去掉img标签里的style、width、height属性
				let newContent= html.replace(/<img[^>]*>/gi,function(match,capture){
					match = match.replace(/style="[^"]+"/gi, '').replace(/style='[^']+'/gi, '');
					match = match.replace(/width="[^"]+"/gi, '').replace(/width='[^']+'/gi, '');
					match = match.replace(/height="[^"]+"/gi, '').replace(/height='[^']+'/gi, '');
					return match;
				});
				// 修改所有style里的width属性为max-width:100%
				newContent = newContent.replace(/style="[^"]+"/gi,function(match,capture){
					match = match.replace(/width:[^;]+;/gi, 'max-width:100%;').replace(/width:[^;]+;/gi, 'max-width:100%;');
					return match;
				});
				// 去掉<br/>标签
				newContent = newContent.replace(/<br[^>]*\/>/gi, '');
				// img标签添加style属性：max-width:100%;height:auto
				newContent = newContent.replace(/\<img/gi, '<img style="max-width:100%;height:auto;display:block;margin:0px auto;"');
				return newContent;
			},
		}
	}
</script>

<style>
	/* 评论 */
	.u-comment {
		padding: 0 20upx;
	}

	.u-comment-title {
		padding: 20upx;
		font-size: 30upx;
		font-weight: bold;
	}
</style>
