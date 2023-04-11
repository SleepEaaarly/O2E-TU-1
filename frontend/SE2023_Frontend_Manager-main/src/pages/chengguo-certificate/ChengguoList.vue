<template>
<div>
    <a-card :bordered="false">
        <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="listData">
            <a-list-item slot="renderItem" key="item.title" slot-scope="item">
                <a-space direction="vertical" slot="extra" width="272" aligh="end" style="margin-right: 20px;">
                    <a-row>
                        <a-col :span="24">
                            <a-button type="text" style="width: 80px" @click="handleShow(item.id)">
                                查看
                            </a-button>
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col :span="24">
                            <a-popconfirm title="确定通过审核吗？" ok-text="确定" cancel-text="取消" @confirm="handleApply(item.id)">
                                <a-button type="primary" style="width: 80px"> 通过</a-button>
                            </a-popconfirm>
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col :span="24">
                            <a-popconfirm title="确定拒绝通过吗？" ok-text="确定" cancel-text="取消" @confirm="handleRefuse(item.id)">
                                <a-button type="danger" style="width: 80px"> 拒绝</a-button>
                            </a-popconfirm>
                        </a-col>
                    </a-row>
                </a-space>
                <a-modal v-model="showDetail" title="" @ok="handleOk" width="750px">
                    <ChengguoCard v-if="showDetail" v-bind="post"></ChengguoCard>
                </a-modal>
                <a-list-item-meta :description="item.create_time">
                    <a slot="title" :herf="item.herf">{{ item.chengguoName }}</a>
                    <a-avatar slot="avatar" shape="square"  :src="item.pic"></a-avatar>
                </a-list-item-meta>
                <a style="display: block;" class="textbreak" herf="javascript:void(0)" @click="handleShow(item.id)">
                    成果信息简介：{{ item.profile | ellipsis }}
                </a>
            </a-list-item>
        </a-list>
    </a-card>
</div>
</template>

<script>
import ChengguoCard from './ChengguoCard.vue';
export default {
    name: "ChengguoList",
    components: {ChengguoCard},
    filters: {
        ellipsis (value) {
            if (!value) return ''
            if (value.length > 130) {
                return value.slice(0,130) + '...'
            }
            return value
        }
    },
    data() {
        return {
            listData: [
                {
                    id: 0,
                    chengguoName: "成果名称",
                    create_time: "申请时间：2023-04-04T01:39:28.970Z",
                    profile: "成果简介成果简介成果简介成果简介成果简介成果简介成果简介成果简介",
                    pic: "http://127.0.0.1:8000/api/images/202205/02/icons/zkg.jpg"
                }
            ]
        }
    },
    mounted() {
        
    },
    inject: ['reload'],
    methods: {
        
    },
}
</script>

<style scoped>
a:link {
  color: black;
} /* 未被访问的链接 */
a:hover {
  color: #13c2c2;
} /* 鼠标指针移动到链接上 */
a:active {
  color: #13c2c2;
} /* 正在被点击的链接 */
</style>