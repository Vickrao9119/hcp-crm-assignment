import { Box, Typography, Button } from '@mui/material';

export default function EmptyState({ title = 'Nothing here yet', subtitle, actionLabel, onAction, icon }) {
  return (
    <Box sx={{ textAlign: 'center', py: 6 }}>
      {icon}
      <Typography variant="h6" sx={{ mt: 1 }}>{title}</Typography>
      {subtitle && <Typography variant="body2" color="text.secondary">{subtitle}</Typography>}
      {actionLabel && (
        <Button variant="contained" sx={{ mt: 2 }} onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </Box>
  );
}
