import { useEffect, useRef, useState } from 'react'
import axios from 'axios'
import { connectMQTT } from '../services/mqttClient'
import RecommendationButton from '../../music/components/RecommendationButton'

interface Props {
  currentUser: string
  targetUser: string
}

interface Message {
  room_id: string
  sender: string
  receiver: string
  message: string
  timestamp: string
}

const ChatRoom = ({ currentUser, targetUser }: Props) => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const clientRef = useRef<any>(null)
  const topic = `chat/${[currentUser, targetUser].sort().join('_')}`
  const room_id = `${[currentUser, targetUser].sort().join('_')}`
  const chatEndRef = useRef<HTMLDivElement>(null)
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  // 1. Geçmiş mesajları API'den çek
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/chat/get_messages`, {
          params: { room_id , limit:50 ,offset:0},
        })
        setMessages(res.data.messages)
        scrollToBottom()
      } catch (err) {
        console.error('Geçmiş mesajlar çekilemedi:', err)
      }
    }
    fetchHistory()
  }, [room_id])

  // MQTT ile anlık mesajları dinlenmesi
  useEffect(() => {
    const client = connectMQTT()
    clientRef.current = client

    client.on('connect', () => {
      client.subscribe(topic)
      console.log(`Subscribed to ${topic}`)
    })

    client.on('message', (t: string, payload: Buffer) => {
      if (t === topic) {
        try {
          const msg: Message = JSON.parse(payload.toString())
          setMessages((prev) => [...prev, msg])
        } catch (err) {
          console.error("Mesaj çözümleme hatası:", err)
        }
      }
    })

    return () => {
      client.unsubscribe(topic)
      client.end()
    }
  }, [topic])

  // 3. Yeni mesaj gönder
  const sendMessage = () => {
    if (!input.trim()) return
    const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ')
    const newMessage: Message = {
      room_id,
      sender: currentUser,
      receiver: targetUser,
      message: input,
      timestamp,
    }

    clientRef.current?.publish(topic, JSON.stringify(newMessage))
    setInput('')
  }

  return (
    <div>
      <h3>{targetUser} ile Sohbet</h3>
      <RecommendationButton currentUser={currentUser} targetUser={targetUser} />

      <div
        style={{
          height: 300,
          overflowY: 'auto',
          border: '1px solid #ccc',
          padding: '0.5rem',
          marginBottom: '1rem',
        }}
      >
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === currentUser ? 'right' : 'left' }}>
            <div>
              <b>{msg.sender}</b>: {msg.message}
            </div>
            <small>{new Date(msg.timestamp).toLocaleTimeString()}</small>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <input
        type="text"
        placeholder="Mesaj..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        style={{ width: '80%', marginRight: '0.5rem' }}
      />
      <button onClick={sendMessage}>Gönder</button>
    </div>
  )
}

export default ChatRoom
