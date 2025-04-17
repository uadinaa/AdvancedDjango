// import axios from 'axios'
// import { refreshAccessToken } from './services/auth'
//
// const instance = axios.create({
//   baseURL: 'http://localhost:8000/api/',
// })
//
// instance.interceptors.request.use(config => {
//   const token = localStorage.getItem('access')
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`
//   }
//   return config
// })
//
// // Auto-refresh on 401
// instance.interceptors.response.use(
//   res => res,
//   async err => {
//     const originalRequest = err.config
//     if (err.response?.status === 401 && !originalRequest._retry) {
//       originalRequest._retry = true
//       const newAccess = await refreshAccessToken()
//       if (newAccess) {
//         originalRequest.headers.Authorization = `Bearer ${newAccess}`
//         return instance(originalRequest)
//       }
//     }
//     return Promise.reject(err)
//   }
// )

// export default instance

// src/axios.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json'
  }
})

instance.interceptors.request.use(config => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default instance
