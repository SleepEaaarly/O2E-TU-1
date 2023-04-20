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

export const orderGenerateCard = async (expertId, enterpriseId, id) => {
    let headers = {
        'Authorization': 'Bearer ' + uni.getStorageSync('token')
    }
    await axios.get('order_report/generateCard', {
        expertId: expertId,
        enterpriseId: enterpriseId,
        id: id
    }, headers)
}