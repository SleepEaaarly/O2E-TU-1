<template>
    <view class="content">
        <image class="logo" :src="Imgs"></image>
        <view class="text-area">
            <button class="title" @click="pictureClick()">{{title}}</button>
        </view>
    </view>
</template>

<script>
    export default {
        data() {
            return {
                title: '调用相机',
                Imgs: '/static/logo.png'
            }
        },
        onLoad() {

        },
        methods: {
            // 调用手机相机
            pictureClick () {
                uni.chooseImage({
                    count: 1,
                    sizeType: ['original', 'compressed'],
                    sourceType: ['camera','album'], //这要注意，camera掉拍照，album是打开手机相册
                    success: (res)=> {
                        console.log(res);
                        const tempFilePaths = res.tempFilePaths;
                        this.Imgs = res.tempFilePaths[0]
                        // this.$forceUpdate();
                        // console.log(this.Imgs)
                    }
                });
            },
            upLoadPic() {
                uni.uploadFile({
                    url: 'https://www.cailanzi001.com/api/v1/qiniu/upload/img', //服务器地址
                    fileType:"image",//ZFB必填,不然报错
                    filePath: tempFilePaths[0],//这个就是我们上面拍照返回或者先中照片返回的数组
                    name: 'imgFile',
                    success: (uploadFileRes) => {
                        let imgData = JSON.parse(uploadFileRes.data)
                        console.log(imgData.data.imgUrl);
                        console.log(this);
                        this.imgDataUrl = imgData.data.imgUrl
                    }
                });
            },
            scanQRcode() {
                uni.scanCode({
                    onlyFromCamera: true,//只允许拍照，不允许本地相册
                    scanType:["qrCode"],//扫码类型 以为 二位 xxx
                    success:  (res)=> {
                        console.log('条码内容：' + res);
                    }
                });
            }
        }
    }
</script>

<style>
    .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .logo {
        height: 200rpx;
        width: 200rpx;
        margin-top: 200rpx;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 50rpx;
    }

    .text-area {
        display: flex;
        justify-content: center;
    }

    .title {
        font-size: 36rpx;
        color: #8f8f94;
    }
</style>
