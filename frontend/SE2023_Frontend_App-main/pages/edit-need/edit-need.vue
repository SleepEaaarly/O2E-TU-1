<template>
	<view class="container">
		<view class="tui-status-bar">
			<uni-card :is-shadow="false" is-full>
				<text class="uni-h6">修改需求</text>
			</uni-card>
		</view>
		<view class="need-form">
			<form @submit="update" @reset="reset">
				<uni-section title="需求标题" subTitle="修改您的需求标题" type="line" padding>
					<uni-easyinput v-model="title" focus placeholder="请输入内容" @input="inputTitle"></uni-easyinput>
				</uni-section>
				<uni-section title="需求描述" subTitle="修改您的需求描述" type="line" padding>
					<uni-easyinput type="textarea" v-model="description" placeholder="请输入内容" @input="inputDescription"></uni-easyinput>
				</uni-section>
				<uni-section title="需求经费" subTitle="修改您的需求价格 ( 单位: 万元 ) " type="line" padding>
					<uni-easyinput type="digit" v-model="money" placeholder="单位:万元" @input="inputMoney"></uni-easyinput>
				</uni-section>
				<uni-section title="关键词" subTitle="请将关键词控制在3个以内" type="line" padding>
					<uni-easyinput v-model="key_word" placeholder="请输入一些关键词,以英文分号分开" @input="inputKeyword"></uni-easyinput>
				</uni-section>
				<uni-section title="领域" subTitle="修改您的需求范畴" type="line" padding>
					<view class="uni-list">
						<view class="uni-list-cell">
							<view class="uni-list-cell-left">
								当前选择
							</view>
							<view class="uni-list-cell-db">
								<picker @change="inputField" :value="index" :range="field_items">
									<view class="uni-input">{{field_items[index]}}</view>
								</picker>
							</view>
						</view>
					</view>
				</uni-section>
				<uni-section title="地址" subTitle="修改您的需求地址" type="line" padding>
					<uni-easyinput v-model="address" placeholder="请输入需求地址" @input="inputAddress"></uni-easyinput>
				</uni-section>
				<uni-section title="紧急程度" subTitle="修改您的紧急程度" type="line" padding></uni-section>
				<view class="uni-list">
					<radio-group @change="radioChange">
						<label class="uni-list-cell uni-list-cell-pd" v-for="(item, index) in emergencyItems" :key="item.value">
							<view>
								<radio :value="item.value" :checked="index === emergency" />
							</view>
							<view>{{item.name}}</view>
						</label>
					</radio-group>
				</view>
				<view class="uni-btn-v">
					<button type="primary" form-type="submit">更新</button>
				</view>
			</form>
		</view>
	</view>
</template>
<script>
	import {
		mapMutations,
		mapState
	} from 'vuex'
	import { editneed } from '@/api/edit-need.js'
	import { getNeedDetail } from '@/api/need-detail.js'
	import uniCard from '@/components/uni_easyinput/uni-card/components/uni-card/uni-card.vue'
	import uniEasyinput from '@/components/uni_easyinput/uni-easyinput/components/uni-easyinput/uni-easyinput.vue'
	import uniSection from '@/components/uni-section/uni-section.vue'
	import uniDatetimePicker from '@/components/uni_datetime_picker/uni-datetime-picker/components/uni-datetime-picker/uni-datetime-picker.vue'
	export default {
		components:{
			uniCard,
			uniEasyinput,
			uniSection,
			uniDatetimePicker
		},
		data() {
			return {
				need_id: '',
				company_id: '',
				title: '',
				description: '',
				money: '',
				start_time: '',
				end_time: '',
				key_word: '',
				field: 0,
				address: '',
				state: 0,
				emergency: '',
				predict: 0,
				real: 0,
				index: 0,
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
				]
			}
		},
		mounted() {
			setTimeout(() => {
				this.datetimesingle = Date.now() - 2 * 24 * 3600 * 1000
				this.single = '2021-2-12'
				// this.range = ['2021-03-1', '2021-4-28']
				this.datetimerange = ['2021-07-08 0:01:10', '2021-08-08 23:59:59']
				// this.start = '2021-07-10'
				// this.end = '2021-07-20'
			}, 3000)
		},
		computed:{ ...mapState(['userInfo']) },
		onLoad(data) {
			this.initData(data.id)
		},
		// onShow(){
		// 	try {
		// 		this.initData(this.detail.id)
		// 	} catch (e) {
			
		// 	}
		// },
		methods: {
			async initData(id) {
				// uni.setNavigationBarTitle({
				// 	title: "需求详情"
				// });
				let data = await getNeedDetail(id)
				// console.log("data is" + data)
				this.company_id = this.userInfo.id
				this.need_id = id
				this.title = data.title
				this.description = data.description
				this.money = data.money
				this.start_time = data.start_time
				this.end_time = data.end_time
				this.key_word = data.key_word
				this.field = data.field
				this.address = data.address
				this.emergency = data.emergency
				this.index = this.field
			},
			// 修改完，返回...
			back() {
				uni.navigateBack()
			},
			inputTitle(e) {
				this.title = e.detail
			},
			inputDescription(e) {
				this.description = e.detail
			},
			inputMoney(e) {
				this.money = e.detail
			},
			show: function(e) {
				this.$refs.start_time.show()
			},
			changeLogStart(e) {
				console.log('----changeStartTime事件:', e)
			},
			changeLogEnd(e) {
				console.log('----changeEndTime事件:', e)
			},
 			inputKeyword(e) {
				this.key_word = e.detail
			},
			inputField(e) {
				this.index = e.detail.value
				console.log(this.index)
				this.field = this.index
			},
			inputAddress(e) {
				this.address = e.detail
			},
			inputPredict(e) {
				this.predict = e.detail
			},
			radioChange: function(evt) {
				for (let i = 0; i < this.emergencyItems.length; i++) {
					if (this.emergencyItems[i].value === evt.detail.value) {
						this.emergency = i
						break
					}
				}
			},
			validate: function(data) {
				let validate_answer = true
				if (data.title === '') {
					this.$http.toast('请输入需求标题！')
					validate_answer = false
				} else if (data.description === '') {
					this.$http.toast('请对需求输入具体描述！')
					validate_answer = false
				} else if (data.money === '') {
					this.$http.toast('请输入资金！')
					validate_answer = false
				} else if (data.start_time === '' || data.end_time === '' || data.start_time >= data.end_time) {
					this.$http.toast('请输入正确的时间！')
					validate_answer = false
				// } else if (!isKeyword(data.key_word)) {
				// 	this.$http.toast("请按照格式输入！")
				// 	validate_answer = false
				} else if (data.address === '') {
					this.$http.toast('请输入正确的地址！')
					validate_answer = false
				} else if (data.emergency === '') {
					this.$http.toast('请评定紧急程度！')
					validate_answer = false
				}
				// } else if (data.predict === '0' || data.predict === 0) {
				// 	this.$http.toast('预估人数必须大于0！')
				// 	validate_answer = false
				// }
				return validate_answer
			},
			isKeyword: function(key_word) {
				let mPattern = /^([\u4e00-\u9fa5])+(\s[\u4e00-\u9fa5])*/
				return mPattern.test(key_word)
			},
			async update() {
				let data = {
					// "company_id": this.company_id,
					'title': this.title,
					'description': this.description,
					'money': this.money,
					'start_time': this.start_time,
					'end_time': this.end_time,
					'key_word': this.key_word,
					'field': this.field,
					'address': this.address,
					'state': this.state,
					'emergency': this.emergency,
					// 'predict': this.predict,
					// "real": this.real
				}
				let company_id = this.company_id
				let need_id = this.need_id
				let validate_answer = this.validate(data)
				if (validate_answer) {
					let result = await editneed(company_id, need_id, data)
					if (result&&result.code) {
						this.$http.toast('需求更新失败！')
					} else {
						this.$http.toast('需求更新成功！')
						this.back()
					}
				}
			},
		}
	}
</script>

<style lang="scss" scoped>
	.container {
		min-height: 1000upx;
		.tui-page-title {
			width: 100%;
			font-size: 48rpx;
			font-weight: bold;
			color: $uni-text-color;
			line-height: 42rpx;
			padding: 110rpx 40rpx 40rpx 40rpx;
			box-sizing: border-box;
		}
		.tui-header {
			width: 100%;
			padding: 40rpx;
			display: flex;
			align-items: center;
			justify-content: space-between;
			box-sizing: border-box;
		}
		.tui-form {
			padding-top: 50rpx;
			
			.thorui-input-title {
				padding-right: 10rpx;
				font-size: 35rpx;
			}

			.tui-view-input {
				width: 100%;
				box-sizing: border-box;
				padding: 0 40rpx;

				.tui-cell-input {
					width: 100%;
					display: flex;
					align-items: center;
					padding-top: 48rpx;
					padding-bottom: $uni-spacing-col-base;

					input {
						flex: 1;
						padding-left: $uni-spacing-row-base;
					}

					.tui-icon-close {
						margin-left: auto;
					}

					.tui-btn-send {
						width: 156rpx;
						text-align: right;
						flex-shrink: 0;
						font-size: $uni-font-size-base;
						color: $uni-color-primary;
					}

					.tui-gray {
						color: $uni-text-color-placeholder;
					}
				}
			}

			.tui-cell-text {
				width: 100%;
				padding: 40rpx $uni-spacing-row-lg;
				box-sizing: border-box;
				font-size: $uni-font-size-sm;
				color: $uni-text-color-grey;
				display: flex;
				align-items: center;

				.tui-color-primary {
					color: $uni-color-primary;
					padding-left: $uni-spacing-row-sm;
				}
			}

			.tui-btn-box {
				width: 100%;
				padding: 0 $uni-spacing-row-lg;
				box-sizing: border-box;
				margin-top: 80rpx;
			}
		}
	}
	.date-set {
		background-color: #fff;
		padding: 10px;
	}
	.emergency-evaluate {
		margin: 5upx;
	}
	button {
		margin: 20upx;
		height: 70upx;
		font-size: small;
	}
</style>
