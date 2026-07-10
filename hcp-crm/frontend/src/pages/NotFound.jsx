import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function NotFound() {
  const navigate = useNavigate();
  return (
    <Box sx={{ textAlign: 'center', py: 10 }}>
      <Typography variant="h1" sx={{ fontFamily: '"Fraunces", serif', fontSize: 96, color: 'primary.main' }}>404</Typography>
      <Typography variant="h6" sx={{ mb: 3 }}>This page took a wrong turn at the clinic.</Typography>
      <Button variant="contained" onClick={() => navigate('/dashboard')}>Back to Dashboard</Button>
    </Box>
  );
}
