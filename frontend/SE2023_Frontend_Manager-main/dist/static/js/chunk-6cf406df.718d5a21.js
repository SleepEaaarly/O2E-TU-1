(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-6cf406df"],{"45bf":function(e,t,a){},"5d57":function(e,t,a){"use strict";a("dd9b")},"80c1":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("common-layout",[s("div",{staticClass:"top"},[s("div",{staticClass:"header"},[s("img",{staticClass:"logo",attrs:{alt:"logo",src:a("4ffd")}}),s("span",{staticClass:"title"},[e._v(e._s(e.systemName))])]),s("div",{staticClass:"desc"},[e._v("希望是一个好东西，也许是最好的，好东西是不会消亡的")])]),s("div",{staticClass:"login"},[s("a-form",{attrs:{form:e.form},on:{submit:e.onSubmit}},[s("a-tabs",{staticStyle:{padding:"0 2px"},attrs:{size:"large",tabBarStyle:{textAlign:"center"}}},[s("a-tab-pane",{key:"1",attrs:{tab:"账户密码登录"}},[s("a-alert",{directives:[{name:"show",rawName:"v-show",value:e.error,expression:"error"}],staticStyle:{"margin-bottom":"24px"},attrs:{type:"error",closable:!0,message:e.error,showIcon:""}}),s("a-form-item",[s("a-input",{directives:[{name:"decorator",rawName:"v-decorator",value:["name",{rules:[{required:!0,message:"请输入账户名",whitespace:!0}]}],expression:"[\n                'name',\n                {\n                  rules: [\n                    {\n                      required: true,\n                      message: '请输入账户名',\n                      whitespace: true,\n                    },\n                  ],\n                },\n              ]"}],attrs:{autocomplete:"autocomplete",size:"large",placeholder:"用户名"}},[s("a-icon",{attrs:{slot:"prefix",type:"user"},slot:"prefix"})],1)],1),s("a-form-item",[s("a-input",{directives:[{name:"decorator",rawName:"v-decorator",value:["password",{rules:[{required:!0,message:"请输入密码",whitespace:!0}]}],expression:"[\n                'password',\n                {\n                  rules: [\n                    {\n                      required: true,\n                      message: '请输入密码',\n                      whitespace: true,\n                    },\n                  ],\n                },\n              ]"}],attrs:{size:"large",placeholder:"密码",autocomplete:"autocomplete",type:"password"}},[s("a-icon",{attrs:{slot:"prefix",type:"lock"},slot:"prefix"})],1)],1)],1)],1),s("a-form-item",[s("a-button",{staticStyle:{width:"100%","margin-top":"24px"},attrs:{loading:e.logging,size:"large",htmlType:"submit",type:"primary"}},[e._v("登录")])],1)],1)],1)])},r=[],o=a("5530"),n=(a("14d9"),function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"common-layout"},[a("div",{staticClass:"content"},[e._t("default")],2),a("page-footer",{attrs:{"link-list":e.footerLinks,copyright:e.copyright}})],1)}),i=[],c=a("613e"),l=a("5880"),m={name:"CommonLayout",components:{PageFooter:c["a"]},computed:Object(o["a"])({},Object(l["mapState"])("setting",["footerLinks","copyright"]))},u=m,d=(a("b3ef"),a("2877")),p=Object(d["a"])(u,n,i,!1,null,"63c094a6",null),g=p.exports,f=a("93d6"),b=a("b775"),h=a("89a5"),v={name:"Login",components:{CommonLayout:g},data:function(){return{logging:!1,error:"",form:this.$form.createForm(this)}},computed:{systemName:function(){return this.$store.state.setting.systemName}},methods:Object(o["a"])(Object(o["a"])({},Object(l["mapMutations"])("account",["setUser","setPermissions","setRoles"])),{},{onSubmit:function(e){var t=this;e.preventDefault(),this.form.validateFields((function(e){if(!e){t.logging=!0;var a=t.form.getFieldValue("name"),s=t.form.getFieldValue("password");"SUPERMAN"==a?(t.$message.error("账号或密码错误"),t.logging=!1):Object(f["b"])(a,s).then(t.afterLogin).catch((function(e){t.$message.error("账号或密码错误"),t.logging=!1}))}}))},afterLogin:function(e){var t=this,a=[{CN:"管理员 | O2E-TU-2-后台管理",HK:"Java工程師 | 螞蟻金服-計算服務事業群-微信平台部",US:"Java engineer | Ant financial - Computing services business group - WeChat platform division"}],s={name:e.data.userInfo.username,avatar:"https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",address:"重庆市",position:a[0]},r=[{id:"admin",operation:["add","edit","delete"]}];this.logging=!1;var o=e.data;o.message="欢迎回来",this.setUser(s),this.setRoles(r),Object(b["g"])({token:e.data.access_token,expireAt:new Date((new Date).getTime()+18e5)}),Object(f["a"])().then((function(e){var a=e.data.data;Object(h["d"])(a),t.$router.push("/dashboard"),t.$message.success(o.message,3)}))}})},w=v,y=(a("5d57"),Object(d["a"])(w,s,r,!1,null,"3adbb8b9",null)),x=y.exports;t["default"]=x},b3ef:function(e,t,a){"use strict";a("45bf")},dd9b:function(e,t,a){}}]);