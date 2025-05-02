import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register } from '../services/authAPI'

const RegisterForm = () => {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '',
    surname: '',
    username: '',
    password: '',
    favorite_artist: '',
    favorite_genre: ''
  })
  const [error, setError] = useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await register(form)
      navigate('/login')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Kayıt işlemi başarısız.')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Kayıt Ol</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <input name="name" placeholder="Ad" required onChange={handleChange} />
      <input name="surname" placeholder="Soyad" required onChange={handleChange} />
      <input name="username" placeholder="Kullanıcı Adı" required onChange={handleChange} />
      <input name="password" type="password" placeholder="Şifre" required onChange={handleChange} />

      <select name="favorite_artist" required onChange={handleChange}>
        <option value="">Sanatçı seçin</option>
        <option value="Adele">Adele</option>
        <option value="Pharrell Williams">Pharrell Williams</option>
        <option value="Debussy">Debussy</option>
        <option value="Survivor">Survivor</option>
        <option value="Coldplay">Coldplay</option>
        <option value="Kanye West">Kanye West</option>
        <option value="Bruno Mars">Bruno Mars</option>
        <option value="Marconi Union">Marconi Union</option>
      </select>

      <select name="favorite_genre" required onChange={handleChange}>
        <option value="">Tür seçin</option>
        <option value="Pop">Pop</option>
        <option value="Classical">Classical</option>
        <option value="Rock">Rock</option>
        <option value="Hip-Hop">Hip-Hop</option>
        <option value="Funk">Funk</option>
        <option value="Ambient">Ambient</option>
      </select>

      <button type="submit">Kayıt Ol</button>
    </form>
  )
}

export default RegisterForm
