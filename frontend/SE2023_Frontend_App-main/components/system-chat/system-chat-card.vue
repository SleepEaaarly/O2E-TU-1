<template>
    <view  >
        <uni-row class="header">
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
        </uni-row>
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
    import uniCol from '@/components/uni-row/components/uni-col/uni-col.vue'
	import uniRow from '@/components/uni-row/components/uni-row/uni-row.vue'
    export default {
        components: {
            uniCol,
            uniRow
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
        onReady() {
            this.initdata()
        },
        methods: {
            async initdata() {
                try {
                    const res = uni.getSystemInfoSync()
                    let t = 200
                    this.style.contentH = res.windowHeight
                    this.style.contentW = res.windowWidth
                } catch(e) {}
            },
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
</style>