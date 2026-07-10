import { Box, Paper, Typography, Chip, Stack } from '@mui/material';
import { motion } from 'framer-motion';

export default function ChatBubble({ role, text, entities, savedInteraction }) {
  const isUser = role === 'user';
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', marginBottom: 12 }}
    >
      <Paper
        elevation={0}
        sx={{
          p: 1.5,
          maxWidth: '75%',
          bgcolor: isUser ? 'primary.main' : 'background.paper',
          color: isUser ? '#fff' : 'text.primary',
          border: isUser ? 'none' : '1px solid',
          borderColor: 'divider',
          borderRadius: 3,
          borderBottomRightRadius: isUser ? 4 : 12,
          borderBottomLeftRadius: isUser ? 12 : 4,
        }}
      >
        <Typography variant="body2">{text}</Typography>
        {entities && (
          <Stack direction="row" flexWrap="wrap" gap={0.5} sx={{ mt: 1 }}>
            {entities.doctor && <Chip size="small" label={`Doctor: ${entities.doctor}`} />}
            {entities.hospital && <Chip size="small" label={`Hospital: ${entities.hospital}`} />}
            {entities.products?.map((p) => <Chip key={p} size="small" label={p} color="secondary" />)}
            {savedInteraction && <Chip size="small" label="Saved ✓" color="success" />}
          </Stack>
        )}
      </Paper>
    </motion.div>
  );
}
