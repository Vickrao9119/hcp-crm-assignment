import { useEffect, useState } from 'react';
import { Box, Typography } from '@mui/material';
import { dashboardApi } from '../api/endpoints';
import AnalyticsCharts from '../components/AnalyticsCharts';
import Loading from '../components/Loading';

export default function Analytics() {
  const [data, setData] = useState(null);
  const [monthly, setMonthly] = useState([]);

  useEffect(() => {
    Promise.all([dashboardApi.analytics(), dashboardApi.get()]).then(([a, d]) => {
      setData(a.data);
      setMonthly(d.data.monthly_chart);
    });
  }, []);

  if (!data) return <Loading label="Loading analytics..." />;

  return (
    <Box>
      <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif', mb: 2 }}>Analytics</Typography>
      <AnalyticsCharts monthlyChart={monthly} byPriority={data.by_priority} bySpecialization={data.by_specialization} />
    </Box>
  );
}
