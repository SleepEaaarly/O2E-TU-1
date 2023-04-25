<template>
    <view class="system-chat-bottom u-f-ac animated fadeInDown fast" >
        <view v-if="!notAI" class="icon iconfont icon-kulian u-f-ajc" @click="humanAISwitch"></view>
        <view v-if="notAI" class="icon iconfont icon-smile u-f-ajc" @click="humanAISwitch"></view>
        <input type="text" 
         placeholder="请输入私信" 
         v-model="text" 
         confirm-type="search" 
         @confirm="submit"/>
        <view class="icon iconfont icon-fabu u-f-ajc" @click="submit"></view>
    </view>

</template>

<script>

    export default {
        props: [
            'notAI'
        ],
        mounted() {
        },
        data() {
            return {
                text: "",
            }
        },
        onReady() {
        },
        methods: {
            submit() {
                this.$emit('submit', this.text);
                this.text = "";
            },
            humanAISwitch() {
                this.notAI = !this.notAI
                this.$emit('isHuman', this.notAI)
            }
        },
    }
</script>

<style scoped>
@import "../../common/icon.css";
.system-chat-bottom{
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	height: 120upx;
	padding: 0 20upx;
	background: #FFFFFF;
	border-top: 1upx solid #EEEEEE;
}
.system-chat-bottom>input{
	flex: 1;
	margin-right: 20upx;
    margin-left: 20upx;
	padding: 10upx 20upx;
	border-radius: 10upx;
	background: #F7F7F7;
}
.sytem-chat-bottom>view{
	width: 80upx;
	font-size: 45upx;
}
</style>
