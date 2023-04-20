import axios from "@/config/requestConfig.js";

export const requireGenerateCard = async (uId, id) => {
	let headers = {
		'Authorization': 'Bearer ' + uni.getStorageSync('token')
	}
	await axios.post('need_report/generateCard', {
		uId: uId,
		id: id
	}, headers)
}

export const getRequireReport = async (id) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    let output = await axios.get('require_report', {
        id: id
    }, headers)
    return output
}