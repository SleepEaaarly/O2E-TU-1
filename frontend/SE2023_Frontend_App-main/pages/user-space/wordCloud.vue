<template>
	<view>
		<uni-section title="兴趣领域" type="line">
			<!-- 专家动态的词云 -->
			<view class="charts-box">
				<qiun-data-charts 
				  type="word"
				  :opts="opts"
				  :chartData="chartData"
				/>
			</view>
			
			<!-- 若无权限显示这个 -->
			<!-- <view v-show="false">
				<no-permit-see></no-permit-see>
			</view> -->
		</uni-section>

	</view>
</template>

<script>
	import noPermitSee from '@/components/common/no-permit-see.vue'
	export default {
		components:{ noPermitSee, },
		data() {
			return {
				chartData: {},
				//您可以通过修改 config-ucharts.js 文件中下标为 ['word'] 的节点来配置全局默认参数，如都是默认参数，此处可以不传 opts 。实际应用过程中 opts 只需传入与全局默认参数中不一致的【某一个属性】即可实现同类型的图表显示不同的样式，达到页面简洁的需求。
				opts: {
					color: ['#1890FF','#91CB74','#FAC858','#EE6666','#73C0DE','#3CA272','#FC8452','#9A60B4','#ea7ccc'],
					padding: undefined,
					extra: {
					  word: {
						type: 'normal',
						autoColors: false
					  }
					}
				}
			}
		},
		// ctmd傻逼玩意！子组件这里mounted()如果换成onReady()就啥也加载不出来了
		mounted() {
		    this.getServerData()
		},
		methods: {
			getServerData() {
			    //模拟从服务器获取数据时的延时
			    //模拟服务器返回数据，如果数据格式和标准格式不同，需自行按下面的格式拼接
				let res = {
					series: [
					  {
						name: '机器学习',
						textSize: 25,
						data: undefined
					  },
					  {
						name: '自然语言处理',
						textSize: 20,
						data: undefined
					  },
					  {
						name: '计算机视觉',
						textSize: 20,
						data: undefined
					  },
					  {
						name: '强化学习',
						textSize: 20,
						data: undefined
					  },
					  {
						name: '大数据',
						textSize: 20,
						data: undefined
					  },
					  {
						name: '智能交通',
						textSize: 20,
						data: undefined
					  },
					  {
						name: '智慧城市',
						textSize: 20,
						data: undefined
					  },
					  {
						name: '目标检测',
						textSize: 20,
						data: undefined
					  },
					  {
						name: '数据编织',
						textSize: 10,
						data: undefined
					  },
					  {
						name: '网络安全网格',
						textSize: 12,
						data: undefined
					  },
					  {
						name: '隐私增强计算',
						textSize: 10,
						data: undefined
					  },
					  {
						name: '组装式应用',
						textSize: 12,
						data: undefined
					  },
					  {
						name: '决策智能',
						textSize: 10,
						data: undefined
					  },
					  {
						name: '跨全端',
						textSize: 12,
						data: undefined
					  },
					  {
						name: '云原生平台',
						textSize: 10,
						data: undefined
					  },
					  {
						name: '超级自动化',
						textSize: 12,
						data: undefined
					  }
					]
				}
				this.chartData = JSON.parse(JSON.stringify(res))
			},
		}
	}
</script>

<style scoped>
	/* 请根据实际需求修改父元素尺寸，组件自动识别宽高 */
	.charts-box {
		width: 100%;
		height: 215px;	/* 小 于这个值会把上面uni-section的字挡住 */
	}
</style>
