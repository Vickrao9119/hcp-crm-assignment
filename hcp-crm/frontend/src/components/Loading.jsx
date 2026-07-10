/**
 * App-wide loading indicator: an animated "pulse line" (ECG-style),
 * echoing the CRM's medical theme instead of a generic spinner.
 */
import { Box, Typography } from '@mui/material';
import { motion } from 'framer-motion';

export default function Loading({ label = 'Loading...' }) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1, py: 6 }}>
      <svg width="120" height="40" viewBox="0 0 120 40">
        <motion.path
          d="M0 20 H30 L38 5 L48 35 L56 20 H120"
          fill="none"
          stroke="var(--pulse-color, #2FB6A6)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          initial={{ pathLength: 0, opacity: 0.4 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ duration: 1.1, repeat: Infinity, repeatType: 'loop' }}
        />
      </svg>
      <Typography variant="body2" color="text.secondary">{label}</Typography>
    </Box>
  );
}
