<template>
	<view>
		<fui-card :footerLine = "false" style="width: 100px;height: 150px;">
			<u-row>
				<image class="logo" :src="logoPath" style = "height: 90px;width: 90px; margin-top: 5px; margin-left: 5px;border-radius: 30px;">
					
				</image>
			</u-row>
			<u-row style="margin-top: 5px;">
				<text style="font-size: 15px;margin:auto;font-weight: 600;">{{name}}</text>
				<u-tag v-if="type" :text="type" type="error" plain plainFill shape="circle" size = "mini"></u-tag>
			</u-row>
				
			<!-- <fui-button text="默认按钮"></fui-button> -->
			<u-button type="primary" text="查看" size = "mini" style = "width: 50px;height: 20px;"></u-button>

	
		</fui-card>
		
	</view>
</template>

<script>
	export default {
		name:"search_person_card",
		data() {
			return {
				
			};
		},
		props:['name','logoPath',"type"]
	}
</script>

<style>

</style>