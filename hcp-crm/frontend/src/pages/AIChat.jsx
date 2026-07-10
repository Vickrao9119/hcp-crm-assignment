import { Box, Typography } from '@mui/material';
import ChatWindow from '../components/ChatWindow';

export default function AIChat() {
  return (
    <Box>
      <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif', mb: 2 }}>AI Chat</Typography>
      <ChatWindow />
    </Box>
  );
}
