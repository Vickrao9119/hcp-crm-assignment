import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { dashboardApi } from '../../api/endpoints';
import { addAsyncCases } from '../thunkHelpers';

export const fetchDashboard = createAsyncThunk('dashboard/fetch', async () => {
  const { data } = await dashboardApi.get();
  return data;
});

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState: { stats: null, recentActivity: [], upcomingFollowups: [], monthlyChart: [], status: 'idle' },
  reducers: {},
  extraReducers: (builder) => {
    addAsyncCases(builder, fetchDashboard, {
      fulfilled: (state, action) => {
        state.stats = action.payload.stats;
        state.recentActivity = action.payload.recent_activity;
        state.upcomingFollowups = action.payload.upcoming_followups;
        state.monthlyChart = action.payload.monthly_chart;
      },
    });
  },
});

export default dashboardSlice.reducer;
