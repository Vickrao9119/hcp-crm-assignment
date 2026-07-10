import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Typography, Paper } from '@mui/material';
import { fetchNotifications } from '../store/slices/notificationSlice';
import { notificationApi } from '../api/endpoints';
import NotificationPanel from '../components/NotificationPanel';

export default function Notifications() {
  const dispatch = useDispatch();
  const { items } = useSelector((s) => s.notifications);

  useEffect(() => { dispatch(fetchNotifications()); }, [dispatch]);

  const handleMarkRead = async (id) => {
    await notificationApi.markRead(id);
    dispatch(fetchNotifications());
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif', mb: 2 }}>Notifications</Typography>
      <Paper sx={{ p: 2 }}>
        <NotificationPanel items={items} onMarkRead={handleMarkRead} />
      </Paper>
    </Box>
  );
}
