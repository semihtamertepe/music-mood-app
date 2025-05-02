import { useAppSelector } from '../app/hooks'
import UserList from '../features/users/components/UserList'
import ChatRoom from '../features/chat/components/ChatRoom'
import { useState } from 'react'

const ChatPage = () => {
  const currentUser = useAppSelector((state) => state.auth.username)
  const [selectedUser, setSelectedUser] = useState<string | null>(null)

  if (!currentUser) return <p>Giriş yapılmadı</p>

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ width: '30%', borderRight: '1px solid gray' }}>
        <UserList onSelectUser={setSelectedUser} />
      </div>
      <div style={{ width: '70%', padding: '1rem' }}>
        {selectedUser ? (
          <ChatRoom currentUser={currentUser} targetUser={selectedUser} />
        ) : (
          <p>Mesajlaşmak için bir kullanıcı seçin</p>
        )}
      </div>
    </div>
  )
}

export default ChatPage
