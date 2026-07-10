/**
 * Login page — hero pulse-line animation + credentials form.
 * Signature visual: the ECG/pulse-line motif used across the app.
 */
import { useForm } from 'react-hook-form';
import { Box, Paper, Typography, TextField, Button, Alert } from '@mui/material';
import { motion } from 'framer-motion';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { login } from '../store/slices/authSlice';

export default function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { status, error } = useSelector((s) => s.auth);
  const { register, handleSubmit } = useForm({ defaultValues: { email: 'admin@hcpcrm.com', password: 'Admin@123' } });

  const onSubmit = async (values) => {
    const result = await dispatch(login(values));
    if (login.fulfilled.match(result)) navigate('/dashboard');
  };

  return (
    <Box
      sx={{
        minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: 'linear-gradient(160deg, #0E3550 0%, #164B70 60%, #1B5C88 100%)', p: 2,
      }}
    >
      <Paper sx={{ p: 5, width: 420, borderRadius: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <svg width="64" height="24" viewBox="0 0 120 40" style={{ margin: '0 auto', display: 'block' }}>
            <motion.path
              d="M0 20 H30 L38 5 L48 35 L56 20 H120"
              fill="none" stroke="#2FB6A6" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"
              initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.4 }}
            />
          </svg>
          <Typography variant="h4" sx={{ fontFamily: '"Fraunces", serif', mt: 1 }}>AI First CRM</Typography>
          <Typography variant="body2" color="text.secondary">HCP Interaction Module</Typography>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField label="Email" type="email" {...register('email', { required: true })} />
          <TextField label="Password" type="password" {...register('password', { required: true })} />
          <Button type="submit" variant="contained" size="large" disabled={status === 'loading'}>
            {status === 'loading' ? 'Signing in...' : 'Sign In'}
          </Button>
        </Box>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2, textAlign: 'center' }}>
          Demo: admin@hcpcrm.com / Admin@123
        </Typography>
      </Paper>
    </Box>
  );
}
