import { Box, Typography } from '@mui/material';

/**
 * Standard page title using the Fraunces display font. Pass `actions` to render
 * controls (search, buttons, filters) on the right of a flex header row.
 */
export default function PageHeader({ title, actions, sx }) {
  if (actions) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, flexWrap: 'wrap', gap: 1, ...sx }}>
        <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif' }}>{title}</Typography>
        {actions}
      </Box>
    );
  }
  return (
    <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif', mb: 2, ...sx }}>{title}</Typography>
  );
}
