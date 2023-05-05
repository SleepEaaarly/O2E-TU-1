<template>
  <view class="mask" :class= "mask == 'true' || mask == true ? 'mask-show' : ''" @click="Mclose" v-if="show" @touchmove.stop.prevent="preventTouchMove">
		<!-- 加载动画开始 -->    <!-- loading1~loading30挑选任意一个替换下方html 且替换对应css -->
		<!-- <view class="container">
		  <view class="popsicle">
			<view class="colors"></view>
		  </view>
		  <view class="stick"></view>
		  <view class="shadow"></view>
		</view> -->
		
		<view class="loader">
		  <view class="block-1"></view>
		  <view class="block-2"></view>
		  <view class="block-3"></view>
		  <view class="block-4"></view>
		  <view class="block-5"></view>
		  <view class="block-6"></view>
		  <view class="block-7"></view>
		  <view class="block-8"></view>
		  <view class="block-9"></view>
		  <view class="block-10"></view>
		  <view class="block-11"></view>
		  <view class="block-12"></view>
		  <view class="block-13"></view>
		  <view class="block-14"></view>
		  <view class="block-15"></view>
		  <view class="block-16"></view>
		</view>
		
		<!-- 加载动画结束 -->
		<view class="title">{{text}}</view>
  </view>
  <!-- 遮罩层-->
</template>

<script scoped="true">
export default {
  name: 'w-loading',
	props:{
		text: String,
		mask: Boolean | String,
		click: Boolean | String,
	},
  data() {
    return { show: false }
  },
	methods:{
		preventTouchMove(){
			console.log('stop user scroll it!')
			return
		},
		Mclose(){
			if(this.click == 'false' || this.click == false){
				this.show = false
			}
		},
		open(){
			this.show = true
    },
    close(){
      this.show = false
    }
	}
}
</script>

<style>
.mask {
  /* pointer-events: none; */
  position: fixed;
  z-index: 99999;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
	flex-direction:column;
  justify-content: center;
  align-items: center;
	flex-wrap: wrap;
}
.mask.mask-show{
	background: rgba(7, 17, 27, .3);
}
.title{
	color: #fff;
	font-size: 28upx;
}





/* loading加载动画的css */
.container {
  height: 280upx;
  width: 200upx;
}

.popsicle {
  height: 180upx;
  width: 120upx;
  border-radius: 55upx 55upx 10upx 10upx;
  position: relative;
  display: block;
  margin: 0 auto;
  overflow: hidden;
  -webkit-animation: float 2s ease-in infinite alternate;
  animation: float 2s ease-in infinite alternate;
}
.popsicle:before {
  content: "";
  height: 120%;
  width: 140%;
  position: absolute;
  left: -20%;
  top: -10%;
  background-image: -webkit-linear-gradient(
    bottom,
    #f63999 25%,
    #30dcf6 25%,
    #30dcf6 50%,
    #f2d200 50%,
    #f2d200 75%,
    #70ca5c 75%
  );
  background-image: linear-gradient(
    0deg,
    #f63999 25%,
    #30dcf6 25%,
    #30dcf6 50%,
    #f2d200 50%,
    #f2d200 75%,
    #70ca5c 75%
  );
  display: block;
  -webkit-transform: rotate(-20deg);
  transform: rotate(-20deg);
  -webkit-animation: magic 2.5s linear infinite;
  animation: magic 2.5s linear infinite;
}
@-webkit-keyframes magic {
  to {
    background-position: 0 210upx;
  }
}
@keyframes magic {
  to {
    background-position: 0 210upx;
  }
}
.popsicle:after {
  content: "";
  position: absolute;
  left: 10upx;
  bottom: 10upx;
  width: 13upx;
  height: 120upx;
  border-radius: 50upx;
  background: rgba(255, 255, 255, 0.35);
}

.stick {
  width: 38upx;
  height: 45upx;
  background: #e09c5f;
  border-radius: 0 0 12upx 12upx;
  display: block;
  margin: 0 auto;
  -webkit-animation: float 2s ease-in infinite alternate;
  animation: float 2s ease-in infinite alternate;
}
.stick:after {
  display: block;
  content: "";
  width: 100%;
  height: 14upx;
  background: rgba(0, 0, 0, 0.4);
}

@-webkit-keyframes float {
  to {
    -webkit-transform: translateY(20upx);
    transform: translateY(20upx);
  }
}

@keyframes float {
  to {
    -webkit-transform: translateY(20upx);
    transform: translateY(20upx);
  }
}
.shadow {
  width: 124upx;
  height: 35upx;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 60upx / 22upx;
  display: block;
  margin: 0 auto;
  -webkit-transform: scaleY(0.7) translateY(30upx);
  transform: scaleY(0.7) translateY(30upx);
  -webkit-animation: shad 2s ease-in infinite alternate;
  animation: shad 2s ease-in infinite alternate;
}

@-webkit-keyframes shad {
  to {
    -webkit-transform: scaleX(0.9) scaleY(0.7) translateY(30upx);
    transform: scaleX(0.9) scaleY(0.7) translateY(30upx);
  }
}

@keyframes shad {
  to {
    -webkit-transform: scaleX(0.9) scaleY(0.7) translateY(30upx);
    transform: scaleX(0.9) scaleY(0.7) translateY(30upx);
  }
}

/* 自定义动画loading */
.loader {
  height: 60upx;
  transform: translateX(-0%) translateY(-0%);
  width: 60upx;
}
.loader view {
  animation: load 4s ease-in-out infinite;
  background: #fff;
  display: block;
  height: 12upx;
  opacity: 0;
  position: absolute;
  width: 12upx;
}
.loader view.block-1 {
  animation-delay: 0.92s;
  left: 0upx;
  top: 0upx;
}
.loader view.block-2 {
  animation-delay: 0.84s;
  left: 16upx;
  top: 0upx;
}
.loader view.block-3 {
  animation-delay: 0.76s;
  left: 32upx;
  top: 0upx;
}
.loader view.block-4 {
  animation-delay: 0.68s;
  left: 48upx;
  top: 0upx;
}
.loader view.block-5 {
  animation-delay: 0.6s;
  left: 0upx;
  top: 16upx;
}
.loader view.block-6 {
  animation-delay: 0.52s;
  left: 16upx;
  top: 16upx;
}
.loader view.block-7 {
  animation-delay: 0.44s;
  left: 32upx;
  top: 16upx;
}
.loader view.block-8 {
  animation-delay: 0.36s;
  left: 48upx;
  top: 16upx;
}
.loader view.block-9 {
  animation-delay: 0.28s;
  left: 0upx;
  top: 32upx;
}
.loader view.block-10 {
  animation-delay: 0.2s;
  left: 16upx;
  top: 32upx;
}
.loader view.block-11 {
  animation-delay: 0.12s;
  left: 32upx;
  top: 32upx;
}
.loader view.block-12 {
  animation-delay: 0.04s;
  left: 48upx;
  top: 32upx;
}
.loader view.block-13 {
  animation-delay: -0.04s;
  left: 0upx;
  top: 48upx;
}
.loader view.block-14 {
  animation-delay: -0.12s;
  left: 16upx;
  top: 48upx;
}
.loader view.block-15 {
  animation-delay: -0.2s;
  left: 32upx;
  top: 48upx;
}
.loader view.block-16 {
  animation-delay: -0.28s;
  left: 48upx;
  top: 48upx;
}

@keyframes load {
  0% {
    opacity: 0;
    transform: translateY(-100upx);
  }
  15% {
    opacity: 0;
    transform: translateY(-100upx);
  }
  30% {
    opacity: 1;
    transform: translateY(0);
  }
  70% {
    opacity: 1;
    transform: translateY(0);
  }
  85% {
    opacity: 0;
    transform: translateY(100upx);
  }
  100% {
    opacity: 0;
    transform: translateY(100upx);
  }
}
</style>
