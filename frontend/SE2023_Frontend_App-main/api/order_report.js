import axios from "@/config/requestConfig.js";

export const getOrderReport = async (id) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token') 
    }
    let output = await axios.get('order_report/get', {
        id: id,
    }, headers)
    return output
}