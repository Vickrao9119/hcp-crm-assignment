import { Grid, Card, CardContent, Typography, Box } from '@mui/material';
import { MdLocalHospital, MdEventAvailable, MdPendingActions, MdCheckCircle, MdCalendarMonth } from 'react-icons/md';

const CARD_CONFIG = [
  { key: 'total_doctors', label: 'Total Doctors', icon: <MdLocalHospital />, color: '#164B70' },
  { key: 'todays_meetings', label: "Today's Meetings", icon: <MdEventAvailable />, color: '#2FB6A6' },
  { key: 'pending_followups', label: 'Pending Follow-ups', icon: <MdPendingActions />, color: '#E0A63E' },
  { key: 'completed_meetings', label: 'Completed Meetings', icon: <MdCheckCircle />, color: '#3E7CA6' },
  { key: 'monthly_meetings', label: 'Monthly Meetings', icon: <MdCalendarMonth />, color: '#D65656' },
];

export default function DashboardCards({ stats }) {
  return (
    <Grid container spacing={2}>
      {CARD_CONFIG.map((cfg) => (
        <Grid item xs={12} sm={6} md={2.4} key={cfg.key}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                <Box sx={{ color: cfg.color, fontSize: 26 }}>{cfg.icon}</Box>
                <Box>
                  <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif' }}>
                    {stats?.[cfg.key] ?? '—'}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">{cfg.label}</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}
