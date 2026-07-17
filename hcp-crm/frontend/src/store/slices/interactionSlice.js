import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { interactionApi } from '../../api/endpoints';
import { addAsyncCases } from '../thunkHelpers';

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
    addAsyncCases(builder, fetchInteractions, {
      fulfilled: (state, action) => {
        state.items = action.payload.items;
        state.total = action.payload.total;
      },
    });
    builder.addCase(createInteraction.fulfilled, (state, action) => {
      state.items.unshift(action.payload);
    });
  },
});

export default interactionSlice.reducer;
