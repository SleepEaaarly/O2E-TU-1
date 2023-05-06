<template>
	<view class="container">
		<view class="tui-status-bar"></view>
		<view v-if="userInfo.type=='0'" class="tui-page-title">专家认证</view>
		<view v-else-if="userInfo.type=='4'" class="tui-page-title">专家信息编辑</view>
		<view class="tui-form">
			<view class="tui-view-input">
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="people" color="#6d7a87" :size="40"></tui-icon>
						<input :require="true" :value="name" placeholder="请输入真实姓名(必填)" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputName" />
						<view class="tui-icon-close" v-show="name" @tap="clearInput(1)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="card" color="#6d7a87" :size="40"></tui-icon>
						<input :require="true" :value="ID_num" placeholder="请输入身份证(必填)" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputID_num" />
						<view class="tui-icon-close" v-show="ID_num" @tap="clearInput(2)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="mobile" color="#6d7a87" :size="40"></tui-icon>
						<input :require="true" :value="phone" placeholder="请输入电话号码(必填)" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputPhone" />
						<view class="tui-icon-close" v-show="phone" @tap="clearInput(3)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false">
					<view>
						<view class="thorui-input-title" :require="true">擅长领域(至少选择一项)</view>
						<checkbox-group @change="getSelectedInfo">
							<label v-for="(item,index) in checkboxItems" :key="index">
									<view class="thorui-align__center">
										<checkbox :checked="item.checked" :value="item.value" color="#f8683c" borderColor="#999">
										</checkbox>
										<text class="tui-text">{{item.name}}</text>
									</view>
							</label>
						</checkbox-group>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="strategy" color="#6d7a87" :size="40"></tui-icon>
						<input :value="paper" placeholder="请输入一篇发表的论文全称(知兔可查)" 
								placeholder-class="tui-phcolor" type="text" maxlength="200" @input="inputPaper" />
						<view class="tui-icon-close" v-show="paper" @tap="clearInput(4)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="strategy" color="#6d7a87" :size="40"></tui-icon>
						<input :value="patent" placeholder="请输入一篇发表的专刊全称(知兔可查)" 
								placeholder-class="tui-phcolor" type="text" maxlength="200" @input="inputPatent" />
						<view class="tui-icon-close" v-show="patent" @tap="clearInput(5)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell>
					<view class="thorui-input-title">(论文和专刊至少选择一项填写)</view>
					</tui-list-cell>
				<tui-list-cell :hover="false" :lineLeft="false" backgroundColor="transparent">
					<view class="tui-cell-input">
						<tui-icon name="home" color="#6d7a87" :size="40"></tui-icon>
						<input :value="organization" placeholder="请输入工作单位(必填)" placeholder-class="tui-phcolor" type="text" maxlength="36" @input="inputOrganization" />
						<view class="tui-icon-close" v-show="organization" @tap="clearInput(6)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				
				
				<tui-list-cell :hover="false">
					<view>
						<view class="thorui-input-title">个人简介</view>
						<textarea :require="true" placeholder="请输入个人简介(必填)" placeholder-class="thorui-phcolor" maxlength="512" @input="inputScholar_Profile" :value="scholar_profile"></textarea>
						<view class="tui-icon-close" v-show="scholar_profile" @tap="clearInput(7)">
							<tui-icon name="close-fill" :size="32" color="#bfbfbf"></tui-icon>
						</view>
					</view>
				</tui-list-cell>
				<tui-list-cell :hover="false">
					<view>
						<view class="thorui-input-title">身份证照片(必填)</view>
						<uploadID @getIDpic="getIDPath"></uploadID>
					</view>
				</tui-list-cell>

			</view>
			
			<checkbox-group @change="checkboxChange">
				<label class="tui-cell-text">
					<checkbox :checked="accepted" style="transform:scale(0.75)" />申请认证代表同意
					<view class="tui-color-primary" hover-class="tui-opcity" :hover-stay-time="150" @tap="protocol">用户服务协议、隐私政策</view>
				</label>
			</checkbox-group>
			
			<view v-if="userInfo.type=='0'" class="tui-btn-box">
				<tui-button @tap="certificate" :disabledGray="true" :disabled="disabled" :shadow="true" shape="circle">申请认证</tui-button>
			</view>
			<view v-else-if="userInfo.type=='4'" class="tui-btn-box">
				<tui-button @tap="certificate" :disabledGray="true" :disabled="disabled" :shadow="true" shape="circle">提交审核</tui-button>
			</view>
		</view>
	</view>
	
</template>

<script>
	import { enterprise_certificate } from '../../api/certificate.js'
	import {
		mapMutations,
		mapState
	} from 'vuex'
	import uploadLicense from '../../components/uploadImages/uploadLicense.vue'
	import uploadID from '../../components/uploadImages/uploadID.vue'
	import form from '../../components/thorui/tui-validation/tui-validation.js'
	export default {
		components:{
			uploadLicense,
			uploadID
		},
		data() {
			return {
				userID: '',
				name: '',
				ID_num: '',
				phone: '',
				paper: '',
				patent: '',
				organization: '',
				field: '',
				scholar_ID: '',
				scholar_profile: '',
				selectedItems: [],
				checkboxItems:[{
					name: '信息技术',
					value: '0',
					checked: false,
				},
				{
					name: '装备制造',
					value: '1',
					checked: false,
				},
				{
					name: '新材料',
					value: '2',
					checked: false,
				},
				{
					name: '新能源',
					value: '3',
					checked: false,
				},
				{
					name: '节能环保',
					value: '4',
					checked: false,
				},
				{
					name: '生物医药',
					value: '5',
					checked: false,
				},
				{
					name: '科学创意',
					value: '6',
					checked: false,
				},
				{
					name: '检测检验',
					value: '7',
					checked: false,
				},
				{
					name: '其他',
					value: '8',
					checked: false,
				},
				],
				accepted: false,	//框框是否选中
			}
		},
		computed:{
			disabled: function() {
				let bool = true
				if (this.userID &&this.name && (this.paper || this.patent) &&
					this.organization && this.ID_num &&
					this.scholar_ID && this.scholar_profile &&
					this.accepted) {
					bool = false
				}
				return bool
			},
			...mapState(['userInfo'])
		},
		onLoad(data) {
			//this.userID = data.uid;
			
			this.userID = this.userInfo.id
			if(this.userInfo.expert_name){
				this.name = this.userInfo.expert_name
				this.organization = this.userInfo.expert_organization
				this.field = this.userInfo.expert_field
				this.scholar_profile = this.userInfo.expert_scholarprofile
				this.phone = this.userInfo.expert_phone
			}
			console.log('onLoad in certification '+ this.userID)
		},
		methods: {
			//验证手机号码
			back() {
				uni.navigateBack()
			},
			inputName(e) {
				this.name = e.detail.value
			},
			inputPaper(e) {
				this.paper = e.detail.value
			},
			inputPatent(e) {
				this.patent = e.detail.value
			},
			inputOrganization(e) {
				this.organization = e.detail.value
			},
			inputField(e) {
				this.field = e.detail.value
			},
			inputID_num(e) {
				this.ID_num = e.detail.value
			},
			inputScholar_ID(e) {
				this.scholar_ID = e.detail.value
			},
			inputScholar_Profile(e) {
				this.scholar_profile = e.detail.value
			},
			inputPhone(e) {
				this.phone = e.detail.value
			},
			clearInput(type) {
				if (type === 1) {
					this.name = ''
				} else if(type === 2) {
					this.ID_num = ''
				}else if (type === 3) {
					this.phone = ''
				} else if (type === 4) {
					this.paper = ''
				} else if (type === 5) {
					this.patent = ''
				} else if (type === 6) {
					this.organization = ''
				} else if (type === 7) {
					this.scholar_profile = ''
				}
			},
			protocol() {
				this.tui.href('/pages/doc/protocol/protocol')
			},
			getIDPath(val) {
				if (val.length > 0) {
					this.scholar_ID = val[0]
				} else {
					this.scholar_ID = ''
				}
				console.log('IDPath!')
				console.log(this.scholar_ID)
			},
			getSelectedInfo(e) {
				console.log(e.detail.value)
				this.selectedItems = e.detail.value
			},
			checkID() {
				if (this.scholar_ID.length != 18) {
					return true
				} else {
					return false
				}
			},
			getFieldString() {
				let string = []
				let str = ''
				let first = false
				for (let i = 0; i < this.checkboxItems.length; i++) {
					string.push('0')
				}
				console.log('string is ' + string)
				for (let i = 0; i < this.selectedItems.length; i++) {
					console.log('seledted ' + this.selectedItems[i])
					string[this.selectedItems[i]] = '1'
				}
				console.log('string is ' + string)
				
				for (let i = 0; i < string.length; i++) {
					if(string[i]=='1'){
						if(first){
							str = str + ' '
						}else{
							first = true
						}
						str = str + this.checkboxItems[i].name
					}
				}
				this.field = str
			},
			checkFiledString() {
				if (this.selectedItems.length === 0) {
					return true
				}
				return false
			},
			validate() {
				let rules = [{
					name: 'phone',
					rule: ['isMobile'],
					msg: ['请输入正确手机号']
				},
				{	
					name: 'scholar_ID',
					rule: ['required'],
					msg: ['请输入身份证号'],
					validator: [{
						msg: '请输入正确身份号码',
						method: this.checkID
					}]
				},
				{
					name: 'field',
					rule: ['required'],
					msg: ['请至少选择一个领域'],
					validator: [{
						msg: '请至少选择一个领域',
						method: this.checkFieldString
					}]
				}
				]
				let formData = {
					userID: this.userID,
					name: this.name,
					paper: this.paper,
					patent: this.patent,
					organization: this.organization,
					field: this.field,
					ID_num: this.ID_num,
					scholar_ID: this.scholar_ID,
					scholar_profile: this.scholar_profile,
					phone: this.phone,
				}
				let checkRes = form.validation(formData, rules)
				return checkRes
			},
			certificate() {
				console.log('认证开始！')
				this.getFieldString()
				console.log(this.field)
				let checkRes = this.validate()
				if (checkRes) {
					uni.showToast({
						title: checkRes,
						icon: 'none'
					})
					return
				} 
				uni.uploadFile({
					// url: 'http://127.0.0.1:8000/api/expert/setinfo',
					url: 'http://116.63.14.146:8000/api/expert/setinfo',
					// url: 'http://116.63.14.146:8000/api/expert/setinfo',
				// url: 'http://122.9.14.73:8000/api/expert/setinfo',
					files: [{
						uri: this.scholar_ID,
						name: 'scholar_ID'
					}],
					formData:{
						'id': this.userID,
						'name': this.name,
						'ID_num': this.ID_num,
						'phone': this.phone,
						'paper': this.paper,
						'patent': this.patent,
						'organization': this.organization,
						'field': this.field,
						'scholar_profile': this.scholar_profile
					},
					success: uploadFileRes => {
						uni.showToast({
							success: '',
							title: '申请成功'
						})
						// uni.$emit('certificateSuccess')
						setTimeout(function () {
							uni.navigateBack({
								delta: 1
							})
						}, 1000)
						console.log(uploadFileRes.data)
						console.log('认证申请已发送')
					},
					fail: err => {
						console.log(err)
					}
				})
				return
			},
			checkboxChange(e){
				this.accepted = !this.accepted
				console.log('改变！')
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
				margin-top: 25rpx;
				padding: 0rpx $uni-spacing-row-lg;
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
				margin-top: 30rpx;
			}
		}
	}
</style>
