(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2a2fe798"],{"2ba6":function(t,a,e){},"4a1f":function(t,a,e){"use strict";e.r(a);var s=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",[e("div",{class:["search-head",t.layout,t.pageWidth]},[e("div",{staticClass:"search-input"},[e("a-input-search",{staticClass:"search-ipt",staticStyle:{width:"522px"},attrs:{placeholder:"请输入...",size:"large",enterButton:"搜索"}})],1),e("div",{staticStyle:{padding:"0 24px"}},[e("a-tabs",{attrs:{tabBarStyle:{margin:0},activeKey:t.activeKey},on:{change:t.navigate}},[e("a-tab-pane",{key:"1",attrs:{tab:"文章"}}),e("a-tab-pane",{key:"2",attrs:{tab:"应用"}}),e("a-tab-pane",{key:"3",attrs:{tab:"项目"}})],1)],1)]),e("div",{staticClass:"search-content"},[e("router-view")],1)])},c=[],r=e("5530"),i=(e("14d9"),e("5880")),n={name:"SearchLayout",computed:Object(r["a"])(Object(r["a"])({},Object(i["mapState"])("setting",["layout","pageWidth"])),{},{activeKey:function(){switch(this.$route.path){case"/list/search/article":return"1";case"/list/search/application":return"2";case"/list/search/project":return"3";default:return"1"}}}),methods:{navigate:function(t){switch(t){case"1":this.$router.push("/list/search/article");break;case"2":this.$router.push("/list/search/application");break;case"3":this.$router.push("/list/search/project");break;default:this.$router.push("/workplace")}}}},u=n,h=(e("695f"),e("2877")),l=Object(h["a"])(u,s,c,!1,null,"6ef899ce",null);a["default"]=l.exports},"695f":function(t,a,e){"use strict";e("2ba6")}}]);