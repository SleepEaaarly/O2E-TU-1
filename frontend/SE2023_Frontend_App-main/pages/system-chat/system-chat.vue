<template>
    <view>
        <tui-button v-if="!isHuman" @click="openmenu" :size="28" :plain="true">
            当前问题类型为{{questionType==='basic'?"平台功能问题":"其他问题"}}
        </tui-button>
        <template v-if="!isHuman">
            <tui-bubble-popup :show="show" :mask="true" position="absolute" width="370rpx" translateY="0rpx" triangleTop="-50rpx" borderWidth="0" @close="openmenu()">
				<tui-list-cell :hover="true" :arrow="true" backgroundColor="#dcdcdc" @click="switchQuestionType(0)">
					<tui-icon name="search"></tui-icon>
						平台功能问题
				</tui-list-cell>
				
			</tui-bubble-popup>
            <tui-bubble-popup :show="show" :mask="false" position="absolute" width="370rpx" translateY="0rpx" translateX="380rpx" triangleTop="-20rpx" borderWidth="0" @close="openmenu()">
				<tui-list-cell :hover="true" :arrow="true" backgroundColor="#dcdcdc" @click="switchQuestionType(1)">
					<tui-icon name="search"></tui-icon>
					其他问题
				</tui-list-cell>
			</tui-bubble-popup>
        </template>
        <scroll-view id="scrollview" scroll-y :scroll-top="scrollTop"
        :scroll-with-animation="true"
        refresher-enabled
        @refresherrefresh="scrollTopHandle"
        :refresher-triggered="triggered"
        :style="{height: style.contentH + 'px'}">
            <!-- 聊天列表 -->
            <block v-for="(item, index) in currentSystemChatMsgs" :key="index">
                <view class="chat-item">
                    <system-chat-list 
                        @goToUserInfo="goToUserInfo" 
                        :item="item" :index="index" :isHuman="isHuman"></system-chat-list>
                </view>
            </block>
            <require_message_card
                title="请帮我写软工吧"
                companyName="北京航空航天大学"
                :companyLogoPath="testpic"
                intro="Here is a summary of some of the most commonly used methods in machine learning."
                time="上午 7:43"
                ></require_message_card>
                <system-chat-list 
                        @goToUserInfo="goToUserInfo" 
                        :item="item" :isHuman="isHuman"></system-chat-list>
            <work_message_card 
                title="A Summary of Machine Learning" 
                expertName="占瑞乙" 
                expertLogoPath="/static/head_zry_fox.jpg"
                intro="Here is a summary of some of the most commonly used methods in machine learning." 
                time="上午 7:45">

            </work_message_card>
        </scroll-view>
        
        <system-chat-bottom @submit="submit" @isHuman="getHuman" :isai="isHuman"></system-chat-bottom>
    </view>
</template>

<script>
    import systemChatBottom from 'components/system-chat/system-chat-bottom.vue'
    import systemChatCard from 'components/system-chat/system-chat-card.vue'
    import systemChatList from 'components/system-chat/system-chat-list.vue'
    import time from '../../common/time'
    import {mapState, mapMutations, mapGetters} from 'vuex'
    import {showSystemMessage, pushSystemMessage, getBasicAISystemQuestionAns, 
        getAdvanceAISystemQuestionAns, createSystemChat, getSystemChat,
        readSystemChatMsg} from '@/api/system-chat.js'
    // import {acceptOrder, rejectOrder, accomplishOrder} from '@/api/platform/order.js'
    import {picUrl} from '@/api/common.js'
    import Vue from 'vue'
    // import {getOrderDetail} from '@/api/order-detail.js'
    // import {getNeedDetail} from '@/api/need-detail.js'
    import require_message_card from '../../components/require_message_card.vue'
    import work_message_card from '../../components/work_message_card.vue'
    export default {
        components: {
            systemChatBottom,
            systemChatCard,
            systemChatList,
            require_message_card,
            work_message_card
        },
        computed: {
            ...mapState(['system_chat', 'userInfo']),
            ...mapGetters(['currentSystemChatMsgs'])
        },
        data() {
            return {
                testpic: "/static/head.jpg",
                aiPic: "/static/head.jpg",
                isShow: false,
                isHuman: false,
                currentState: 'AI',
                questionType: 'basic',   // basic or advance
                // test
                item: {
                    // fromId: 0,
                    // toId: 0,
                    // index: 0,
                    isme: 0,    // 是不是本人发的，如果是本人发送的则显示在屏幕右边
                                    // 如果不是本人发的，则显示在屏幕左边
                    userpic: "userpiclink", // 用户头像，如果是消息是本人发送的，头像就是本人头像，否则就是对面人的头像
                    type: 'text',   // 可选的值包括 'switch info', 'text', 'pic', 'card'
                    /*
                        message：
                            1. 如果是 switch info，则 message 无意义
                            2. 如果是 text，则 message 本身就是需要展示的值
                            3. 如果是 pic，则 message 本身是图片的 url
                            4. 如果是 card，则 message 无意义，具体的内容在 card info 中
                    */
                    message: "测试0", 
                    // time: "test time", 显示出来的聊天框时间
                    cardInfo: {
                        cardType: "expert", // expert enterpise demand technique(chengguo)
                        title: "专家名称/企业名称/需求名称/成果名称",
                        avatar: "专家头像/企业图片/需求图片/成果图片 没有则默认",
                        info: "企业简介/专家简介/需求简介/成果简介"
                    },
                    gstime: null,
                    created_at: "test created"
                },
                style: {
                    contentH: 0,
                    itemH: 0,
                },
                triggered: false,
                scrollTop: 0,
                list: [],
                cId: 0,
                socket: null,
                fid: undefined,
                show: false,
                timer: null,
            }
        },
        onShow() {
            this.isShow = true
        },
        beforeDestroy() {
            this.isShow = false
            // this.setIndex()
            // this.setMsgPage(1)
            this.clear()
        },
        // 监听下拉刷新
        onPullDownRefresh() {
            // init data
            this.initdata()
        },
        async onLoad(data) {    // 设置导航栏标题和设置导航栏颜色
            console.log(data)
            uni.setNavigationBarColor({
                frontColor: "#000000",
                backgroundColor: '#fffae1',
                animation: {
                    duration: 500,
                    timingFunc: 'easeInOut' // 动画以低速开始和结束
                }
            })
            this.initorder()
        },
        onReady() {
            this.getData()
            this.initdata()
            this.pageToBottom(true)
            this.initorder()
            this.initdata()
            readSystemChatMsg(this.userInfo.id)
        },
        // 监听标题栏按钮点击事件
        onNavigationBarButtonTap(e) { 
            // 有很多功能可以做，例如点击右上角头像按钮实现跳转逻辑
            switch (e.index) {
                case 0: 
                    this.goToUserInfo(this.system_chat.uId)
                    break
            }
        },
        watch: {
            currentSystemChatMsgs(old) {
                if (this.triggered) {

                } else {
                    this.pageToBottom(true)
                }
            }
        },
        methods: {
            ...mapMutations([
                'addSystemChatMessage',
                'addSystemNoReadMessage',
                'setSystemChat']),
            // 监听chat bottom子组件中 isHuman 的变化
            getHuman(isHuman) {
                let now = new Date().getTime()
                console.log(isHuman)
                this.isHuman = isHuman
                if (isHuman === true) {
                    this.currentState = '人工'
                    showSystemMessage(this.userInfo.id, 1)   // 在管理端展示聊天窗口
                } else {
                    this.currentState = 'AI'
                    showSystemMessage(this.userInfo.id, 0)  // 不在管理端展示聊天窗口
                }
                let obj = { // 插入前端列表的数据
                    isme: 1,
                    userpic: this.userInfo.userpic,
                    type: 'switch_info',
                    message: "give up",
                    time: time.gettime.gettime(now),
                    cardInfo: {},
                    gstime: now,
                    created_at: now
                }
                if (isHuman) {
                    obj.message = '人工'
                } else {
                    obj.message = 'AI'
                }
                this.addSystemChatMessage(obj)
                this.pageToBottom(true)
            },
            switchQuestionType(data) {
                if (data == null) {
                    if (this.questionType === 'basic') {
                        this.questionType = 'advance'
                    } else {
                        this.questionType = 'basic'
                    }
                } else if (data == 0) {
                    this.questionType = 'basic'
                } else if (data == 1) {
                    this.questionType = 'advance'
                }
                this.openmenu()
            },
            // 初始化参数
            async initdata() {  // 获得页面信息（高度）
                try {
                    const res = uni.getSystemInfoSync()
                    let t = 200
                    this.style.contentH = res.windowHeight - uni.upx2px(t)
                    uni.stopPullDownRefresh()
                } catch (e) { }
            },
            refresh() {     // 刷新，每个5秒
                this.timer = setInterval(() => {
                    setTimeout(this.trym, 0)
                }, 1000 * 5)
            },
            async initorder() { // 获得专家和企业之间的需求和订单信息

            },
            async sendm(data) { // 通过 submit 发送数据
                this.submit(data)
            },
            scrollTopHandle() {
                console.log("system chat scroll top handle")
                if (this.triggered) {
                    setTimeout(() => {
                        // 这部分还不太明白学长写的啥意思
                    }, 200)
                    return
                }
                this.triggered = true
            },
            pageToBottom(isfirst = false) {    // 页面展示当前聊天的底部
                let q = uni.createSelectorQuery().in(this)
                let itemH = q.selectAll('.chat-item')   // TODO: 不确定这个是否可行
                // console.log(this.currentSystemChatMsgs)
                if (this.currentSystemChatMsgs.length !== 0) {
                    this.$nextTick(() => {
                        itemH.fields({size: true}, data => {
                            console.log("data is")
                            console.log(data)
                            if (data) {
                                if (isfirst) {
                                    for (let i = 0; i < data.length; i++) {
                                        this.style.itemH += data[i].height
                                    }
                                    console.log(this.style.itemH)
                                } else {
                                    this.style.itemH += data[data.length - 1].height
                                }
                                this.scrollTop = (this.style.itemH > this.style.contentH) ? this.style.itemH : 0
                            }
                        }).exec()
                    })
                }
            },
            openmenu() {    // 开启和关闭菜单
                if (this.show) {
                    this.show = false
                } else {
                    this.show = true
                }
            },
            clear() {   // 清除计时器
                clearInterval(this.timer)
                this.timer = null
            },
            goToUserInfo(uid) { // 进入用户空间
                uni.navigateTo({url: '../../pages/user-space/user-space?uid=' + uid})
            },
            // 获取聊天数据
            async getData() {
                // 从服务器上获取到的数据
                let chatroomId = await createSystemChat({
                    uId: this.userInfo.id
                })
                let result = await getSystemChat(this.userInfo)
                console.log(result)
                console.log(result.isai)
                if (result.isai == 1) {
                    this.isHuman = false
                } else {
                    this.isHuman = true
                    
                }
                console.log(this.isHuman)
                let load_system_chat = {}
                load_system_chat.noreadnum = result.noreadnum
                load_system_chat.messages = []
                let last_time = 0
                for (var i = 0; i < result.messages.length; i++) {
                    let message = {}
                    message.message = result.messages[i].message
                    message.isme = result.messages[i].isme
                    message.userpic = result.messages[i].user_pic
                    message.type = result.messages[i].type
                    message.gstime = time.gettime.getChatTime(result.messages[i].created_at, last_time)
                    last_time = result.messages[i].created_at
                    load_system_chat.messages.push(message)
                    // console.log(message)
                }
                // console.log(load_system_chat)
                this.setSystemChat(load_system_chat)
                // console.log(this.currentSystemChatMsgs)
            },
            async submit(data) {    // 提交（发送）信息
                console.log("submit data")
                // 构建数据
                let now = new Date().getTime()
                if (data === '') {
                    uni.showToast({
                        title: '消息不能为空',
                        icon: 'none'
                    })
                    return
                }
                let msg = await pushSystemMessage({   // 发送给后端的数据
                    'uId': this.userInfo.id,
                    'content': data,
                    "isme": 1
                })
                let obj = { // 插入前端列表的数据
                    isme: 1,
                    userpic: this.userInfo.userpic,
                    type: 'text',
                    message: data,
                    // message: "http://127.0.0.1:8000/api/images/202205/07/icons/1651921131602.png",
                    time: time.gettime.gettime(now),
                    cardInfo: {},
                    gstime: now,
                    created_at: now
                }
                this.addSystemChatMessage(obj)
                if (!this.isHuman) {    // 如果不是人工，则可以直接获得输出
                    if (this.questionType === 'basic') {    // 对于操作的基础问题，可以直接输出结果
                        // 1. 将问题送入楚珉的AI模型接口，获取输出
                        let output = await getBasicAISystemQuestionAns(data)
                        // 1.5 判断code是否等于200，如果等于500不进行接下来的判断
                        if (code !== 200) {
                            // 我觉得还是提示一下比较好
                            console.log("基础问题：失败")
                            uni.showToast({
                                title: output.error_msg,
                                icon: 'none'
                            })
                            return
                        }
                        // 2. 判断是否转人工
                        if (output.transfer == "True" || output.transfer == true) {
                            // 转人工
                            // 2.1 构建转人工信息
                            let now = new Date().getTime()
                            let obj = { // 插入前端列表的数据
                                isme: 0,
                                userpic: this.aiPic,
                                type: 'text',
                                message: "啊偶，遇到我不会的了，建议您转人工哦",
                                time: time.gettime.gettime(now),
                                cardInfo: {},
                                gstime: now,
                                created_at: now
                            }
                            // 2.2 将转人工信息发送给数据库
                            let msg = await pushSystemMessage({   // 发送给后端的数据
                                'uId': this.userInfo.id,
                                'content': "啊偶，遇到我不会的了，建议您转人工哦",
                                "isme": 0
                            })
                            // 2.3 将转人工信息插入前端store
                            this.addSystemChatMessage(obj)
                        } else {
                            // 不转人工
                            // 2.1 构建转人工信息
                            let now = new Date().getTime()
                            let obj = { // 插入前端列表的数据
                                isme: 0,
                                userpic: this.aiPic,
                                type: 'text',
                                message: output.answer,
                                time: time.gettime.gettime(now),
                                cardInfo: {},
                                gstime: now,
                                created_at: now
                            }
                            // 2.2 将转人工信息发送给数据库
                            let msg = await pushSystemMessage({   // 发送给后端的数据
                                'uId': this.userInfo.id,
                                'content': output.answer,
                                "isme": 0
                            })
                            // 2.3 将转人工信息插入前端store
                            this.addSystemChatMessage(obj)
                        }
                    } else {    // 其他问题，流程：
                        // 1. 将问题送入自动回复模型接口2，回收楚珉output
                        let output = await getAdvanceAISystemQuestionAns(data)
                        // 1.5 判断code
                        if (code !== 200) {
                            // 错误处理
                            console.log("其他问题：失败")
                            uni.showToast({
                                title: output.error_msg,
                                icon: 'none'
                            })
                            return
                        }
                        // 2.1 处理信息
                        let now = new Data().getTime()
                        let obj = { // 插入前端列表的数据
                            isme: 0,
                            userpic: this.aiPic,
                            type: 'text',
                            message: output.answer,
                            time: time.gettime.gettime(now),
                            cardInfo: {},
                            gstime: now,
                            created_at: now
                        }
                        // 2.2 将转人工信息发送给数据库
                        let msg = await pushSystemMessage({   // 发送给后端的数据
                            'uId': this.userInfo.id,
                            'content': output.answer,
                            "isme": 0
                        })
                        // 2.3 将转人工信息插入前端store
                        this.addSystemChatMessage(obj)
                        // 2.4.1 专家信息
                        let expertList = output.card.expert
                        for (let i = 0; i < expertList.length; i++) {
                            // 2.4.1.1 构建专家信息
                            let obj = {
                                isme: 0,
                                userpic: this.aiPic,
                                type: 'card',
                                message: "一条卡片信息~",
                                time: time.gettime.gettime(now),
                                cardInfo: expertList[i],
                                gstime: now,
                                created_at: now
                            }
                            // 2.4.1.2 将信息发送给数据库
                                // TODO: 这个有点麻，可能还得和涛哥约定一下如何传输数据
                            // 2.4.1.3 将信息插入前端 store
                            this.addSystemChatMessage(obj)
                        }
                        // 2.4.2 企业信息
                        let enterpriseList = output.card.enterprise 
                        for (let i = 0; i < enterpriseList.length; i++) {
                            // 2.4.2.1 构建企业信息
                            let obj = {
                                isme: 0,
                                userpic: this.aiPic,
                                type: 'card',
                                message: "一条卡片信息~",
                                time: time.gettime.gettime(now),
                                cardInfo: enterpriseList[i],
                                gstime: now,
                                created_at: now
                            }
                            // 2.4.2.2 将信息发送给数据库
                                // TODO: 这个有点麻，可能还得和涛哥约定一下如何传输数据
                            // 2.4.2.3 将信息插入前端 store
                            this.addSystemChatMessage(obj)
                        }
                        // 2.4.3 成果信息
                        let resultList = output.card.result
                        for (let i = 0; i < resultList.length; i++) {
                            // 2.4.3.1 构建企业信息
                            let obj = {
                                isme: 0,
                                userpic: this.aiPic,
                                type: 'card',
                                message: "一条卡片信息~",
                                time: time.gettime.gettime(now),
                                cardInfo: resultList[i],
                                gstime: now,
                                created_at: now
                            }
                            // 2.4.3.2 将信息发送给数据库
                                // TODO: 这个有点麻，可能还得和涛哥约定一下如何传输数据
                            // 2.4.3.3 将信息插入前端 store
                            this.addSystemChatMessage(obj)
                        }
                    }
                }
                this.pageToBottom(true) // 页面到新的数据处
            },
        }
    }
</script>

<style>

</style>