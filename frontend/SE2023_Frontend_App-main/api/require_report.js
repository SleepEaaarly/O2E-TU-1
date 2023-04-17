import axios from "@/config/requestConfig.js";

export const getRequireReport = async (id) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    let output = await axios.get('require_report', {
        id: id
    }, headers)
    return output
}