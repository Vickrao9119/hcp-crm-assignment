import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Grid, Card, CardContent, Chip, List, ListItem, ListItemText } from '@mui/material';
import dayjs from 'dayjs';
import { doctorApi, interactionApi } from '../api/endpoints';
import Loading from '../components/Loading';
import EmptyState from '../components/EmptyState';
import PageHeader from '../components/PageHeader';

export default function DoctorProfile() {
  const { id } = useParams();
  const [doctor, setDoctor] = useState(null);
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([doctorApi.get(id), interactionApi.list({ doctor_id: id, page_size: 20 })])
      .then(([dRes, iRes]) => {
        setDoctor(dRes.data);
        setInteractions(iRes.data.items);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Loading label="Loading profile..." />;
  if (!doctor) return <EmptyState title="Doctor not found" />;

  return (
    <Box>
      <PageHeader title={doctor.name} />
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="text.secondary">Specialization</Typography>
              <Typography sx={{ mb: 1.5 }}>{doctor.specialization || '—'}</Typography>
              <Typography variant="subtitle2" color="text.secondary">City</Typography>
              <Typography sx={{ mb: 1.5 }}>{doctor.city || '—'}</Typography>
              <Typography variant="subtitle2" color="text.secondary">Phone</Typography>
              <Typography sx={{ mb: 1.5 }}>{doctor.phone || '—'}</Typography>
              <Typography variant="subtitle2" color="text.secondary">Email</Typography>
              <Typography>{doctor.email || '—'}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Interaction Timeline</Typography>
              {interactions.length ? (
                <List>
                  {interactions.map((i) => (
                    <ListItem key={i.id} divider alignItems="flex-start">
                      <ListItemText
                        primary={dayjs(i.meeting_date).format('DD MMM YYYY, hh:mm A')}
                        secondary={
                          <>
                            {i.products_discussed && <Chip size="small" sx={{ mr: 1, mb: 0.5 }} label={i.products_discussed} />}
                            <Chip size="small" sx={{ mr: 1, mb: 0.5 }} label={i.priority} color="secondary" />
                            <Typography variant="body2" color="text.secondary">{i.notes}</Typography>
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              ) : <EmptyState title="No interactions yet" />}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
