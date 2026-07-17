import { useSelector } from 'react-redux';
import { Box, Grid } from '@mui/material';
import ProfileMenu from '../components/ProfileMenu';
import PageHeader from '../components/PageHeader';

export default function Profile() {
  const user = useSelector((s) => s.auth.user);
  return (
    <Box>
      <PageHeader title="Profile" />
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <ProfileMenu user={user} />
        </Grid>
      </Grid>
    </Box>
  );
}
