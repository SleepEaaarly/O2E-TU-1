<template>
	<view class="uni-combox">
		<view v-if="label" class="uni-combox__label" :style="labelStyle">
			<text>{{label}}</text>
		</view>
		<view class="uni-combox__input-box">
			<input class="uni-combox__input" type="text" :placeholder="placeholder" v-model="inputVal" @input="onInput" @focus="onFocus" @blur="onBlur" />
			<!-- <uni-icons class="uni-combox__input-arrow" type="arrowdown" size="14" @click="toggleSelector"></uni-icons> 源代码注释掉上下距离太高不好看,去掉源码中class-->
			<uni-icons  type="arrowdown" size="18" v-if="inputVal===''" color="#999999" @click="toggleSelector"></uni-icons> <!-- 下箭头颜色#999999 -->
			<uni-icons  type="clear" size="18" v-else color="#999999" @click="clearInputVal"></uni-icons> <!-- add by limeng 追加的代码片段用叉号图标快速清空输入框 -->
			<view class="uni-combox__selector" v-if="showSelector">
				<scroll-view scroll-y="true" class="uni-combox__selector-scroll">
					<view class="uni-combox__selector-empty" v-if="filterCandidatesLength === 0">
						<text>{{emptyTips}}</text>
					</view>
					<view class="uni-combox__selector-item" v-for="(item,index) in filterCandidates" :key="index" @click="onSelectorClick(index)">
						<text>{{item}}</text>
					</view>
				</scroll-view>
			</view>
		</view>
	</view>
</template>

<script>
	import uniIcons from '../uni-icons/uni-icons.vue'
	export default {
		name: 'uniCombox',
		components: {
			uniIcons
		},
		props: {
			label: {
				type: String,
				default: ''
			},
			labelWidth: {
				type: String,
				default: 'auto'
			},
			placeholder: {
				type: String,
				default: ''
			},
			/** 不再需要这个属性
			candidates: {
				type: Array,
				default () {
					return []
				}
			},*/
			//add by limeng 20210702 增加 map 类型的属性
			candidatesMap: {
				type: Map,//这个类型会被警告但是不影响使用
				default () {
					return {}
				}
			},
			emptyTips: {
				type: String,
				default: '无匹配项'
			},
			value: {
				type: String,
				default: ''
			}
		},
		data() {
			return {
				showSelector: false,
				inputVal: '',  //输入框中输入的字符
				inputValId: '',//add by limeng 真实往后台传递的下拉id标识(比如项目id)
			}
		},
		computed: {
			labelStyle() {
				if (this.labelWidth === 'auto') {
					return {}
				}
				return {
					width: this.labelWidth
				}
			},
			filterCandidates() {
				//从candidatesMap 取值遍历所有key并赋值给内部变量candidates这个数组
				var candidates = [];//数组清空
				this.candidatesMap.forEach(function(value, key){
					var key = key;
					candidates.push(key);//获取的值给内部变量赋值
				})

				return candidates.filter((item) => {
					return item.indexOf(this.inputVal) > -1
				})
			},
			filterCandidatesLength() {
				return this.filterCandidates.length
			}
		},
		watch: {
			value: {
				handler(newVal) {
					this.inputVal = newVal
				},
				immediate: true
			},
		},
		methods: {
			toggleSelector() {
				this.showSelector = !this.showSelector
			},
			onFocus() {
				this.showSelector = true
			},
			onBlur() {
				/**update by limeng 20210710 上午周六
				  离开输入框焦点的时候输入框里的内容必须包含在下拉框列表中，
				  否则输入框内容是用户瞎写的没有意义，后台也无法识别
				  因此,强制用户必须以选中的为准
				  备注：提供输入功能仅仅是为了匹配合适的下拉选项，但不能以输入的值为准,必须以选中的为准
				*/
			    //if(this.candidates.indexOf(this.inputVal) > -1){ //则包含该元素
				if(this.filterCandidates.indexOf(this.inputVal) > -1){ //则包含该元素
				   	//alert("你输值在列表中");
					//关闭下拉(原代码保留)
					setTimeout(() => {
						this.showSelector = false
					}, 50)
				}else {
					//alert("你输的值不在列表中，此时下拉列表不能关闭，直到用户选中才能关闭下拉");
					return;
				}
			},
			onSelectorClick(index) {//index 只是这个数组中顺序的索引值比如 1,2,3...,和map中的key value没有关系
				this.inputVal = this.filterCandidates[index]//选中后给控件的输入框赋值
				this.inputValId = this.candidatesMap.get(this.inputVal);//根据输入框内容反查出对应的id或者code(以便提交到后台)
				this.showSelector = false;//选中后关闭下拉列表
				this.$emit('input', this.inputVal);//拿到子组件的值(name)赋值给父组件的input事件,即父组件的v-model绑定的属性
				this.$emit("setId",this.inputValId);//将name对应的id或者code返回给父组件,通过调用父组件的setId方法传值给父组件data中声明的变量
			},
			onInput() {
				setTimeout(() => {
					this.$emit('input', this.inputVal)
				})
			},
			clearInputVal(){
				this.inputVal='';
				this.inputValId = '';//同时清空输入框id
				this.$emit("setId",'');//将父组件的值也置为空
			}
		}
	}
</script>

<style scoped>
	.uni-combox {
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		height: 40px;
		flex-direction: row;
		align-items: center;
		/* border-bottom: solid 1px #DDDDDD;
 */
	}

	.uni-combox__label {
		font-size: 16px;
		line-height: 22px;
		padding-right: 10px;
		color: #999999;
	}

	.uni-combox__input-box {
		position: relative;
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex: 1;
		flex-direction: row;
		align-items: center;
	}

	.uni-combox__input {
		flex: 1;
		font-size: 33upx;/*16px*/
		height: 25px;
		line-height: 22px;
	}

	.uni-combox__input-arrow {
		padding: 10px;
	}

	.uni-combox__selector {
		box-sizing: border-box;
		position: absolute;
		top: 42px;
		left: 0;
		width: 100%;
		background-color: #FFFFFF;
		border-radius: 0px;
		box-shadow: #DDDDDD 4px 4px 8px, #DDDDDD -4px -4px 8px;
		z-index: 2;
	}

	.uni-combox__selector-scroll {
		max-height: 500px;/*200px*/
		box-sizing: border-box;
	}

	.uni-combox__selector::before {
		content: '';
		position: absolute;
		width: 0;
		height: 0;
		border-bottom: solid 6px #FFFFFF;
		border-right: solid 6px transparent;
		border-left: solid 6px transparent;
		left: 50%;
		top: -6px;
		margin-left: -6px;
	}

	.uni-combox__selector-empty,
	.uni-combox__selector-item {
		/* #ifdef APP-NVUE */
		display: flex;
		/* #endif */
		line-height: 50px;/*36px*/
		font-size: 33upx;/* 14px*/
		text-align: center;
		border-bottom: solid 1px #DDDDDD;
		margin: 0px 10px;
	}

	.uni-combox__selector-empty:last-child,
	.uni-combox__selector-item:last-child {
		border-bottom: none;
	}
</style>