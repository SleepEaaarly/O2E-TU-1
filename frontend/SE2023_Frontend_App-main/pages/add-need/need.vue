<template>
	<view class="container">
		<view class="tui-status-bar">
			<uni-card :is-shadow="false" is-full>
				<text class="uni-h6">需求描述</text>
			</uni-card>
		</view>
		<view class="need-form">
			<form @submit="submit" @reset="reset">
				<uni-section title="需求标题" subTitle="为您的需求总结一个标题" type="line" padding>
					<uni-easyinput v-model="title" focus placeholder="请输入内容" @input="inputTitle"></uni-easyinput>
				</uni-section>
				<uni-section title="需求描述" subTitle="详细描述您的需求" type="line" padding>
					<uni-easyinput type="textarea" v-model="description" placeholder="请输入内容" @input="inputDescription"></uni-easyinput>
				</uni-section>
				<uni-section title="经费" subTitle="为您的需求标上价格 ( 单位: 万元 ) " type="line" padding>
					<uni-easyinput type="digit" v-model="money" placeholder="单位:万元" @input="inputMoney"></uni-easyinput>
				</uni-section>
				<uni-section title="开始日期" subTitle="请选择需求开始日期" type="line" padding>
					<view class="date-set">
						<uni-datetime-picker type="datetime" v-model="start_time" @change="changeLogStart" />
					</view>
				</uni-section>
				<uni-section title="结束日期" subTitle="请选择需求结束日期" type="line" padding>
					<view class="date-set">
						<uni-datetime-picker type="datetime" v-model="end_time" @change="changeLogEnd" />
					</view>
				</uni-section>
				<uni-section title="关键词" subTitle="推荐您输入3个以内英文关键词, 并以英文分号分开" type="line" padding>
					<uni-easyinput v-model="key_word" placeholder="请输入关键词" @input="inputKeyword"></uni-easyinput>
				</uni-section>
				<uni-section title="领域" subTitle="请为您的需求确定一个领域方向" type="line" padding>
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
				<uni-section title="地址" subTitle="请为您的需求添加地址" type="line" padding>
					<uni-easyinput v-model="address" placeholder="请输入需求地址" @input="inputAddress"></uni-easyinput>
				</uni-section>
				<uni-section title="紧急程度" subTitle="请为您的需求进行紧急估量" type="line" padding></uni-section>
				<view class="uni-list">
					<radio-group @change="radioChange">
						<label class="uni-list-cell uni-list-cell-pd" v-for="(item, index) in emergencyItems" :key="item.value">
							<view class="emergency-evaluate">
								<radio :value="item.value" :checked="index === emergency" />
							</view>
							<view>{{item.name}}</view>
						</label>
					</radio-group>
				</view>
				<!-- <uni-section title="预估人数" subTitle="为您的需求商定所需人数" type="line" padding>
					<uni-easyinput type="digit" v-model="predict" placeholder="请输入内容" @input="inputPredict"></uni-easyinput>
				</uni-section> -->
				
				<view class="uni-btn-v">
					<button type="primary" form-type="submit">直接发布</button>
					<button type="primary" @click="saveNeed">保存</button>
					<button type="default" form-type="reset">清除</button>
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
	import {
		addneed,
		saveneed
	} from '@/api/add-need.js'
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
		watch: {
			datetimesingle(newval) {
				console.log('单选:', this.datetimesingle)
			},
			range(newval) {
				console.log('范围选:', this.range)
			},
			datetimerange(newval) {
				console.log('范围选:', this.datetimerange)
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
			//this.userID = data.uid;
			
			this.company_id = this.userInfo.id
			console.log('onLoad in certification '+ this.userID)
		},
		methods: {
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
			inputRegisterCapital(e) {
				this.register_capital = e.detail
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
			async submit() {
				console.log("start_submit")
				let data = {
					'company_id': this.company_id,
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
				}
				let validate_answer = this.validate(data)
				if (validate_answer) {
					console.log("validate_success!")
					let result = await addneed(data)
					if (result&&result.code) {
						console.log("submit_fail!!")
						this.$http.toast('需求创建失败！')
					} else {
						console.log("submit_success!")
						this.$http.toast('需求创建成功！')
						this.back()
					}
				} else {
					this.$http.toast('需求创建失败！')
				}
			},
			reset: function(e) {
				this.title = '',
				this.description = '',
				this.money = '',
				this.start_time = '',
				this.end_time = '',
				this.key_word = '',
				this.field = 0,
				this.address = '',
				this.state = 0,
				this.emergency = '',
				this.index = 0
			},
			async saveNeed() {
				let data = {
					'company_id': this.company_id,
					'title': this.title,
					'description': this.description,
					'money': this.money,
					'start_time': this.start_time,
					'end_time': this.end_time,
					'key_word': this.key_word,
					'field': this.field,
					'address': this.address,
					'state': 2,
					'emergency': this.emergency,
				}
				let validate_answer = this.validate(data)
				if (validate_answer) {
					let result = await saveneed(data)
					if (result&&result.code) {
						this.$http.toast('需求保存失败！')
					} else {
						this.$http.toast('需求保存成功！')
						this.back()
					}
				}
			}
		}
	}
</script>

<style lang="scss" scoped>
	.container {
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
