import Swal from 'sweetalert2'
import { getMusicRecommendation } from '../services/musicAPI'
import { useAppSelector } from '../../../app/hooks'

interface Props {
  currentUser: string
  targetUser: string
}

const RecommendationButton = ({ currentUser, targetUser }: Props) => {
  const token = useAppSelector((state) => state.auth.token)

  const handleClick = async () => {
    if (!token) return
  
    const roomId = [currentUser, targetUser].sort().join('_')
  
    // Loading ekranı
    Swal.fire({
      title: 'Tavsiye alınıyor...',
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading()
      }
    })
  
    try {
      const data = await getMusicRecommendation(roomId, token)
      const music = data.recommended_music
  
      // Tavsiye başarıyla alındı → yeni alert
      Swal.fire({
        title: '🎵 Müzik Tavsiyesi',
        html: `
          <strong>Parça:</strong> ${music.Song_Name}<br/>
          <strong>Sanatçı:</strong> ${music.Artist}<br/>
          <strong>Tür:</strong> ${music.Genre}<br/>
          <strong>Duygu:</strong> ${music.Sentiment_Label}
        `,
        icon: 'info',
        confirmButtonText: 'Tamam',
      })
    } catch (err) {
      // Hata olursa
      Swal.fire({
        title: 'Hata',
        text: 'Tavsiye alınamadı',
        icon: 'error',
      })
    }
  }
  
  

  return <button onClick={handleClick}>🎧 Müzik Tavsiyesi Al</button>
}

export default RecommendationButton
