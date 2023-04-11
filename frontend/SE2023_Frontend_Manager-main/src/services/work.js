import {request, METHOD} from "../utils/request";
import {WorkAll, BASE_URL_IP} from './api';

export const getWorkAll = () => {
    let paras = {"field": '',"period": '',"key_word": ''}
    return request(WorkAll, METHOD.GET, paras);
}

export const getWork = (id, method) => {
    const url = `${BASE_URL_IP}/api/result/getinfo/${id}`
    return request(url, method);
}

export const WorkApply = (id, method) => {
    const url = `${BASE_URL_IP}/api/result/agree/${id}`
    return request(url, method)
}

export const WorkRefuse = (id, method) => {
    const url = `${BASE_URL_IP}/api/result/refuse/${id}`

    return request(url, method)
}
