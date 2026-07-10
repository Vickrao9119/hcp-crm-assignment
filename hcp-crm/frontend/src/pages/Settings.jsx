import { useDispatch, useSelector } from 'react-redux';
import { Box, Typography, Paper, FormControlLabel, Switch, Divider } from '@mui/material';
import { toggleTheme } from '../store/slices/themeSlice';

export default function Settings() {
  const dispatch = useDispatch();
  const mode = useSelector((s) => s.theme.mode);

  return (
    <Box>
      <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif', mb: 2 }}>Settings</Typography>
      <Paper sx={{ p: 3, maxWidth: 480 }}>
        <Typography variant="subtitle1" gutterBottom>Appearance</Typography>
        <FormControlLabel
          control={<Switch checked={mode === 'dark'} onChange={() => dispatch(toggleTheme())} />}
          label="Dark Mode"
        />
        <Divider sx={{ my: 2 }} />
        <Typography variant="subtitle1" gutterBottom>Notifications</Typography>
        <FormControlLabel control={<Switch defaultChecked />} label="Email alerts for follow-ups" />
        <FormControlLabel control={<Switch defaultChecked />} label="In-app notifications" />
      </Paper>
    </Box>
  );
}
