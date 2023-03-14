<style lang="less">
@import "./login.less";
</style>
<template>
  <div class="login">
    <div class="login-con" >
      <img src='../../assets/images/d.png' />
      <Card icon="log-in"
            :bordered="false"
            dis-hover>
        <!-- <p class='title' slot~~='title'>欢迎登录</p> -->
        <!-- 1为登录表单，2为注册表单 3为找回密码表单  -->
        <div class="form-con">
          <template v-if="type === 1">
            <login-form @on-success-valid="handleSubmit"
                        :error_message='login_error' style="margin: 0px"></login-form>
            <Button class="modify-pass"
                    type="text"
                    style="text-align: center;"
                    @click="type = 3">忘记密码</Button>
            <Button class="register"
                    type="text"
                    style="text-align: center;"
                    @click="type = type == 2 ? 1 : 2"
                    :style="switchButtonStyle"
                    v-if="type !== 3">{{ message }}</Button>
          </template>
          <template v-if="type === 2">
            <register-form @on-success-valid="handleSubmitRegister"
                           :error_message='register_error' style="margin: 0px"></register-form>
            <Button class="register"
                    type="text"
                    style="text-align: center;"
                    @click="type = type == 2 ? 1 : 2"
                    :style="switchButtonStyle"
                    v-if="type !== 3">{{ message }}</Button>
          </template>
          <template v-if="type === 3">
            <modify-pass-form @on-success-valid="handleSubmitForgetPass"
                              :error_message='modifypass_error' style="margin: 0px"></modify-pass-form>
            <br>
            <Button type='primary' @click="type = 1" long>
              返回
            </Button>
          </template>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import LoginForm from '_c/login-form'
import RegisterForm from '_c/register-form'
import ModifyPassForm from '_c/modifypass-form'
// import { getErrModalOptions } from '@/libs/util.js'
import { mapActions } from 'vuex'
import { register, sendForgetPassForm } from '@/api/user'
export default {
  data () {
    return {
      type: 1,
      register_error: '',
      modifypass_error: '',
      login_error: ''
    }
  },
  components: {
    LoginForm,
    RegisterForm,
    ModifyPassForm
  },
  computed: {
    switchButtonStyle: function () {
      return this.type === 1 ? {
        margin: '0',
        float: 'right'
      } : {
        margin: '10px 0 0 0 ',
        width: '100%'
      }
    },
    message: function () {
      return this.type === 1 ? '注册账号' : '使用已有账号登录'
    }
  },
  methods: {
    ...mapActions(['handleLogin', 'handleRegister']),
    handleSubmit ({ userName, password }) {
      this.handleLogin({ userName, password }).then(res => {
        this.$router.push({
          name: this.$config.homeName
        })
      }).catch(err => {
        this.$Message.error('登录失败!')
        if (err.response.data.code === 401) {
          this.login_error = '账号或密码错误'
        } else {
          console.log(err)
          this.login_error = '用户未注册'
        }
      })
    },
    handleSubmitRegister ({ userName, password, email, verifyCode }) {
      const data = { username: userName, password: password, email: email, code: verifyCode }
      register('put', data).then(res => {
        this.$Message.success('注册成功！')
        this.register_error = ''
        this.type = 1 // 应该切换到登录界面
        console.log
      }).catch(err => {
        if (err.response.data.code===402) {
          this.register_error = '验证码错误!'
        }else if(err.response.data.code=== 409){
          this.register_error = '邮箱已注册!' 
        } else { // Username conflicted
          this.register_error = '用户名已被注册!'
        }
      })
    },
    handleSubmitForgetPass ({ password, email, verifyCode }) {
      const data = { password: password, email: email, code: verifyCode }
      sendForgetPassForm('put', data).then(res => {
        this.$Message.success('修改密码成功！')
        this.odifypass_error = ''
        this.type = 1 // 应该切换到登录界面
      }).catch(err => {
        if (err.response.data.error_msg.search(/Invalid confirm code/)) {
          this.modifypass_error = '验证码错误!'
        } else {
          this.modifypass_error = '邮箱未注册!'
        }
      })
    }
  }
}
</script>
