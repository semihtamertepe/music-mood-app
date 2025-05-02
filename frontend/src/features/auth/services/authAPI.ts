import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const login = async (username: string, password: string) => {
  const response = await axios.post(`${API_URL}/api/auth/login`, {
    username,
    password,
  })
  return response.data
}

export const register = async (formData: any) => {
  const response = await axios.post(`${API_URL}/api/auth/register`, formData)
  return response.data
}

