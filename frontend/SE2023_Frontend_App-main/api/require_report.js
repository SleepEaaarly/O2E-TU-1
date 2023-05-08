import axios from "@/config/requestConfig.js";

export const requireGenerateCard = async (uId, id) => {
	let headers = {
		'Authorization': 'Bearer ' + uni.getStorageSync('token')
	}
    console.log("sadfadf")
    console.log(uId)
    console.log(id)
	await axios.post('need_report/generateCard', {
		uId: uId,
		id: id
	}, headers)
    console.log("sdfadfa")
}

export const getRequireReport = async (id) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
    let output = await axios.get('need_report/get', {
        reportId: id
    }, headers)
    return output
}