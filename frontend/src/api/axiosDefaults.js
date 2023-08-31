import axios from "axios";

// axios.defaults.baseURL = 'https://web-3-degenz-f7ab1c03f599.herokuapp.com/'
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data'
axios.defaults.withCredentials = true

export const axiosReq = axios.create();
export const axiosRes = axios.create();