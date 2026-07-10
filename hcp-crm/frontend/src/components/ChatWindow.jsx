/**
 * ChatGPT-style AI chat window used on the AI Chat page and inside the
 * Log Interaction "AI Chat" tab.
 */
import { useState, useRef, useEffect } from 'react';
import { Box, TextField, IconButton, Paper } from '@mui/material';
import { MdSend } from 'react-icons/md';
import { useDispatch, useSelector } from 'react-redux';
import { addUserMessage, sendChatMessage } from '../store/slices/chatSlice';
import ChatBubble from './ChatBubble';
import Loading from './Loading';

export default function ChatWindow() {
  const dispatch = useDispatch();
  const { messages, status } = useSelector((s) => s.chat);
  const [input, setInput] = useState('');
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, status]);

  const handleSend = () => {
    if (!input.trim()) return;
    dispatch(addUserMessage(input));
    dispatch(sendChatMessage({ message: input }));
    setInput('');
  };

  return (
    <Paper sx={{ display: 'flex', flexDirection: 'column', height: '70vh', p: 2 }}>
      <Box sx={{ flexGrow: 1, overflowY: 'auto', px: 1 }}>
        {messages.length === 0 && (
          <Box sx={{ color: 'text.secondary', textAlign: 'center', mt: 4 }}>
            Try: "Today I visited Dr Sharma at Apollo Hospital. Discussed diabetes medicines.
            Doctor requested more samples. Schedule follow-up next Monday."
          </Box>
        )}
        {messages.map((m, i) => (
          <ChatBubble key={i} role={m.role} text={m.text} entities={m.entities} savedInteraction={m.savedInteraction} />
        ))}
        {status === 'loading' && <Loading label="Thinking..." />}
        <div ref={endRef} />
      </Box>
      <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
        <TextField
          fullWidth
          placeholder="Describe your visit..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <IconButton color="primary" onClick={handleSend}><MdSend /></IconButton>
      </Box>
    </Paper>
  );
}
