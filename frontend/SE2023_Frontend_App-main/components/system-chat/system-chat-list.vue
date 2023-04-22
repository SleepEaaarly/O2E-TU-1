<template>
    <view class="system-chat-item animated fadeIn fast">
        <view v-if="item.gstime" class="system-chat-time u-f-ajc">{{item.gstime}}</view>
        <!-- 转换提示信息 -->
        <view v-if="item.type == 'switch_info'" class="system-chat-time u-f-ajc">您已转换为{{item.message === 'AI' ? "AI" : "人工"}}服务</view>
        <view v-if="item.type !== 'switch_info'" class="system-chat-list u-f" :class="{'system-chat-me': item.isme}">
            <!-- 显示管理员/AI头像但不跳转 -->
            <image v-if="!item.isme" :src="item.userpic" mode="widthFix" lazy-load></image>
            <!-- 消息 -->
            <view class="system-chat-list-body">
                
                <!-- 文字 -->
                <text v-if="item.type == 'text'">{{item.message}}</text>
                <!-- 图像 -->
                <image v-if="item.type == 'pic'" :src="item.message" mode="widthFix" lazy-load></image>
                <!-- 卡片 -->
                <!-- <system-chat-card v-if="item.type == 'card'" :src="item.message" class="system-chat-card"></system-chat-card>  -->
                <system-chat-card v-if="item.type == 'card'" :cardInfo="item.cardInfo" class="system-chat-card"></system-chat-card> 
                <!-- 报告 -->
                <require_message_card v-if="item.type == 'report' && item.reportInfo.reportType == 'need'"
                
                >

                </require_message_card>
                
                <work_message_card v-if="item.type == 'report' && item.reportInfo.reportType == 'work'"
                
                >

                </work_message_card>

                <order_message_card v-if="item.type == 'report' && item.reportInfo.reportType == 'order'"
                
                >
                
                </order_message_card>
            </view>
            <!-- 点击头像跳转到自己主页 -->
        </view>
    </view>
</template>

<script>
    import systemChatCard from 'components/system-chat/system-chat-card'
    import require_message_card from '../../components/require_message_card.vue'
    import work_message_card from '../../components/work_message_card.vue'
    import order_message_card from '../order_message_card.vue'
    export default {
        components: {
            systemChatCard,
            require_message_card,
            work_message_card,
            order_message_card
        },
        props: {
            item: Object,
            index: Number,
            isHuman: Boolean,
        },
        mounted() {
            uni.$on('system-chat-list-on-show', function() {
                console.log("system-chat-list-on-show")
                uni.$emit('system-chat-card-on-show')
            })
        },
        methods: {
            navUserInfo() {
                console.log(this.item)
                this.$emit('goToUserInfo', this.item.uid)
            },
            gotoWorkReportDetail() {
                uni.navigateTo({url: '../../pages/work_report/work_report?reportId=' + this.item.reportInfo.reportId})
            },
            gotoRequireReportDetail() {
                uni.navigateTo({url: '../../pages/require_report/require_report?reportId=' + this.item.reportInfo.reportId})
            },
            gotoOrderReportDetail() {
                uni.navigateTo({url: '../../pages/order_report/order_report?reportId=' + this.item.reportInfo.reportId})
            }
        },
    }

</script>

<style scoped>
.system-chat-list {
    padding: 20upx 0;
}

.system-chat-list>image {
    width: 80upx !important;
    height: 80upx !important;
    flex-shrink: 0;
    margin: 0 10upx;
}

.system-chat-list-body {
    position: relative;
    background: #f4f4f4;
    padding: 25upx;
    margin-left: 20upx;
    border-radius: 20upx;
    margin-right: 100upx;
}
.system-chat-list-body:after {
    position: absolute;
    left: -30upx;
    right: 0;
    top: 30upx;
    content: '';
	width: 0;
	height: 0;
	border: 16upx solid #F4F4F4;
	border-color: transparent #F4F4F4 transparent transparent;
}
.system-chat-me {
    justify-content: flex-end;
}
.system-chat-me .system-chat-list-body:after {
    left: auto;
	right: -30upx;
	border-color: transparent transparent transparent #F4F4F4;
}

.system-chat-list-body>image {
    max-width: 150upx;
	max-height: 200upx;
}

.system-chat-list-body>system-chat-card {
    padding: 0;
    max-width: 150upx;
	max-height: 200upx;
}

.system-chat-time {
    padding: 50upx 0;
	color: #a2a2a2;
	font-size: 24upx;
}
</style>