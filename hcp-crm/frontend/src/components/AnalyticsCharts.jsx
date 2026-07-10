import { Grid, Card, CardContent, Typography } from '@mui/material';
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, LineChart, Line, CartesianGrid,
} from 'recharts';

const COLORS = ['#164B70', '#2FB6A6', '#E0A63E', '#D65656', '#3E7CA6'];

export default function AnalyticsCharts({ monthlyChart = [], byPriority = [], bySpecialization = [] }) {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>Meetings Trend</Typography>
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={monthlyChart}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="meetings" stroke="#164B70" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>By Priority</Typography>
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={byPriority} dataKey="value" nameKey="label" outerRadius={90} label>
                  {byPriority.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>By Specialization</Typography>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={bySpecialization}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#2FB6A6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
