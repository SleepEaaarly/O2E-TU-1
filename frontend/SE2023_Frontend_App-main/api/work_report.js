import axios from "@/config/requestConfig.js";

export const getWorkReport = async (id) => {
    // 通过成果报告的id获取生成好的成果报告
    // 这里返回的数据结构应该不能像定义的那样简单
    let headers = {
        "Authorization": "Bearer " + uni.getStorageSync('token')
    }
    let output = await axios.get('work_report/get', {
        id: id,
    }, headers)
    return output
}

