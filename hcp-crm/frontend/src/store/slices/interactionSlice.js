import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { interactionApi } from '../../api/endpoints';

export const fetchInteractions = createAsyncThunk('interactions/fetch', async (params) => {
  const { data } = await interactionApi.list(params);
  return data;
});

export const createInteraction = createAsyncThunk(
  'interactions/create',
  async (payload, { rejectWithValue }) => {
    try {
      const { data } = await interactionApi.create(payload);
      return data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to create interaction');
    }
  }
);

const interactionSlice = createSlice({
  name: 'interactions',
  initialState: { items: [], total: 0, status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload.items;
        state.total = action.payload.total;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error?.message || 'Failed to load interactions';
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.error = null;
        state.items.unshift(action.payload);
      })
      .addCase(createInteraction.rejected, (state, action) => {
        state.error = action.payload || action.error?.message || 'Failed to create interaction';
      });
  },
});

export default interactionSlice.reducer;
