import { configureStore } from '@reduxjs/toolkit'
import authReducer from '../features/auth/slices/authSlice'
import userReducer from '../features/users/slices/userSlice'
import chatReducer from '../features/chat/slices/chatSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    users: userReducer,
    chat: chatReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
