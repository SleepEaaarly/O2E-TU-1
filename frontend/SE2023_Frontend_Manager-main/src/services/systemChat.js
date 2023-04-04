import { request, METHOD } from "../utils/request";
import { BASE_URL_IP } from "./api";

export const getSystemChatAll = () => {
    const url = `${BASE_URL_IP}/api/systemChat/getall`;
    return request(url, METHOD.GET);
}
