import axios from '@/config/requestConfig.js';



export const addachievement = async (data) => {
    let headers = {
        "Authorization": 'Bearer ' + uni.getStorageSync('token')
    }
	// console.log('add new achievement')
	// console.log(data.type)
    
    let result = await axios.post('result/add', data, headers)
    return result
    // console.log('Fail to add achievement.[Reason: AchType ERROR]')
}

export const saveachievement = async (data) => {
    let result = addachievement(data)
    return result
}