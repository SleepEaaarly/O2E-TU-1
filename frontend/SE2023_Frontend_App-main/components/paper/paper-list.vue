<template>
	<view class="paper-list u-f-ac animated fadeIn fast" @tap="opendetail(index)">
		<image :src="item.userpic" mode="widthFix" lazy-load></image>
		<view>
			<!-- 专家/企业标识 -->
			<view v-if="item.name != ''">
				<view v-if="this.item.type == 4" class="expert-name-style u-f-ac">
					<view>{{item.username}}</view>
					<view style="margin-left: 0.5em;" @click.stop="goToUserInfo(item)">@{{item.name}}</view>
					<view style="margin-left: auto;">{{item.time}}</view>
				</view>
				<view v-else-if="this.item.type != 5" class="enterprise-name-style u-f-ac">
					<view>{{item.username}}</view>
					<view style="margin-left: 0.5em;" @click.stop="goToUserInfo(item)">@{{item.name}}</view>
					<view style="margin-left: auto;">{{item.time}}</view>
				</view>
			</view>
			<!-- 普通用户无标识 -->
			<view v-else>
				<view class="u-f-ac">
					<view>{{item.username}}</view>
					<view style="margin-left: auto;">{{item.time}}</view>
				</view>
			</view>
			<view class="u-f-ac u-f-jsb"><text class="overflowText">{{item.message}}</text>
				<template v-if="item.noreadnum>0">
					<uni-badge :text="item.noreadnum" type="error"></uni-badge>
				</template>
			</view>
		</view>
	</view>
</template>

<script>
	import uniBadge from '../../components/uni-badge/uni-badge.vue'
	export default {
		components:{ uniBadge },
		props:{
			item:Object,
			index:Number
		},
		data() {
			return { color: this.item.type === 4 ? 'skyblue' : '#ff9f62' }
		},
		methods:{
			opendetail(index){
				this.$emit('readMsg', index)
				uni.navigateTo({ url: '../../pages/user-chat/user-chat?index='+index })
			},
			// 企业与专家 @+姓名 跳转
			goToUserInfo(item){
				uni.navigateTo({ url:'../../pages/user-space/user-space?uid=' + item.fid })
			},
		}
	}
</script>

<style scoped>
.paper-list{
	border-bottom: 1upx solid #EEEEEE;
	padding: 20upx 0;
	height: 110upx;
	width: 100%;
}
.overflowText{
	width: 50vw;
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
}
.paper-list>image{
	width: 100upx!important;
	height: 100upx!important;
	border-radius: 100%;
	margin-right: 20upx;
	flex-shrink: 0;
}
.paper-list>view{
	flex: 1;
}

/* 第一个元素-好友名 */
.paper-list>view>view>view>view:first-child{
	font-size: 37upx;
}

/* 第二个元素-@+企业名 */ 
.paper-list>view>view>view>view:nth-child(2){
	/* color: #ff9f62;	/* 颜色与企业微信相同 */ 
	/* 橘色颜色与企业微信相同 */
	/* color: this.item.type == 4 ? #00aaff : #ff9f62; */
}

/* 最后一个元素-右侧时间 */
.paper-list>view>view>view>view:last-child{
	color: #CBCBCB;
}

.paper-list>view>view:last-child{
	color: #999999;
}

/* 第二个元素-@+专家名 */
.expert-name-style>view:nth-child(2) {
	/* 橘色颜色与企业微信相同 */
	color: #ff9f62;
}

/* 第二个元素-@+企业名 */
.enterprise-name-style>view:nth-child(2) {
	color: #00aaff;
}

</style>
