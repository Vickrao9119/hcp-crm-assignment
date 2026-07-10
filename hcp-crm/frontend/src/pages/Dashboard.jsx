import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Grid, Card, CardContent, Typography, List, ListItem, ListItemText, Box } from '@mui/material';
import dayjs from 'dayjs';
import { fetchDashboard } from '../store/slices/dashboardSlice';
import DashboardCards from '../components/DashboardCards';
import Loading from '../components/Loading';
import EmptyState from '../components/EmptyState';

export default function Dashboard() {
  const dispatch = useDispatch();
  const { stats, recentActivity, upcomingFollowups, status } = useSelector((s) => s.dashboard);

  useEffect(() => { dispatch(fetchDashboard()); }, [dispatch]);

  if (status === 'loading' && !stats) return <Loading label="Loading dashboard..." />;

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2, fontFamily: '"Fraunces", serif' }}>Dashboard</Typography>
      <DashboardCards stats={stats} />

      <Grid container spacing={2} sx={{ mt: 1 }}>
        <Grid item xs={12} md={7}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Recent Activity</Typography>
              {recentActivity?.length ? (
                <List>
                  {recentActivity.map((a) => (
                    <ListItem key={a.id} divider>
                      <ListItemText primary={a.notes || 'Interaction logged'} secondary={dayjs(a.created_at).format('DD MMM, hh:mm A')} />
                    </ListItem>
                  ))}
                </List>
              ) : <EmptyState title="No recent activity" />}
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={5}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Upcoming Follow-ups</Typography>
              {upcomingFollowups?.length ? (
                <List>
                  {upcomingFollowups.map((f) => (
                    <ListItem key={f.id} divider>
                      <ListItemText primary={`Follow-up`} secondary={dayjs(f.due_date).format('DD MMM YYYY, hh:mm A')} />
                    </ListItem>
                  ))}
                </List>
              ) : <EmptyState title="No upcoming follow-ups" />}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
