<template>
	<view class="inputBox" :style="{zIndex: isShowScrollView ? '100': '10'}">
		<view class="focusBox" @click.stop="toFocus">
			<input class="inputStyle" :placeholder="placeholder" :disabled="!isActive" :focus="isFocus" :value="value"
				@input="input" @focus="focus" @blur="blur"></input>
			<u-icon v-if="isShowScrollView && value" class="icon-close" color="#bbb" name="close-circle-fill"
				size="36rpx" @click.prevent.stop="clear"></u-icon>
		</view>
		<view class="srollViewBox" v-if="isShowScrollView"
			@touchmove.stop>
			<scroll-view class="scrollView" scroll-y>
				<block v-if="!isLoading">
					<view class="scrollView-item" v-for="(item,index) in list" :key="index"
						@click.stop="clickItem(item)">
						{{item[labelName]}}
					</view>
					<view v-if="!list.length">
						搜索结果为空
					</view>
				</block>
				<view class="loading" v-else>
					loading
				</view>
			</scroll-view>
		</view>
		<view class="mask" v-if="isShowScrollView" @click.stop="clickMask" @touchmove.stop></view>
	</view>
</template>

<script>
	export default {
		props: {
			value: {
				type: String,
				default: ''
			},
			list: {
				type: Array,
				default: () => ([])
			},
			hidden: {
				type:Boolean,
				default:false
			},
			labelName: {
				type: String,
				default: 'label'
			},
			isLoading: {
				type: Boolean,
				default: false
			},
			placeholder: {
				type: String,
				default: "请输入内容"
			},
			// 禁用输入框， 触发unAble
			disabled: {
				type: Boolean,
				default: false
			},
		},
		data() {
			return {
				isShowScrollView: false,
				isFocus: false,
				isActive: false,
			};
		},
		methods: {
			toFocus() {
				if (this.disabled) {
					this.$emit("unAble")
					return
				}
				this.isFocus = false
				this.isActive = true
				if (!this.isShowScrollView) {
					this.isShowScrollView = true
					this.$emit("update:hidden", this.isShowScrollView)
				}
				this.$nextTick(() => {
					this.isFocus = true
				})
			},
			focus() {
				this.$emit("focus")
			},
			blur() {
				this.isActive = false
				this.isFocus = true
				this.$nextTick(() => {
					this.isFocus = false
				})
			},
			clickMask() {
				this.isActive = false
				this.isShowScrollView = false
				this.$emit("update:hidden", this.isShowScrollView)
				this.isFocus = false
				this.$emit("clickMask")

			},
			clickItem(item) {
				this.isActive = false
				this.isShowScrollView = false
				this.$emit("update:hidden", this.isShowScrollView)
				this.isFocus = false
				this.$emit("clickItem", item)
			},

			input(e) {
				this.$emit('input', e.detail.value)
			},

			clear() {
				this.$emit('input', '')
			}
		}
	}
</script>

<style lang="scss" scoped>
	.inputBox {
		position: relative;
		padding: 0 14rpx;
		font-size: 28rpx;
		height: 86rpx;

		.focusBox {
			position: relative;

			.inputStyle {
				height: 86rpx;
				color: #006DF7;
				padding-right: 60rpx;
			}

			.icon-close {
				position: absolute;
				z-index: 11;
				right: 16rpx;
				top: 50%;
				transform: translate(0, -50%);
			}
		}

	}


	.srollViewBox {
		position: absolute;
		z-index: 3;
		left:0;
		right:0;
		bottom: -12rpx;
		transform: translateY(100%);
		background-color: #fff;
		border-radius: 12rpx;
		padding: 14rpx;
		box-shadow: 0 6rpx 16rpx 0 rgba(0, 0, 0, .08), 0 3rpx 6rpx -4rpx rgba(0, 0, 0, .12), 0 9rpx 28rpx 8rpx rgba(0, 0, 0, .05);

		.scrollView {
			border-radius: 12rpx;
			height: 200rpx;

			&-item {
				padding-left: 200rpx;
				margin-top: 16rpx;
				min-height: 33rpx;
				font-size: 28rpx;
				color: #BBBBBB;
				line-height: 33rpx;
			}
		}

		.loading {
			display: flex;
			align-items: center;
			justify-content: center;
			margin-top: 100rpx;
		}
	}

	.mask {
		position: fixed;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
	}
</style>
