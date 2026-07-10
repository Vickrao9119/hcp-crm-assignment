import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { interactionApi } from '../../api/endpoints';

export const fetchInteractions = createAsyncThunk('interactions/fetch', async (params) => {
  const { data } = await interactionApi.list(params);
  return data;
});

export const createInteraction = createAsyncThunk('interactions/create', async (payload) => {
  const { data } = await interactionApi.create(payload);
  return data;
});

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
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.items.unshift(action.payload);
      });
  },
});

export default interactionSlice.reducer;
