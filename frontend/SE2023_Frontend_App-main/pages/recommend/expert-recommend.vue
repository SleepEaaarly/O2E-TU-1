<template>
	<view>
		<!-- 这里主要添加前面关于需求的描述信息补充 -->
		<view>
			<uni-row class="header">
				<uni-col :span="9" class="image">
					<image src="../../static/bgimg/need_contracted.jpg" mode="widthFix" lazy-load class="image-image"></image>
				</uni-col>
				<uni-col :span="14" :offset="1">
					<text class="need-title">{{need.title}}</text>
					<uni-row class="need-info">
						<uni-row :span="14" class="need-info-item">
							<uni-icons type="gear" size="18"></uni-icons>
							<text class="need-info-text">领域：{{field_items[need.field]}}</text>
						</uni-row>
						<uni-row :span="14" class="need-info-item">
							<uni-icons type="gear" size="18"></uni-icons>
							<text class="need-info-text">关键词：
								<view v-for="(keyword, index) in part_keywords" :key="index" class="keywords-tag">
									<uni-tag v-bind:text="keyword" type="royal" style="margin-left: 10upx; text-align: center; word-break: keep-all;"></uni-tag>
								</view>
							</text>
						</uni-row>
					</uni-row>
				</uni-col>
			</uni-row>
		</view>
		
		<!-- 这里主要是标题 -->
		<view class="Recommend-title">
			<uni-section class="recommend-section" title="推荐结果" subTitle="可直接联系对接~" type="circle">
			</uni-section>
			<button class="recommend-change" style="color:#590696" size="mini" @click="changeAiRecommend">
				<uni-icons type="refresh-filled" style="color:#590696" size="18"></uni-icons>
				换一换
			</button>
		</view>
		
		<!-- 这里增加对于专家的补充 -->
		<view class="Recommend">
			<view v-for="(expert, index) in expertRegister">
				<uni-card :title="expert.expert_name" :sub-title="expert.email" :extra="expert.expert_organization" :thumbnail="expert.userpic" @click="goToExpertInfo(expert)">
					<view>
						<text class="expert-title-head">匹配论文信息: </text>
						<text class="expert-title" style="color: #000080; margin-left: 30upx;">{{expert.title}}</text>
					</view>
					<view>
						<text class="expert-title-head">专家评价信息：</text>
					</view>
					<view>
						<text>合作体验</text>
						<uni-rate :readonly="true" :value="expert.comment[0]" />
						<text>完成速度</text>
						<uni-rate :readonly="true" :value="expert.comment[1]" />
						<text>专业水平</text>
						<uni-rate :readonly="true" :value="expert.comment[2]" />
					</view>
					<!-- <uni-list> -->
						<!-- <uni-list-item title="匹配信息" showArrow clickable @click="goToExpertInfo(expert)"></uni-list-item> -->
						<!-- <uni-list-item title="查看评价" showArrow clickable @click=""></uni-list-item> -->
					<!-- </uni-list> -->
					<view slot="actions" class="card-actions no-border">
						<view class="card-actions-item" @click="contact(expert)">
							<button type="primary" class="expert-button">立即对接</button>
						</view>
					</view>
				</uni-card>
			</view>
		</view>
		
		<view class="Recommend-title">
			<uni-section title="其他推荐" subTitle="其他推荐结果,请自行联系~" type="circle">
			</uni-section>
		</view>
		
		<view>
			<uni-row class="need-introduction">
				<uni-col :span="23" :offset="1">
					<uni-icons type="gear" size="18"></uni-icons>
					<text class="need-introduction-text">关键词：
						<view v-for="(keyword, index) in keywords" :key="index" class="keywords-tag">
							<uni-tag v-bind:text="keyword" type="royal" 
							style="margin-left: 10upx; overflow:hidden; text-overflow:ellipsis; white-space:no-wrap;"></uni-tag>
						</view>
					</text>
				</uni-col>
			</uni-row>
		</view>
		<view v-for="(expert, index) in expertOther">
			<uni-card :title="expert.expert_name" :extra="expert.expert_organization" @click="showToast">
				<text class="expert-title-head">匹配论文信息:</text>
				<text class="expert-title">{{expert.title}}</text>
			</uni-card>
		</view>
		
		<uni-section title="自主搜索" subTitle="没有满意的结果?" type="circle">
			<button type="primary" @click="goToUserSearch">
				<uni-icons type="search" size="20" color="#ffffff"></uni-icons>
				搜索专家
			</button>
		</uni-section>
		
		<view>
			<load-more loadtext="~~到底了~~"></load-more>
		</view>
		
		<uni-popup ref="popup" type="message">
			<uni-popup-message type="error" message="该专家用户暂未入驻,请企业自行联系~" :duration="2000"></uni-popup-message>
		</uni-popup>
		
		<!-- 推荐时的加载动画 -->
		<w-loading text="智能推荐中.." mask="true" click="true" ref="loading"></w-loading>
	</view>
</template>

<script>
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import loadMore from '@/components/common/load-more.vue'
	import { picUrl } from '@/api/common.js'
	import uniPopupMessage from '@/components/uni-popup-message/uni-popup-message.vue'
	import uniPopup from '@/components/uni-popup/uni-popup.vue'
	import { aiRecommend } from '@/api/manage-need.js'
	import { mapState } from 'vuex'
	import { createContact } from '@/api/need-detail.js'
	import wLoading from '@/components/w-loading/w-loading.vue'	// 加载动画
	
	export default {
		components: {
			uniCol,
			uniRow,
			loadMore,
			uniPopup,
			uniPopupMessage
		},
		data() {
			return {
				need: {},
				expertRegister: [],
				expertOther: [],
				field_items: [
					'信息技术', '装备制造', '新材料', '新能源', '节能环保', '生物医药', '科学创意', '检验检测', '其他'
				],
				showDescription: false,
				refCount: 0,	// 刷新次数计数
				curNeedId: '',	// 当前需求id
			}
		},
		computed: { 
			keywords: function () {
				let words = this.need.key_word
				let word_list = words.split(';')
				console.log('word_list')
				console.log(word_list.length)
				console.log(word_list[0])
				word_list.sort(function(a, b) {
					return a.length - b.length
				})
				return word_list
			},
			part_keywords: function() {
				if (this.keywords) {
					return this.keywords.slice(0, 2) 
				}
			},
			...mapState(['userInfo']) 
			
		},
		onLoad(option) {
			if (option) {
				try {
					let options = JSON.parse(decodeURIComponent(option.item))
					let object = options
					this.need = object
					this.initExperts(object.need_id)
					this.curNeedId = object.need_id	// 记录当前需求id
					
				} catch(e) {
					console.log(e)
				}
			} else {
				console.log('Error! no data is loaded')
			}
		},
		
		onReady(){
			this.$refs.loading.open()	// 打开动画钩子
		},
		
		methods: {
			async initExperts(id) {
				let experts = await aiRecommend(id)
				if (experts) {
					this.expertRegister = experts.register 
					this.expertOther = experts.other
					if (experts.register.length >= 5) {
						this.expertRegister = experts.register.slice(0, 4)
					} 
					if (experts.other.length >= 5) {
						this.expertOther = experts.other.slice(0, 4)
					}
				}
				this.validate()
				
				this.$refs.loading.close()	// 关闭动画钩子
			},
			validate() {
				console.log(this.expertRegister.length)
				for(var i = 0; i < this.expertRegister.length; i ++) {
					this.expertRegister[i].userpic = picUrl + this.expertRegister[i].userpic
				}
				for(var i = 0; i < this.expertOther.length; i ++) {
					this.expertOther[i].userpic = picUrl + this.expertOther[i].userpic
				}
			},
			goToExpertInfo(expert) {
				uni.navigateTo({ url:'../user-space/user-space?uid='+ expert.id })
				event.stopPropagation()
			},
			contact(expert) {
				let temp={
					expert_id:expert.id,
					enterprise_id:this.userInfo.id,
					need_id:this.need.need_id,
				}
				let s =createContact(temp)
				uni.navigateTo({ url:'../user-chat/user-chat?fid='+expert.id })
				event.stopPropagation()
			},
			showToast() {
				this.$refs.popup.open()
			},
			// 更换一批推荐结果
			changeAiRecommend() {
				console.log(this.refCount)
				this.refCount += 1
				this.refreshExperts(this.curNeedId)
			},
			// 依据refCount更新推荐结果
			async refreshExperts(id) {
				this.$refs.loading.open()	// 开启动画钩子
				
				let experts = await aiRecommend(id)
				if (experts) {
					this.expertRegister = experts.register 
					this.expertOther = experts.other
					if (experts.register.length >= 5) {
						this.expertRegister = experts.register.slice(0, 4)
					} 
					if (experts.other.length >= 5) {
						this.expertOther = experts.other.slice(0, 4)
					}
				}
				this.validate()
				
				this.$refs.loading.close()	// 关闭动画钩子
			},
			// 自己去搜专家
			goToUserSearch() {
				console.log('Click!')
				uni.navigateTo({ url: '../user-search/user-search' })
			}
		}
	}
</script>

<style>
	.detail {
		min-height: 1380upx;
		background-color: #F1F1F1;
		padding: 10upx;
	}
	.header {
		margin: 10upx;
		background-color: white;
		border: solid #F5FFF0 2upx;
		height: 24%;
	}
	.image-image {
		padding-top: 5%;
		width:100%;
	}
	.keywords-tag {
		display: inline;
	}
	.need-title {
		text-overflow: ellipsis;
		text-wrap: none;
		color: skyblue;
		font-weight: bold;
	}
	.need-info-item {
		height: auto;
		font-weight: 100;
		font-size: 20upx;
	}
	.need-introduction {
		max-height: 150upx;
		opacity: 0.8;
		background-color: #FFFFFD;
		margin-top: 10upx;
	}
	
	.expert-title-head {
		font-weight: 100;
		font-size: small;
	}
	
	.expert-info {
		background-color: #FFFFFD;
		margin-top: 20upx;
	}
	.expert-image {
		margin-top: 10upx;
		margin-left: 8upx;
		width: 80upx;
		border-radius: 50px;
		margin-right: 3px;
	}
	.expert-null-image {
		height: 40upx;
	}
	.expert-header-view{
		display: flex;
		flex-direction: row;
	}
	.expert-button {
		margin: 20upx;
		font-size: small;
	}
	.expert-name {
		font-weight: 900;
		font-size: medium;
	}
	.expert-phone {
		font-size: x-small;
	}
	.expert-null-organization {
		margin-left: 50upx;
		color: skyblue;
	}
	.expert-organization {
		color: skyblue;
	}

.recommend-section {
	display: inline-flex;
}

/* 换一换推荐结果按钮 */
.recommend-change {
	display: inline-flex;
	/* margin-left: auto; */
	justify-content: end;
}

</style>
