<template>
  <Form ref="form" :model="form" :rules="ruleCustom" :label-width="80">
    <Form-item label="用户名" prop="userName">
      <Input type="text" v-model="form.userName" required='true'></Input>
    </Form-item>

    <Form-item label="密码" prop="password">
      <Input type="password" v-model="form.password"></Input>
    </Form-item>
    <Form-item label="确认密码" prop="passwordCheck">
      <Input type="password" v-model="form.passwordCheck"></Input>
    </Form-item>
    <Form-item label="邮箱" prop="email">
      <Input type="email" v-model="form.email"></Input>
    </Form-item>
    <Form-item class='verify-item' label="验证码" prop="verifyCode">
      <Input class='verify-input' type="text" v-model="form.verifyCode"></Input>
    </Form-item>
    <Button :disabled='verifyDisabled' @click='handleSendVerify' class='send-verify'>{{verifyHint}}</Button>
    <p style="color: red;text-align: center;">{{error_message}}</p>
    <Button type='primary' @click="handleSubmit('form')" long>注册</Button>
  </Form>
</template>
<script>
import { sendRegiserEmail } from '@/api/user'
export default {
  data () {
    const validateAccount = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入账号'))
      } else if (value.length < 6 || value.length > 16) {
        callback(new Error('账号长度应在6-16位之间'))
      } else {
        callback()
      }
    }
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else if (value.length < 6 || value.length > 16) {
        callback(new Error('密码长度应在6-16位之间'))
      } else {
        if (this.form.passwdCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.form.validateField('passwordCheck')
        }
        callback()
      }
    }
    const validatePassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入邮箱'))
      } else if (!value.match(/[^@]+@[^@.]+\.[^@]/)) {
        callback(new Error('邮箱格式错误！'))
      } else {
        callback()
      }
    }

    return {
      verifyHint: '发送验证码',
      verifyDisabled: false,
      gap: 60,
      timer: null,
      form: {
        userName: '',
        password: '',
        passwordCheck: '',
        email: '',
        verifyCode: ''

      },
      ruleCustom: {
        userName: [{
          required: true,
          validator: validateAccount,
          trigger: 'blur'
        }],
        password: [{
          required: true,
          validator: validatePass,
          trigger: 'blur'
        }],
        passwordCheck: [{
          required: true,
          validator: validatePassCheck,
          trigger: 'blur'
        }],
        email: [{
          required: true,
          validator: validateEmail,
          trigger: 'blur'
        }],
        verifyCode: [{
          required: true,
          message: '请输入验证码'
        }]
      }
    }
  },
  props: {
    error_message: {
      type: String,
      default: ''
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$emit('on-success-valid', {
            userName: this.form.userName,
            password: this.form.password,
            email: this.form.email,
            verifyCode: this.form.verifyCode
          })
        } else {
          this.$Message.error('注册失败!')
        }
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    handleSendVerify () {
      this.$refs.form.validateField('email')
      sendRegiserEmail('post', {
        email: this.form.email
      }).then(res => {
        this.$Message.success('发送成功!')
      }).catch(err => {
        console.log(err)
        console.log(this.form.email)
        this.$Message.error('邮箱已被注册!')
      })
      this.verifyDisabled = true
      this.timer = setInterval(() => {
        this.gap--
        this.verifyHint = this.gap + '秒'
        if (this.gap === 0) {
          clearInterval(this.timer)
          this.verifyDisabled = false
          this.verifyHint = '发送验证码'
          this.gap = 6
        }
      }, 1000)
    }
  }
}
</script>

<style>
.verify-item {
  width: 160px;
  display: inline-block;
}
.verify-input {
  width: 80px;
}

.send-verify {
  margin-left: 10px;
  display: inline-block;
}
</style>
