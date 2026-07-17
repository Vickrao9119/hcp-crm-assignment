import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { authApi } from '../../api/endpoints';
import { addAsyncCases } from '../thunkHelpers';

export const login = createAsyncThunk('auth/login', async (credentials, { rejectWithValue }) => {
  try {
    const { data } = await authApi.login(credentials);
    localStorage.setItem('access_token', data.access_token);
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'Login failed');
  }
});

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: localStorage.getItem('access_token') || null,
    status: 'idle',
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
      localStorage.removeItem('access_token');
    },
  },
  extraReducers: (builder) => {
    addAsyncCases(builder, login, {
      pending: (state) => { state.error = null; },
      fulfilled: (state, action) => {
        state.user = action.payload.user;
        state.token = action.payload.access_token;
      },
      rejected: (state, action) => { state.error = action.payload; },
    });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
