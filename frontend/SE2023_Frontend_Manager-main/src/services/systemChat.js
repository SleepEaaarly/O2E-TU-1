import { request, METHOD } from "../utils/request";
import { BASE_URL_IP } from "./api";

export const getSystemChatAll = () => {
    const url = `${BASE_URL_IP}/api/system_chat/getall`;
    return request(url, METHOD.GET);
}

export const pushSystemChat = (params) => {
    const url = `${BASE_URL_IP}/api/system_chat/pushAdmin`
    return request(url, METHOD.POST, params);
}