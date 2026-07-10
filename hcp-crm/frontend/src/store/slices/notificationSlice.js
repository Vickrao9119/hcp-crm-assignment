import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { notificationApi } from '../../api/endpoints';

export const fetchNotifications = createAsyncThunk('notifications/fetch', async () => {
  const { data } = await notificationApi.list();
  return data;
});

const notificationSlice = createSlice({
  name: 'notifications',
  initialState: { items: [], unreadCount: 0, status: 'idle' },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(fetchNotifications.fulfilled, (state, action) => {
      state.items = action.payload.items;
      state.unreadCount = action.payload.unread_count;
      state.status = 'succeeded';
    });
  },
});

export default notificationSlice.reducer;
