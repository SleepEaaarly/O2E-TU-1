import axios from '../config/requestConfig.js';

export const enterprise_certificate = async (data) => {
	console.log("enterprise_certificate");
	let result = await axios.post('enterprise/setinfo', data);
	return result;
}