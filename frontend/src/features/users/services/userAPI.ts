import axios from 'axios'

const API_URL = 'http://localhost:8000' // API Gateway adresi

export const fetchAllUsers = async (token: string) => {
  const response = await axios.get(`${API_URL}/api/auth/users`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.data
}
