import { Box } from '@mui/material';
import ChatWindow from '../components/ChatWindow';
import PageHeader from '../components/PageHeader';

export default function AIChat() {
  return (
    <Box>
      <PageHeader title="AI Chat" />
      <ChatWindow />
    </Box>
  );
}
