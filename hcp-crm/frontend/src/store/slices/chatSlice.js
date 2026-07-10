import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { chatApi } from '../../api/endpoints';

export const sendChatMessage = createAsyncThunk('chat/send', async (payload) => {
  const { data } = await chatApi.send(payload);
  return data;
});

const chatSlice = createSlice({
  name: 'chat',
  initialState: { messages: [], sessionId: null, status: 'idle' },
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({ role: 'user', text: action.payload });
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.sessionId = action.payload.session_id;
        state.messages.push({
          role: 'assistant',
          text: action.payload.reply,
          entities: action.payload.extracted_entities,
          savedInteraction: action.payload.interaction_saved,
        });
      })
      .addCase(sendChatMessage.rejected, (state) => {
        state.status = 'failed';
        state.messages.push({ role: 'assistant', text: 'Something went wrong. Please try again.' });
      });
  },
});

export const { addUserMessage } = chatSlice.actions;
export default chatSlice.reducer;
