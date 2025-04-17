import axios from '../axios'

export async function refreshAccessToken() {
  const refresh = localStorage.getItem('refresh')
  if (!refresh) return null

  try {
    const res = await axios.post('auth/token/refresh/', { refresh })
    localStorage.setItem('access', res.data.access)
    return res.data.access
  } catch {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    return null
  }
}

export function hasRole(requiredRoles) {
  const role = localStorage.getItem('role')
  return requiredRoles.includes(role)
}
