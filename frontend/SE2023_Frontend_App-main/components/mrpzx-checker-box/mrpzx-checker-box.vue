<template>
	<view class="checker-box">
		<slot />
	</view>
</template>

<script>
	export default {
		name: "checker",
        props: {
            value: {
                default: ""
            },
            type: {
                type: String,
                default: "radio"
            },
            must: {
                type: Boolean,
                default: false
            }
        },
        data () {
            return {
                hashCache: {} // {'a': true, 'b': false, ...}
            }
        },
        provide() {
        	return {
        		checker: this
        	}
        },
        created() {
        	this.childrens = []
        },
        methods: {
            /**
             * @param {Object} value radio时value为单个值，如 xxx，checkbox时为对象，如 {'xxx': true}
             * @param {Boolean} isCheck 是否选中
             */
            changeHandler (value, isCheck) {
                if ("radio" === this.type) {
                    if (!isCheck && this.must) {
                        let selected = this.childrens.find(e => e.value == value)
                        if (void 0 !== selected) {
                            return selected.isCheck = !0
                        }
                    }
                    this.$emit("input", value)
                    this.$emit("on-change", value, isCheck)
                    this.childrens.forEach((item, index) => {
                        if (item.isCheck && value !== item.value) {
                            item.isCheck = false
                        }
                    })
                } else if ("checkbox" === this.type) {
                    if (!isCheck && this.must) {
                        if (this.childrens.findIndex(e => e.isCheck) === -1) {
                            let _value = Object.keys(value)[0]
                            let selected = this.childrens.find(e => e.value == _value)
                            if (void 0 !== selected) {
                                return selected.isCheck = !0
                            }
                        }
                    }
                    Object.assign(this.hashCache, value)
                    let i = this.parseHashCache()
                    this.$emit("input", i)
                    this.$emit("on-change", i)
                }
            },
            clearCheck () {
                this.childrens.forEach((item, index) => {
                    if (item.isCheck) {
                        item.isCheck = false
                        this.hashCache[item.value] = false
                    }
                })
                let e = this.parseHashCache()
                this.$emit("update:value", e)
                this.$emit("on-change", e)
            },
            clear () {
                this.childrens.forEach((item, index) => {
                    if (item.isCheck) {
                        this.hashCache[item.value] = true
                    }
                })
                let e = this.parseHashCache()
                this.$emit("update:value", e)
            },
            checkAll () {
                this.childrens.forEach((item, index) => {
                    if (item.isCheck) {
                        this.hashCache[item.value] = true
                    }
                })
                let e = this.parseHashCache()
                this.$emit("update:value", e)
                this.$emit("on-change", e)
            },
            parseHashCache () {
                let t = [];
                for (let e in this.hashCache) {
                    if (!0 === this.hashCache[e]) {
                        t.push(e)
                    }
                }
                return t
            }
        }
	}
</script>

<style scoped>
    .checker-box {
        background-color: #fff;
        min-height: 900rpx;
        -webkit-box-shadow: 0 2px 4px 0 #e5e5e5;
        box-shadow: 0 2px 4px 0 #e5e5e5;
        border-radius: 8rpx
    }
</style>
