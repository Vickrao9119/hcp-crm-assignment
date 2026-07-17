import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { doctorApi } from '../../api/endpoints';
import { addAsyncCases } from '../thunkHelpers';

export const fetchDoctors = createAsyncThunk('doctors/fetch', async (params) => {
  const { data } = await doctorApi.list(params);
  return data;
});

const doctorSlice = createSlice({
  name: 'doctors',
  initialState: { items: [], total: 0, status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    addAsyncCases(builder, fetchDoctors, {
      fulfilled: (state, action) => {
        state.items = action.payload.items;
        state.total = action.payload.total;
      },
      rejected: (state, action) => { state.error = action.error.message; },
    });
  },
});

export default doctorSlice.reducer;
