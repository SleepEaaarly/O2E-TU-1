<template>
	<view>
		<fui-card :footer-line="false" style ="height: 100px;">
			 <u-row style="margin-bottom: 0%;">
			        <u-col span="3">
			            <image v-if="logoPath" class="logo" :src="logoPath" 
						style = "max-height: 70px;max-width: 70px;margin-left: 10px;margin-top: 15px;border-radius: 20px;">
						</image>
						<image v-else class="logo" :src="defaultPicPath"
						style = "max-height: 70px;max-width: 70px;margin-left: 10px;margin-top: 15px;border-radius: 20px;">
						</image>
					</u-col>
			        <u-col span="9">
						<u-row style="margin-top: 20px;">
							<u-col span="7">
								<u-row>
									<text class = "expertTitle">{{name}}</text>
								<!-- <u-tag v-if="title" :text="title" plain plainFill type="warning"  shape="circle" size = "mini" style="margin-left: 10px;"> </u-tag>
							 -->
									
								</u-row>
								
							</u-col>
							<u-col span="5">
								<u-button @click="expertDetail" type="primary" text="查看详情" size = "mini" style = "width: 90px;height: 28px;"></u-button>
							
							</u-col>
							
						</u-row>
						<u-row style="margin-top: 10px;margin-bottom: 0%;margin-left: 5px;">
							
							<u-tag :text="institution" plain size="mini" class="my-tag"> </u-tag>
							<u-tag v-if="title" :text="title" plain plainFill type="warning"  shape="circle" size = "mini" 
							style="margin-left: 5px;" class="title-tag" ellipsis> </u-tag>
														
							<!-- <text style="font-size: 10px;margin-left: 5px;
							text-overflow:ellipsis;
							overflow:hidden;
							white-space:nowrap;">
							{{mail}}</text> -->
						</u-row>
			        </u-col>
					
			        
			    </u-row>
			

			
			<!-- <view class="fui-card__content fui-padding">这是一个基础卡片的示例，此处为自定义内容区域，自行控制内容样式。</view> -->
		
		</fui-card>
		
	</view>
</template>

<script>
	export default {
		name:"expert_display_card",
		data() {
			return {
				defaultPicPath: '/static//logo.png'
			};
		},
		methods: {
			expertDetail() {
				console.log('expert-card show')
				this.$emit('expertDetail', this.id)
			}

		},
		props:['id', 'name','title','institution','mail','logoPath']
	}
</script>

<style>
	.expertTitle {
		font-weight: 600;
		margin-left: 10px;
		margin-top: 5px;
		margin-bottom: 5px;
		width: 70px;
	}
/* 	.title-tag {
	
		max-width: 150px; 
		display: inline-block;
		
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	} */
	
	
</style>