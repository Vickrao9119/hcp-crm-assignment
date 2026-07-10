import { Box, Typography, Button } from '@mui/material';
import { MdErrorOutline } from 'react-icons/md';

export default function ErrorComponent({ message = 'Something went wrong.', onRetry }) {
  return (
    <Box sx={{ textAlign: 'center', py: 6 }}>
      <MdErrorOutline size={40} color="#D65656" />
      <Typography variant="h6" sx={{ mt: 1 }}>{message}</Typography>
      {onRetry && (
        <Button variant="outlined" sx={{ mt: 2 }} onClick={onRetry}>
          Try again
        </Button>
      )}
    </Box>
  );
}
