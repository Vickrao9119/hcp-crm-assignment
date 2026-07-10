import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { doctorApi } from '../../api/endpoints';

export const fetchDoctors = createAsyncThunk('doctors/fetch', async (params) => {
  const { data } = await doctorApi.list(params);
  return data;
});

const doctorSlice = createSlice({
  name: 'doctors',
  initialState: { items: [], total: 0, status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDoctors.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchDoctors.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload.items;
        state.total = action.payload.total;
      })
      .addCase(fetchDoctors.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export default doctorSlice.reducer;
