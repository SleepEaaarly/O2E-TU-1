<template>
	<view>
		<fui-card :footer-line="false" style ="height: 100px;">
				 <u-row style="margin-bottom: 0%;">
				        <u-col span="3">
				            <image class="logo" :src="logoPath" 
							style = "max-height: 70px;max-width: 70px;margin-left: 10px;margin-top: 15px;border-radius: 20px;">
				        </u-col>
				        <u-col span="9">
							<u-row style="margin-top: 20px;">
								<u-col span="7">
									<u-row>
										<text class = "companyTitle">{{name}}</text>
									
									</u-row>
									
								</u-col>
								<u-col span="5">
									
								</u-col>
								
							</u-row>
						
							<u-row style="margin-top: 10px;margin-bottom: 0%;margin-left: 5px;">
								
								<u-tag :text="address" plain size="mini" type="error"> </u-tag>
								<u-tag :text = "area" plain size="mini" style="margin-left: 20px;"> </u-tag>
								
							</u-row>
							
				        </u-col>
						
				        
				    </u-row>
				
		
				
				<!-- <view class="fui-card__content fui-padding">这是一个基础卡片的示例，此处为自定义内容区域，自行控制内容样式。</view> -->
			
			</fui-card>
		
	</view>
</template>

<script>
	export default {
		name:"company_rep_display_card",
		data() {
			return {
				
			};
		},
		props:['name','address','area','logoPath']
	}
</script>

<style>
	.companyTitle {
			font-weight: 600;
			margin-left: 10px;
			margin-top: 5px;
			margin-bottom: 5px;
			
		}

</style>