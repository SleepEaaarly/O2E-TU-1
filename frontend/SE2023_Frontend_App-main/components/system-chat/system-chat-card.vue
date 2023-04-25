<template>
    <view  >
        <fui-card style="width: 400rpx; height: 120px; margin: 0 0 0 0;" @click.native="gotoCardDetail">
            <view style="margin-top:  20rpx; margin-bottom: 20rpx;">
                <u-row style="margin-left: 20rpx;">
                    {{cardInfo.title}}
                </u-row>
                <u-row>
                    <u-col span="8">
                        <text class="content">
                            {{cardInfo.info}}
                        </text>
                    </u-col>
                    <u-col span="4">
                        <!-- <image src="http://localhost:8080/static/img/need_contracted.b69b28cb.jpg" ></image> -->
                        <!-- <image class="logo" src="http://localhost:8080/static/img/need_contracted.b69b28cb.jpg"  -->
                        <image class="logo" :src="cardInfo.avatar" 
					style = "height: 55px;width: 55px;margin-left: 10px;margin-top: 15px;border-radius: 20px;">
                    </u-col>
                </u-row>
            </view>
        </fui-card>
        <!-- <uni-row class="header">
            <uni-col :span="9" class="image">
                <image :src="cardInfo.avatar" mode="widthFix" lazy-load class="image-image"></image>
            </uni-col>
            <uni-col :span="14" :offset="1" class="title-info">
                <uni-row class="need-title">
                    <text class="need-title">{{ cardInfo.title }}</text>
                </uni-row>
                <uni-row class="need-info">
                    <uni-row :span="14" class="need-info-item">
                        <uni-icons type="fire" size="18"></uni-icons>
                        <text class="need-info-text">{{ cardInfo.info }}</text>
                    </uni-row>
                </uni-row>
            </uni-col>
        </uni-row> -->
        <!-- <uni-row class="header">
            <uni-col>
                <text class="topic_cont_text">testtesttesttesttesttesttesttesttesttest
                    testtesttesttesttesttesttesttesttesttesttest</text>
            </uni-col>
        </uni-row>
        <uni-row>
            <uni-col :span="10">
                <text class="blogContent">testtesttesttesttesttesttesttesttest
                    testtesttesttesttesttesttesttetesttesttesttesttesttesttesttesttest
                    sttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest</text>
            </uni-col>
            <uni-col :span="8">
                
                <image src="../../static/bgimg/need_contracted.jpg" ></image>
            </uni-col>
        </uni-row> -->
    </view>
</template>

<script>
import fuiCard from "@/components/firstui/fui-card/fui-card.vue"
    import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
    export default {
        name: "system-chat-card",
        components: {
            uniCol,
            uniRow,
            fuiCard
        },
        props: {
            cardInfo: Object
        },
        data() {
            return {
                style: {
                    contentH: 0,
                    contentW: 0,
                }
            }
        },
        onLoad() {
            console.log("onReady")
            // this.initdata()

        },
        onShow() {
            console.log("onShow")
        },
        onReady(){
            console.log("onReady")
        },
        mounted() {
            uni.$on('system-chat-card-on-show', function() {
                console.log("system-chat-card-on-show")
                // this.cardInfo = {}
                // this.cardInfo.cardType = 'expert',
                // this.cardInfo.id = 24,
                // this.cardInfo.avatar = "http://localhost:8080/static/img/need_contracted.b69b28cb.jpg",
                // this.cardInfo.info = "测试长消息测试长消息测试长消息测试场消息"
                console.log(this.cardInfo)
                this.initdata()
            });

        },
        beforeDestroy() {
            uni.$off('system-chat-card-on-show')
        },
        methods: {
            async initdata() {
                console.log(1)
                try {
                    const res = uni.getSystemInfoSync()
                    let t = 200
                    this.style.contentH = res.windowHeight
                    this.style.contentW = res.windowWidth
                } catch(e) {}
                // debug init data
                // {  
                //     this.cardInfo.cardType = 'expert',
                //     this.cardInfo.id = 24,
                //     this.cardInfo.avatar = "http://localhost:8080/static/img/need_contracted.b69b28cb.jpg",
                //     this.cardInfo.info = "测试长消息测试长消息测试长消息测试场消息"
                // }
                console.log(this.cardInfo)
            },
            gotoCardDetail() {
                // {  
                //     this.cardInfo = {},
                //     this.cardInfo.title = "测试专家"
                //     this.cardInfo.cardType = 'technique',
                //     this.cardInfo.id = 6,
                //     this.cardInfo.avatar = "http://localhost:8080/static/img/need_contracted.b69b28cb.jpg",
                //     this.cardInfo.info = "测试长消息测试长消息测试长消息测试场消息"
                // }
                console.log(this.cardInfo)
                if (this.cardInfo.cardType === 'expert') {
                    uni.navigateTo({url: '../../pages/user-space/user-space?uid=' + this.cardInfo.id})
                } else if (this.cardInfo.cardType === 'enterprise') {
                    uni.navigateTo({url: '../../pages/user-space/user-space?uid=' + this.cardInfo.id})
                } else if (this.cardInfo.cardType === 'demand') {
                    uni.navigateTo({url: '../../pages/need-detail/detail?id=' + this.cardInfo.id})
                } else if (this.cardInfo.cardType === 'technique') {
                    uni.navigateTo({url: '../../pages/work_detail/work_detail?rid=' + this.cardInfo.id})
                }
            }
        },
    }

</script>

<style>
.header {
    margin: 0upx;
    background-color: white;
    border: solid #F5FFF0 2upx;
    height: 17%;
}
.image-image {
    padding-top: 5%;
    width:100%;
}
.card-style {
    max-width: 300upx;
	max-height: 200upx;
}
.need-title {
    font-size: 35upx;
    font-weight: bold;
    color: skyblue;
    overflow: hidden;
    width: 400rpx !important;
    /* overflow: unset; */
    overflow: hidden;
    /* word-break: break-all; */
    word-break: normal;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: horizontal;
    -webkit-line-clamp: 2;
    
}
.need-info-text {
    font-weight: 100;
    font-size: 20upx;
    overflow:hidden; 
    text-overflow:ellipsis; 
        
}
.need-info-text-detail {
    font-weight: 100;
    font-size: 20upx;
    color: blue;
    height: 10upx;
}

.topic_cont_text {
    overflow: hidden;
    word-break: break-all;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
}

.blogContent {
    font-size: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    color: gray;
    height: 60px;
    text-align: left;
    word-wrap: break-word;
    word-break: normal;
}

.info {
		font-size: 30rpx;
		font-weight: 600;
	}
	.title {
		font-size: 30rpx;
		font-weight: 600;
		text-overflow:ellipsis;
		overflow:hidden;
		white-space:nowrap;
		max-width: 300rpx;
	}
	.content {
		font-size: 20rpx;
		margin-left: 20rpx;
		color: #606266;
		text-overflow:ellipsis;
		overflow:hidden;
		white-space:nowrap;
	}
</style>