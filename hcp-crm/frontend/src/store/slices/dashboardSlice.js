import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { dashboardApi } from '../../api/endpoints';

export const fetchDashboard = createAsyncThunk('dashboard/fetch', async () => {
  const { data } = await dashboardApi.get();
  return data;
});

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState: { stats: null, recentActivity: [], upcomingFollowups: [], monthlyChart: [], status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboard.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(fetchDashboard.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.stats = action.payload.stats;
        state.recentActivity = action.payload.recent_activity;
        state.upcomingFollowups = action.payload.upcoming_followups;
        state.monthlyChart = action.payload.monthly_chart;
      })
      .addCase(fetchDashboard.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error?.message || 'Failed to load dashboard';
      });
  },
});

export default dashboardSlice.reducer;
