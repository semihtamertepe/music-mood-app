import { createSlice } from '@reduxjs/toolkit'

interface UserState {
  list: string[]
}

const initialState: UserState = {
  list: [],
}

const userSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    setUsers: (state, action) => {
      state.list = action.payload
    },
  },
})

export const { setUsers } = userSlice.actions
export default userSlice.reducer
