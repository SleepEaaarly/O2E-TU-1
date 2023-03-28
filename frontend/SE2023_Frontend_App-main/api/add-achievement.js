import axios from '@/config/requestConfig.js';



export const addachievement = async (data) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
	// console.log('add new achievement')
	// console.log(data.type)
    if (0 == data.type - '0') {
        let result = await axios.post('paper/add', data, headers)
    } else if (1 == data.type - '0') {
        let result = await axios.post('patent/add', data, headers)
    } else if (2 == data.type - '0') {
        let result = await axios.post('project/add', data, headers)
    } else {
        console.log('Fail to add achievement.[Reason: AchType ERROR]')
    }
    return result
}

export const saveachievement = async (data) => {
    let result = addachievement(data)
    return result
}