<template>

	<view class="uni-navbar">
		
		<view class="uni-navbar__content" :class="{'uni-navbar--fixed': !!fixed,'uni-navbar--shadow':!!border,'uni-navbar--border':!!border}" :style="{'background-color':backgroundColor}">
			<!-- 状态栏 -->
			<uni-status-bar v-if="statusBar"></uni-status-bar>
			<!-- 导航栏 -->
			<view class="uni-navbar__header" :style="{color:color}">
				<!-- 左边按钮 -->
				<view class="uni-navbar__header-btns" @tap="onClickLeft">
					<view v-if="leftIcon.length">
						<u-icon :type="leftIcon" :color="color" size="24"></u-icon>
					</view>
					<view v-if="leftText.length" class="uni-navbar-btn--left-text" :class="{'uni-navbar-btn-icon-left':!leftIcon.length}">{{leftText}}</view>
					<slot name="left"></slot>
				</view>
				<!-- 中间部分 -->
				<view class="uni-navbar__header-container">
					<view v-if="title.length" class="uni-navbar__header-container-inner">{{title}}</view>
					<!-- 标题插槽 -->
					<slot></slot>
				</view>
				<!-- 右边按钮 -->
				<view class="uni-navbar__header-btns" @tap="onClickRight">
					<view v-if="rightIcon.length">
						<u-icon :type="rightIcon" :color="color" size="24"></u-icon>
					</view>
					<!-- 优先显示图标 -->
					<view v-if="rightText.length&&!rightIcon.length" class="uni-navbar-btn-text">{{rightText}}</view>
					<slot name="right"></slot>
				</view>
			</view>
		</view>
		<view class="uni-navbar__placeholder" v-if="fixed">
			<uni-status-bar v-if="statusBar"></uni-status-bar>
			<view class="uni-navbar__placeholder-view"></view>
		</view>
	</view>

</template>

<script>
	import uniStatusBar from '../uni-status-bar/uni-status-bar.vue'
	import uIcon from '../uni-icon/uni-icon.vue'

	export default {
		name: 'uni-nav-bar',
		components: {
			uniStatusBar,
			uIcon
		},
		props: {
			title: {
				type: String,
				default: ''
			},
			leftText: {
				type: String,
				default: ''
			},
			rightText: {
				type: String,
				default: ''
			},
			leftIcon: {
				type: String,
				default: ''
			},
			rightIcon: {
				type: String,
				default: ''
			},
			fixed: {
				type: [Boolean, String],
				default: false
			},
			color: {
				type: String,
				default: '#000000'
			},
			backgroundColor: {
				type: String,
				default: '#FFFFFF'
			},
			statusBar: {
				type: [Boolean, String],
				default: false
			},
			shadow: {
				type: [String, Boolean],
				default: true
			},
			border: {
				type: [String, Boolean],
				default: true
			}
		},
		mounted() {
			console.log(this.leftText)
		},
		methods: {
			onClickLeft() {
				this.$emit('click-left')
			},
			onClickRight() {
				this.$emit('click-right')
			}
		}
	}
</script>

<style>
	@charset "UTF-8";

	.uni-navbar__content {
		display: block;
		position: relative;
		width: 100%;
		background-color: #fff;
		overflow: hidden
	}

	.uni-navbar__content view {
		line-height: 44px
	}

	.uni-navbar__header {
		display: flex;
		flex-direction: row;
		width: 100%;
		height: 44px;
		line-height: 44px;
		font-size: 16px
	}

	.uni-navbar__header-btns {
		display: inline-flex;
		flex-wrap: nowrap;
		flex-shrink: 0;
		width: 120upx;
		padding: 0 12upx
	}
	.uni-navbar-btn--left-text{
		padding-left: 12upx
	}
	.uni-navbar__header-btns:first-child {
		padding-left: 0
	}

	.uni-navbar__header-btns:last-child {
		width: 60upx
	}

	.uni-navbar__header-container {
		width: 100%;
		margin: 0 10upx
	}

	.uni-navbar__header-container-inner {
		font-size: 30upx;
		text-align: center;
		padding-right: 60upx
	}

	.uni-navbar__placeholder-view {
		height: 44px
	}

	.uni-navbar--fixed {
		position: fixed;
		z-index: 998
	}

	.uni-navbar--shadow {
		box-shadow: 0 1px 6px #ccc
	}

	.uni-navbar--border:after {
		position: absolute;
		z-index: 3;
		bottom: 0;
		left: 0;
		right: 0;
		height: 1px;
		content: '';
		-webkit-transform: scaleY(.5);
		transform: scaleY(.5);
		background-color: #c8c7cc
	}
</style>