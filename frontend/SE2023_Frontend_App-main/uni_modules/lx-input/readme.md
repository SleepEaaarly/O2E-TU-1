# lx-input

### 属性:

| 属性        | 类型    | 默认值     | 说明                                                       |
| ----------- | ------- | ---------- | ---------------------------------------------------------- |
| value       | String  | ''         | 输入框绑定值，支持v-model                                  |
| list        | Array   | []         | 下拉框显示数据                                             |
| hidden.sync | Boolean | false      | 聚焦时返回true, 点击其他地方会返回false，解决input滑动穿透 |
| labelName   | String  | label      | list列表显示的字段名                                       |
| isLoading   | Boolean | false      | 外部传入，显示加载中                                       |
| placeholder | String  | 请输入内容 | 输入框提示                                                 |
| disabled    | Boolean | false      | 外部传入， 禁止聚焦                                        |

### 事件:

| 事件名    | 说明                                         |
| --------- | -------------------------------------------- |
| input     | 当前输入框内容                               |
| unAble    | 禁止聚焦点击时触发                           |
| focus     | 聚焦时触发                                   |
| clickMask | 下拉框激活时，点击其他地方触发，会关闭下拉框 |
| clickItem | 点击某一项触发， 返回点击的list的子项        |



### 简单示例:

```

<template>
	// page-meta 解决input聚焦时滑动穿透， 你有其他方案可以用自己的方案
	<page-meta :page-style="`overflow: ${ hidden ? 'hidden' : 'unset'}`"></page-meta>
	<view class="content">
		<view class="inputContent">
			<view class="label">省级</view>
			<lx-input class="input" v-model="value1" :list="list1" :hidden.sync="hidden"></lx-input>
		</view>
		<view class="inputContent">
			<view  class="label">市级</view>
			<lx-input class="input" v-model="value2" :list="list2" :hidden.sync="hidden"></lx-input>
		</view>
		<view class="inputContent">
			<view  class="label">县级</view>
			<lx-input class="input" v-model="value3" :list="list3" :hidden.sync="hidden"></lx-input>
		</view>
		<view style="height: 1000px;"></view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				value1:'',
				value2:'',
				value3:'',
				list1:[],
				list2:[],
				list3:[],
				
				hidden:false,
				 
			}
		}
	}
</script>

<style lang="scss">
	.content {
		padding: 0 30rpx;
		.inputContent{
			display: flex;
			align-items: center;
			margin-top:100rpx;
			.label{
				font-size: 30rpx;
				font-weight: bold;
				margin-right: 15rpx;
			}
			.input {
				flex:1;
			}
		}
	}
</style>
```

