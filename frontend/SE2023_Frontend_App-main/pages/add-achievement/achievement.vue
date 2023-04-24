<template>
    <view class="container">
        <view class="tui-status-bar">
            <uni-card :is-shadow="false" is-full>
                <text class="uni-h6">成果描述</text>
            </uni-card>
        </view>
        <view class="achievement-form">
            <form @submit="submit" @reset="reset">
                <uni-section title="成果标题" subTitle="为您的成果总结一个标题" type="line" padding>
                    <uni-easyinput v-model="title" focus placeholder="请输入内容"></uni-easyinput>
                </uni-section>
                <uni-section title="摘要" subTitle="描述您的成果" type="line" padding>
                    <uni-easyinput type="textarea" v-model="description" placeholder="请输入内容"
                        ></uni-easyinput>
                </uni-section>
				<uni-section title="内容" subTitle="介绍成果的内容" type="line" padding>
				    <uni-easyinput type="textarea" v-model="content" placeholder="请输入内容"
				        ></uni-easyinput>
				</uni-section>
                <uni-section title="成果作者" subTitle="多个作者用英文逗号分隔" type="line" padding>
                    <uni-easyinput v-model="scholars" focus placeholder="请输入作者" ></uni-easyinput>
                </uni-section>
                <!-- <uni-section title="成果链接" subTitle="给出您的成果链接" type="line" padding>
                    <uni-easyinput v-model="achievement_url" focus placeholder="请输入链接" @input="inputachievement_url"></uni-easyinput>
                </uni-section> -->
                <uni-section title="成果发布日期" subTitle="请选择成果发布日期" type="line" padding>
                    <view class="date-set">
                        <uni-datetime-picker type="datetime" v-model="pyear" @change="changeLogStart" />
                    </view>
                </uni-section>
                <uni-section title="领域" subTitle="请为您的成果确定主要领域方向" type="line" padding>
                    <view class="uni-list">
                        <view class="uni-list-cell">
                            <view class="uni-list-cell-left">
                                当前选择
                            </view>
                            <view class="uni-list-cell-db">
                                <picker @change="inputField" :value="index" :range="field_items">
                                    <view class="uni-input">{{ field_items[index] }}</view>
                                </picker>
                            </view>
                        </view>
                    </view>
                </uni-section>
                <uni-section title="成果阶段" subTitle="请选择成果阶段" type="line" padding>
					<view class="uni-list">
						<radio-group @change="radioChange">
							<label class="uni-list-cell uni-list-cell-pd" v-for="(item, index) in achTypes"
								:key="item.value">
								<view class="type-evaluate">
									<radio :value="item.value" :checked="index === period" />
								</view>
								<view>{{ item.name }}</view>
							</label>
						</radio-group>
					</view>
				</uni-section>
                <uni-section title="成果示意图" subTitle="请选择图片展示成果" type="line" padding>
					<view>
						<uploadID @getIDpic="getWorkLogo"></uploadID>
					</view>
                </uni-section>
				<uni-section title="成果详情" subTitle="请选择附件" type="line" padding>
					<view class="add-btn">
					   <uploadWorkPic @getWorkPic="getWorkPic"></uploadWorkPic>
					</view>			
				</uni-section>


                <view class="uni-btn-v">
                    <button type="primary" form-type="submit">直接发布</button>
                    <!-- <button type="primary" @click="saveAchievement">保存</button> -->
                    <button type="default" form-type="reset">清除</button>
                </view>
            </form>
        </view>
    </view>
</template>
<script>
import {
    mapMutations,
    mapState
} from 'vuex'
import {
    addachievement,
    saveachievement
} from '@/api/add-achievement.js'
import uploadWorkPic from '../../components/uploadImages/uploadWorkPic.vue'
import uploadID from '../../components/uploadImages/uploadID.vue'
import uniCard from '@/components/uni_easyinput/uni-card/components/uni-card/uni-card.vue'
import uniEasyinput from '@/components/uni_easyinput/uni-easyinput/components/uni-easyinput/uni-easyinput.vue'
import uniSection from '@/components/uni-section/uni-section.vue'
import uniDatetimePicker from '@/components/uni_datetime_picker/uni-datetime-picker/components/uni-datetime-picker/uni-datetime-picker.vue'
export default {
    components: {
        uniCard,
        uniEasyinput,
        uniSection,
        uniDatetimePicker,
        uploadWorkPic,
        uploadID
    },
    data() {
        return {
			id: '',
            title: '',
            description: '',
			content: '',
            money: '',
            start_time: '',
            end_time: '',
            key_word: '',
            field: 0,
            address: '',
            state: 0,
            type: '',
            predict: 0,
            real: 0,
            index: 0,
			achievement_url: '',
			scholars: '',
			pyear: '',
			isEI: false,
			isSCI: false,
			cites: '',
			paperKind: '',
            achievementFile: null,
            period: '',
            picture: '',
			multipic: [],
			title_max_length: 30,
			abstract_max_length: 300,
			content_max_length: 1000,
			author_max_length: 30,
			pics_max_num: 9,
            field_items: [
                '信息技术', '装备制造', '新材料', '新能源', '节能环保', '生物医药', '科学创意', '检验检测', '其他'
            ],
            achTypes: [
                {
                    value: '0',
                    name: '实验室'
                },
                {
                    value: '1',
                    name: '样品'
                },
                {
                    value: '2',
                    name: '中试'
                },
                {
                    value: '3',
                    name: '产业化'
                }
            ]
			// paperType: [
   //              {
   //                  value: '0',
   //                  name: 'EI'
   //              },
   //              {
   //                  value: '1',
   //                  name: 'SCI'
   //              },
   //              {
   //                  value: '2',
   //                  name: '均不是'
   //              }				
			// ]
        }
    },
    watch: {
        datetimesingle(newval) {
            console.log('单选:', this.datetimesingle)
        },
        range(newval) {
            console.log('范围选:', this.range)
        },
        datetimerange(newval) {
            console.log('范围选:', this.datetimerange)
        }
    },
    mounted() {
        setTimeout(() => {
            this.datetimesingle = Date.now() - 2 * 24 * 3600 * 1000
            this.single = '2021-2-12'
            // this.range = ['2021-03-1', '2021-4-28']
            this.datetimerange = ['2021-07-08 0:01:10', '2021-08-08 23:59:59']
            // this.start = '2021-07-10'
            // this.end = '2021-07-20'
        }, 3000)
    },
    computed: { ...mapState(['userInfo']) },
    onLoad(data) {
        //this.userID = data.uid;

        this.id = this.userInfo.id
        console.log('onLoad in certification ' + this.id)
    },
    methods: {
		// 打开文件选择器
		// openFile(){
		// 	uni.chooseFile({
		// 		count: 1, //默认100
  //               // extension: ['.zip', '.doc', '.xls', '.pdf', 'docx', '.rar', '.7z', '.jpg', '.png', '.jpeg'],
  //               extension: ['.pdf'],
		// 		success: (res) =>{
		// 			console.log(res);
		// 			if(res.tempFiles[0].size / 1024 / 1024 > 20){
		// 				this.$refs.uToast.show({
		// 					title: '附件大小不能超过20M',
		// 					type: 'warning',
		// 				})
		// 				return;
  //                   }
  //                   this.achievementFile = res.tempFilePaths[0]
		// 		}
		// 	});
		// },
        getWorkLogo(val) {
            if (val.length > 0) {
                this.picture = val[0]
            } else {
                this.picture = ''
            }
            console.log('result picture!')
            console.log(this.picture)
        },
		getWorkPic(val){
			if (val.length > 0) {
			    this.multipic = val
			} else {
			    this.multipic = []
			}
			console.log('result multipic!')
			console.log(this.multipic)
		},
        back() {
            uni.navigateBack()
        },
        inputTitle(e) {
            this.title = e.detail.value
        },
        inputDescription(e) {
            this.description = e.detail.value
        },
		inputContent(e) {
		    this.content = e.detail.value
		},
		inputScholars(e){
			this.scholars = e.detail.value
		},
		inputachievement_url(e){
			this.achievement_url = e.detail.value
		},
        inputMoney(e) {
            this.money = e.detail.value
        },
        inputPicture(e){
            this.picture = e.detail.value
        },
        show: function (e) {
            this.$refs.start_time.show()
        },
        changeLogStart(e) {
            console.log('----changeStartTime事件:', e)
        },
        changeLogEnd(e) {
            console.log('----changeEndTime事件:', e)
        },
        inputKeyword(e) {
            this.key_word = e.detail
        },
        inputField(e) {
            this.index = e.detail.value
            
            this.field = this.field_items[this.index]
			console.log(this.field)
        },
        inputRegisterCapital(e) {
            this.register_capital = e.detail.value
        },
        inputAddress(e) {
            this.address = e.detail.value
        },
		inputCite(e){
			this.cites = e.detail-0
		},
        inputPredict(e) {
            this.predict = e.detail.value
        },
        radioChange: function (evt) {
            for (let i = 0; i < this.achTypes.length; i++) {
                if (this.achTypes[i].value === evt.detail.value) {
                    console.log(this.achTypes[i])
                    this.period = this.achTypes[i].name
                    break
                }
            }
        },
		// kindChange: function (evt) {
		//     for (let i = 0; i < this.paperType.length; i++) {
		//         if (this.paperType[i].value === evt.detail.value) {
		//             this.paperKind = i
		// 			if (0 == i - 0){
		// 				this.isSCI = true
		// 				this.isEI = false
		// 			} else if (1 == i - 0){
		// 				this.isEI = true
		// 				this.isSCI = false
		// 			} else {
		// 				this.isSCI = false
		// 				this.isEI = false
		// 			}
		//             break
		//         }
		//     }
		// },
        validate: function (data) {
            let validate_answer = true
            if (data.title === '' || data.title.length > this.title_max_length) {
				if(data.title === ''){
					this.$http.toast('请输入成果标题！')
				}else{
					this.$http.toast('成果标题请勿超过' + this.title_max_length +'字！')
				}                
                validate_answer = false
            } else if (data.abstract === '' || data.abstract.length > this.abstract_max_length) {
                if(data.abstract === ''){
					this.$http.toast('请详细描述您的成果！')
				}else{
					this.$http.toast('成果摘要请勿超过' + this.abstract_max_length +'字！')
				}
                validate_answer = false
            } else if (data.content === '' || data.content.length > this.content_max_length) {
                if(data.content === ''){
					this.$http.toast('请输入成果内容！')
				}else{
					this.$http.toast('成果内容请勿超过' + this.content_max_length +'字！')
				}
                validate_answer = false
            } else if (data.scholars === '' || data.scholars.length > this.author_max_length) {
                if(data.scholars === ''){
					this.$http.toast('请输入成果作者！')
				}else{
					this.$http.toast('成果作者长度请勿超过' + this.author_max_length +'字！')
				}
                validate_answer = false
            } else if (data.pyear === '') {
                this.$http.toast('请选择发布时间！')
                validate_answer = false
                // } else if (!isKeyword(data.key_word)) {
                // 	this.$http.toast("请按照格式输入！")
                // 	validate_answer = false
            } else if (data.period === '') {
                this.$http.toast('请选择成果阶段！')
                validate_answer = false
            } else if (data.multipic != null && data.multipic.length > this.pics_max_num) {
				this.$http.toast('附件图片请勿超过' + this.pics_max_num + '张！')
				validate_answer = false
                // PDF为可选项   
            } else if (data.picture == null) {
                this.$http.toast('请选择成果图片！')
                validate_answer = false
                // Pic为可选项
            }
            // } else if (data.predict === '0' || data.predict === 0) {
            // 	this.$http.toast('预估人数必须大于0！')
            // 	validate_answer = false
            // }
            return validate_answer
        },
        isKeyword: function (key_word) {
            let mPattern = /^([\u4e00-\u9fa5])+(\s[\u4e00-\u9fa5])*/
            return mPattern.test(key_word)
        },
        async submit() {
				let data = {
					'title': this.title,
					'abstract': this.description,
					'start_time': this.start_time,
					'end_time': this.end_time,
					'period': this.period,
					'field': this.field,
					'address': this.address,
					'state': this.state,
					'type': this.type,
					'achievement_url': this.achievement_url,
					'scholars': this.scholars,
					'pyear': this.pyear,
					'content': this.content,
					'id': this.id,
					'picture': this.picture,
					'multipic': this.multipic
				}
				console.log(data)
				// let validate_answer = this.validate(data)
				// console.log(data.type)
				// if (validate_answer) {
				// 	console.log("validate_success!")
				// } else{
				// 	console.log("fail to validate!")
				// 	return
				// }
				console.log("start_submit")
				console.log(this.id)
				let filelist = []
				for(let i=0;i<this.multipic.length;i++){
					filelist.push({name:'multipic', uri:this.multipic[i]})
				}
				filelist.push({name:'picture', uri:this.picture})
				uni.uploadFile({
					url: 'http://127.0.0.1:8000/api/result/add',
					// url: 'http://116.63.14.146:1234/api/result/add',
				// url: 'http://122.9.14.73:8000/api/enterprise/setinfo',
					files: filelist,
					
					formData:{
						'title': this.title,
						'abstract': this.description,
						'start_time': this.start_time,
						'end_time': this.end_time,
						'period': this.period,
						'field': this.field,
						'address': this.address,
						'state': this.state,
						'type': this.type,
						'achievement_url': this.achievement_url,
						'scholars': this.scholars,
						'pyear': this.pyear,
						'content': this.content,
						'id': this.id
					},
					success: uploadFileRes => {
						uni.showToast({
							success: '',
							title: '发布成功'
						})
						// uni.$emit('certificateSuccess')
						setTimeout(function () {
							uni.navigateBack({
								delta: 1
							})
						}, 1000)
						console.log(uploadFileRes.data)
						console.log('成果发布申请已发送')
					},
					fail: err => {
						uni.showToast({
							fail: '',
							title: '申请失败',
							duration: 1000
						}).then(
							this.$refs.popup.open()
						)
						console.log('发布失败')
					}
				})
        },
        reset: function (e) {
                this.title = '',
                this.description = '',
				this.content = '',
                this.money = '',
                this.start_time = '',
                this.end_time = '',
                this.key_word = '',
                this.field = 0,
                this.address = '',
                this.state = 0,
                this.type = '',
                this.index = 0,
				this.cites = '',
				this.scholars = '',
				this.pyear = '',
				this.achievement_url = '',
				this.isEI = false,
                this.isSCI = false,
                this.picture = null,
                this.achievementFile = null,
                this.period = ''
        },
        async saveAchievement() {
            let data = {
                'title': this.title,
                'abstract': this.description,
				'content': this.content,
                'start_time': this.start_time,
                'end_time': this.end_time,
                'period': this.period,
                'field': this.field,
                'address': this.address,
                'state': this.state,
                'type': this.type,
                'achievement_url': this.achievement_url,
                'scholars': this.scholars,
                'pyear': this.pyear,
                'content': this.content,
                'file': this.achievementFile,
                'picture': this.picture,
				'id': this.id
            }
            let validate_answer = this.validate(data)
            if (validate_answer) {
                let result = await saveachievement(data)
                if (result && result.code) {
                    this.$http.toast('成果保存失败！')
                } else {
                    this.$http.toast('成果保存成功！')
                    this.back()
                }
            }
        }
    }
}
</script>

<style lang="scss" scoped>
.container {
    .tui-page-title {
        width: 100%;
        font-size: 48rpx;
        font-weight: bold;
        color: $uni-text-color;
        line-height: 42rpx;
        padding: 110rpx 40rpx 40rpx 40rpx;
        box-sizing: border-box;
    }

    .tui-header {
        width: 100%;
        padding: 40rpx;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-sizing: border-box;
    }

    .tui-form {
        padding-top: 50rpx;

        .thorui-input-title {
            padding-right: 10rpx;
            font-size: 35rpx;
        }

        .tui-view-input {
            width: 100%;
            box-sizing: border-box;
            padding: 0 40rpx;

            .tui-cell-input {
                width: 100%;
                display: flex;
                align-items: center;
                padding-top: 48rpx;
                padding-bottom: $uni-spacing-col-base;

                input {
                    flex: 1;
                    padding-left: $uni-spacing-row-base;
                }

                .tui-icon-close {
                    margin-left: auto;
                }

                .tui-btn-send {
                    width: 156rpx;
                    text-align: right;
                    flex-shrink: 0;
                    font-size: $uni-font-size-base;
                    color: $uni-color-primary;
                }

                .tui-gray {
                    color: $uni-text-color-placeholder;
                }
            }
        }

        .tui-cell-text {
            width: 100%;
            padding: 40rpx $uni-spacing-row-lg;
            box-sizing: border-box;
            font-size: $uni-font-size-sm;
            color: $uni-text-color-grey;
            display: flex;
            align-items: center;

            .tui-color-primary {
                color: $uni-color-primary;
                padding-left: $uni-spacing-row-sm;
            }
        }

        .tui-btn-box {
            width: 100%;
            padding: 0 $uni-spacing-row-lg;
            box-sizing: border-box;
            margin-top: 80rpx;
        }
    }
}

.date-set {
    background-color: #fff;
    padding: 10px;
}

.type-evaluate {
    margin: 5upx;
}

button {
    margin: 20upx;
    height: 70upx;
    font-size: small;
}</style>
