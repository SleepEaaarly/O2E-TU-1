<template>
	<view>
	<uni-card>
		<view>
			<uni-row :span="24" class="title">
				<uni-col class="title" :span="22">
					<view @click="openDetail">
						{{item.title}}
					</view>
				</uni-col>
				<uni-col class="operation" :span="2" v-if="manage">
					<uni-icons type="more" @click="showToast('bottom')" size="18" class="operation"></uni-icons>
				</uni-col>
			</uni-row>
			<view @click="openDetail">
				<uni-row class="detail">
					<uni-col :span="12" class="detail">
						研发领域：<text class="detail-field">{{field_items[item.field]}}</text>
					</uni-col>
					<uni-col :span="12" class="detail">
						研发金额：<text class="detail-money">￥{{item.money}}万</text>
					</uni-col>
				</uni-row>
				<uni-row class="description">
					<uni-col class="description-text" :span="23">
						{{item.description}}
					</uni-col>
				</uni-row>
			</view> 
			<uni-row>
				<uni-col :span="16">
					<uni-row class="location">
						<uni-icons type="location" size="18"></uni-icons>
						<text>所在地：{{item.address}}</text>
					</uni-row>
					<uni-row class="location">
						<uni-icons type="calendar" size="18"></uni-icons>
						<text>截止时间：{{item.end_time}}</text>
					</uni-row>
					<uni-row class="location">
						<uni-icons type="auth" size="18"></uni-icons>
						<text>
							已对接专家：
						</text>
						<!-- 专家的头像们 -->
						<text v-if="item.experts==undefined || item.experts.length == 0">
							暂无
						</text>
						<view class="expert-header-view">
							<view v-for="(expert, index) in item.experts" :key="index">
								<image :src="expert.expert_icon" mode="widthFix" lazy-load 
									class="expert-image" 
									:title="expert.expert_name"
									@click="seeExpertHome(expert.expert_id)"></image>
							</view>
						</view> 
						
					</uni-row>
				</uni-col>
				<uni-col :span="7" class="buttons" :offset="1" v-if="!edit">
					<button type="primary" class="buttons-text" @click="openDetail">查看详情</button>
				</uni-col>
			</uni-row>
		</view>
		<uni-row>
			<view v-if="edit">
				<button type="primary" @click="goToRecommend" class="operation-buttons">
					专家推荐
				</button>
			</view>
		</uni-row>
		<view v-if="showExpert">
			<view v-for="(expert, index) in expertList">
				<view class="expert-info">
					<uni-row :span="24">
						<uni-col :span="3">
							<image :src="expert.userpic" mode="widthFix" lazy-load class="expert-image"></image>
						</uni-col>
						<uni-col :span="13">
							<uni-row>
								<uni-col>
									<text class="expert-name">
										{{expert.name}}
									</text>
								</uni-col>
							</uni-row>
							<uni-row>
								<text class="expert-organization">
									{{expert.organization}}
								</text>
							</uni-row>
							<uni-row>
								<uni-col>
									<text style="color:blue" class="expert-phone">
									{{expert.phone}}
									</text>
								</uni-col>
							</uni-row>
							<!-- <uni-row v-show="">
								<text class="expert-description">
									{{expert.profile}}
								</text>
							</uni-row> -->
						</uni-col>
						<uni-col :span="8">
							<button type="primary" @click="contact" class="expert-button">立即对接</button>
						</uni-col>
					</uni-row>
				</view>
			</view>
		</view>
	</uni-card>
	
	<uni-popup ref="popup" background-color="#fff">
		<view class="popup-content">
			<uni-row>
				<uni-col :span="8" class="operation-button">
					<view @click="editneed">
						<uni-row>
							<uni-icons type="refreshempty" size="24"></uni-icons>
						</uni-row>
						<uni-row>
							<text>编辑</text>
						</uni-row>
					</view>
				</uni-col>
				<uni-col :span="8" class="operation-button">
					<view @click="deleteneed">
						<uni-row>
							<uni-icons type="minus" size="24"></uni-icons>
						</uni-row>
						<uni-row>
							<text>删除</text>
						</uni-row>
					</view>
				</uni-col>
				<uni-col :span="8" class="operation-button" v-if="edit != 2">
					<view @click="endneed">
						<uni-row>
							<uni-icons type="checkmarkempty" size="24"></uni-icons>
						</uni-row>
						<uni-row>
							<text>结束</text>
						</uni-row>
					</view>
				</uni-col>
				<uni-col :span="8" class="operation-button" v-else>
					<view @click="issue">
						<uni-row>
							<uni-icons type="checkmarkempty" size="24"></uni-icons>
						</uni-row>
						<uni-row>
							<text>发布</text>
						</uni-row>
					</view>
				</uni-col>
			</uni-row>
		</view>
	</uni-popup>
	
	<uni-popup ref="popup_finished" background-color="#fff">
		<view class="popup-content">
			<uni-row>
				<uni-col class="operation-button">
					<view @click="deleteneed">
						<uni-row>
							<uni-icons type="minus" size="24"></uni-icons>
						</uni-row>
						<uni-row>
							<text>删除</text>
						</uni-row>
					</view>
				</uni-col>
			</uni-row>
		</view>
	</uni-popup>
	</view>
</template>

<script>
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
	import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniFav from '@/components/uni-fav/uni-fav.vue'
	import uniCard from '@/components/uni-card/uni-card.vue'
	import uniPopup from '@/components/uni-popup/uni-popup.vue'
	import { picUrl } from '@/api/common.js'
	export default {
		components:{
			uniRow,
			uniCol,
			uniFav,
			uniCard,
			uniPopup
		},
		props:{
			item:Object,
			index:Number,
			userInfo:Object,
			edit: {
				type:Number,
				default: 0
			},
			expertList: {
				type: Array,
				default: ()=>[]
			},
			showExpert: {
				type: Boolean,
				default: false,
			},
			manage: {
				type: Boolean,
				default: false,
			},
			manage_finished: {
				type: Boolean,
				default: false,
			}
		},
		data() {
			return {
				type: 'bottom',
				gutter: 0,
				nvueWidth: 730,
				field_items: [
					'信息技术', '装备制造', '新材料', '新能源', '节能环保', '生物医药', '科学创意', '检验检测', '其他'
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
				],
				matched_explist: [],	//已对接专家列表
			}
		},
		
		methods: {
			openDetail(){
				this.$emit('openDetail',this.item)
			},
			editneed() {
				this.$refs.popup.close()
				this.$emit('editneed', this.item)
			},
			deleteneed() {
				if(!this.manage_finished) {
					this.$refs.popup.close()
				} else {
					this.$refs.popup_finished.close()
				}
				this.$emit('deleteneed', this.item)
			},
			endneed() {
				this.$refs.popup.close()
				this.$emit('endneed', this.item)
			},
			issue() {
				this.$refs.popup.close()
				this.$emit('issue', this.item)
			},
			goToRecommend() {
				this.$emit('goToRecommend', this.item, this.index)
			},
			contact(expert) {
				console.log('expert:'+expert.expert_id)
				this.$emit('contact', this.item, expert)
			},
			// 点击头像，查看专家主页
			seeExpertHome(id){
				console.log('正在跳转到专家：'+id+'的主页')
				uni.navigateTo({ url: '/pages/user-space/user-space?uid=' + id })
			},
			showToast(type) {
				// open 方法传入参数 等同在 uni-popup 组件上绑定 type属性
				if(!this.manage_finished) {
					this.$refs.popup.open(type)
				} else {
					this.$refs.popup_finished.open(type)
				}
			}
		}
	}
</script>


<style scoped>
.title {
	font-size: 30upx;
	font-weight: 600;
	color: #0A98D5;
}
.operation {
	float: right;
}
.detail {
	font-weight: 200;
	font-size: 20upx;
}
.detail-field {
	font-weight: bold !important;
}
.description {
	border-radius: 20upx 20upx 20upx 20upx;
	background-color: #F5FFF0;
}
.description-text {
	margin: 10upx;
	font-size: 25upx;
	font-weight: 100;
}
.location {
	font-size: 20upx;
}
.buttons {
	margin-top: 75upx;
}
.buttons-text {
	font-size: 20upx;
}
.operation-button {
	text-align: center;
}
.operation-buttons {
	height: 60upx;
	text-align: center;
	font-size: small;
	margin-left: 10upx;
	margin-right: 10upx;
	/* box-shadow: 0 0 1upx rgba(0, 0, 0, .12), 1upx 0 0 rgba(0, 0, 0, .04) */
}
.expert-info {
	background-color: #FFFFFD;
	margin-top: 20upx;
}
.expert-image {
	width: 50upx;
	height: 50upx;
	border-radius: 50px;
	margin-right: 3px;
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
.expert-organization {
	color: skyblue;
}
</style>
