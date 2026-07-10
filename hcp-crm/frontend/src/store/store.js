import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import doctorReducer from './slices/doctorSlice';
import interactionReducer from './slices/interactionSlice';
import chatReducer from './slices/chatSlice';
import dashboardReducer from './slices/dashboardSlice';
import themeReducer from './slices/themeSlice';
import notificationReducer from './slices/notificationSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    doctors: doctorReducer,
    interactions: interactionReducer,
    chat: chatReducer,
    dashboard: dashboardReducer,
    theme: themeReducer,
    notifications: notificationReducer,
  },
});
