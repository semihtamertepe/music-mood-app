import { createSlice } from '@reduxjs/toolkit'

interface ChatState {
  currentRoom: string | null
}

const initialState: ChatState = {
  currentRoom: null,
}

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    setRoom: (state, action) => {
      state.currentRoom = action.payload
    },
  },
})

export const { setRoom } = chatSlice.actions
export default chatSlice.reducer
