import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'

interface AuthState {
  token: string | null
  username: string | null
  loading: boolean
  error: string | null
}

const initialState: AuthState = {
  token: null,
  username: null,
  loading: false,
  error: null,
}

// LOGIN ACTION
export const loginUser = createAsyncThunk(
  'auth/loginUser',
  async (
    credentials: { username: string; password: string },
    { rejectWithValue }
  ) => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/auth/login',
        credentials
      )
      return response.data
    } catch (err: any) {
      return rejectWithValue(err.response.data.message || 'Login failed')
    }
  }
)

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.token = null
      state.username = null
      localStorage.removeItem('token')
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false
        state.token = action.payload.access_token
        state.username = action.meta.arg.username
        localStorage.setItem('token', action.payload.access_token)
      })      
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload as string
      })
  },
})

export const { logout } = authSlice.actions
export default authSlice.reducer
