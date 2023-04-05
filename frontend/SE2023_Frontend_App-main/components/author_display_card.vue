<template>
	<view>
		<fui-card :footer-line="false" style ="height: 100px;">
				 <u-row style="margin-bottom: 0%;">
				        <u-col span="3">
				            <image class="logo" :src="logoPath" 
							style = "height: 70px;width: 70px;margin-left: 10px;margin-top: 15px;border-radius: 20px;">
				        </u-col>
				        <u-col span="9">
							<u-row style="margin-top: 20px;">
								<u-col span="7">
									<u-row>
										<text class = "expertTitle">{{name}}</text>
									<u-tag :text="title" plain plainFill type="warning"  shape="circle" size = "mini" style="margin-left: 10px;"> </u-tag>
								
										
									</u-row>
									
								</u-col>
								<u-col span="5">
									
								</u-col>
								
							</u-row>
							<u-row style="margin-top: 10px;margin-bottom: 0%;margin-left: 5px;">
								
								<u-tag :text="institution" plain size="mini"> </u-tag>
								<text style="font-size: 10px;margin-left: 5px;
								text-overflow:ellipsis;
								overflow:hidden;
								white-space:nowrap;">
								
								{{mail}}</text>
							</u-row>
				        </u-col>
						
				        
				    </u-row>
				
		
				
				<!-- <view class="fui-card__content fui-padding">这是一个基础卡片的示例，此处为自定义内容区域，自行控制内容样式。</view> -->
			
			</fui-card>
			
		</view>
		
	</view>
</template>

<script>
	export default {
		name:"author_display",
		data() {
			return {
				
			};
		},
		props:['name','title','institution','mail','logoPath']
	}
</script>

<style>
.expertTitle {
		font-weight: 600;
		margin-left: 10px;
		margin-top: 5px;
		margin-bottom: 5px;
		width: auto;
	}
</style>