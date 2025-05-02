import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const getMusicRecommendation = async (roomId: string, token: string) => {
  const response = await axios.post(
    `${API_URL}/api/music-recommendation/predict`,
    undefined,
    {
      params: {
        room_id: roomId,
      },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )
  return response.data
}
