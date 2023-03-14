<template>
	<view @click.stop="checkHandler" class="checker-item" :style="{'height': height}">
		<view class="checker-item-tag">
            <slot />
            <view v-if="special" class="checker-icon" :class="checkerBorder ? isCheck ? 'borderBlue' : 'borderGray' : ''" :style="{'width': width, 'line-height': height}">
                <text v-if="isCheck" class="checkboxes_sel checker-item-icon active"></text>
                <text v-else class="checkboxes_nor checker-item-icon"></text>
            </view>
            <view v-else class="checker-icon" :style="{'width': width, 'line-height': height}">
                <text v-if="isCheck" class="checker-item-icon active icon iconfont" :class="'circle' == iconType ? 'icon-radio_sel' : 'icon-checkbox_sel'"></text>
                <text v-else class="checker-item-icon  icon iconfont" :class="'circle' == iconType ? 'icon-radio_nor' : 'icon-checkbox_nor'"></text>
            </view>
        </view>
	</view>
</template>

<script>
	export default {
		name: "checker-item",
        props: {
            iconType: {
                default: "circle"
            },
            index: {
                type: [String, Number]
            },
            height: {
                type: String,
                default: ""
            },
            width: {
                type: String,
                default: ""
            },
            checked: {
                type: Boolean,
                default: !1
            },
            special: {
                type: Boolean,
                default: !1
            },
            value: {
                default: ""
            },
            checkerBorder: {
                type: Boolean,
                default: !1
            }
        },
        data: function() {
            return {
                isCheck: !1
            }
        },
        methods: {
            checkHandler: function() {
                if ('radio' === this.checker.type) {
                    this.checker.childrens.forEach(item => {
                    	if (item === this) {
                    		return
                    	}
                    	item.isCheck = false
                    })
                }
                this.isCheck = !this.isCheck
                if ("radio" === this.checker.type) {
                    this.checker.changeHandler(this.value, this.isCheck)
                } else if ("checkbox" === this.checker.type) {
                    let data = {}
                    data[this.value] = this.isCheck
                    this.checker.changeHandler(data)
                }
                this.$emit("checkItem", this.isCheck, this.index, this.value)
                this.$forceUpdate()
            },
            getValue: function() {
                return this.value
            },
            setChecker: function(t) {
                this.isCheck = t
            }
        },
        watch: {
            checked: function(t) {
                this.isCheck = t
            }
        },
        inject: ['checker'],
        created: function() {
            this.isCheck = this.checked
            this.checker.childrens.push(this)
            if (this.checker.type == 'radio') {
                if (this.isCheck) {
                    //如果选中了当前项，取消前一个的选中
                	let lastEl = this.checker.childrens[this.checker.childrens.length - 2]
                	if (lastEl) {
                		this.checker.childrens[this.checker.childrens.length - 2].isCheck = false
                	}
                }
            }
        }
	}
</script>

<style scoped src="./iconfont/iconfont.css"></style>
<style scoped>
    .checker-item {
        position: relative;
        padding: 0 38rpx
    }
    
    .checker-item:active {
        background-color: #f2f4f6;
        font-weight: 700
    }
    
    .checker-icon {
        position: absolute;
        right: 30rpx;
        top: 45rpx
    }

    .checker-item .checker-icon {
        width: 46rpx;
        height: 46rpx;
        border-radius: 23rpx;
        padding: 6rpx;
        text-align: left !important;
        -webkit-box-sizing: border-box;
        box-sizing: border-box
    }
    
    .checker-item .borderBlue,
    .checker-item .borderGray {
        border: 1px solid #2e5bff
    }
    
    .checker-item .checker-item-icon {
        width: 36rpx;
        height: 36rpx;
        display: block
    }
    
    .checker-item .icon-radio_nor {
        color: #d2d4db
    }
    
    .checker-item .icon-radio_sel {
        color: #2e5bff
    }
    
    .checker-item .icon-checkbox_nor {
        color: #d2d4db
    }
    
    .checker-item .icon-checkbox_sel {
        color: #2e5bff
    }
</style>
