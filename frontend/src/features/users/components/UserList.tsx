import { useEffect, useState } from 'react'
import { fetchAllUsers } from '../services/userAPI'
import { useAppSelector } from '../../../app/hooks'

interface Props {
  onSelectUser: (username: string) => void
}

const UserList = ({ onSelectUser }: Props) => {
  const [users, setUsers] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)
  const currentUsername = useAppSelector((state) => state.auth.username)
  const token = useAppSelector((state) => state.auth.token)

  useEffect(() => {
    const loadUsers = async () => {
      try {
        if (!token) return
        const data = await fetchAllUsers(token)
        const usernames = data
          .map((u: any) => u.username)
          .filter((u: string) => u !== currentUsername) // kendini listeleme
        setUsers(usernames)
      } catch (err) {
        setError('Kullanıcılar yüklenemedi.')
      }
    }
    loadUsers()
  }, [token, currentUsername])

  return (
    <div>
      <h3>Kullanıcılar</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {users.map((username) => (
          <li
            key={username}
            onClick={() => onSelectUser(username)}
            style={{ cursor: 'pointer', padding: '0.5rem', borderBottom: '1px solid #ccc' }}
          >
            {username}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default UserList
