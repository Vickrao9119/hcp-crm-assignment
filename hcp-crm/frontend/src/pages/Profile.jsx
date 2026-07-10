import { useSelector } from 'react-redux';
import { Box, Typography, Grid } from '@mui/material';
import ProfileMenu from '../components/ProfileMenu';

export default function Profile() {
  const user = useSelector((s) => s.auth.user);
  return (
    <Box>
      <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif', mb: 2 }}>Profile</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <ProfileMenu user={user} />
        </Grid>
      </Grid>
    </Box>
  );
}
