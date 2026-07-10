import { Card, CardContent, Typography, Box, Chip, IconButton } from '@mui/material';
import { MdLocalHospital, MdPhone, MdEmail, MdMoreVert } from 'react-icons/md';
import { useNavigate } from 'react-router-dom';

export default function DoctorCard({ doctor }) {
  const navigate = useNavigate();
  return (
    <Card sx={{ cursor: 'pointer', height: '100%' }} onClick={() => navigate(`/doctors/${doctor.id}`)}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Typography variant="h6">{doctor.name}</Typography>
          <IconButton size="small" onClick={(e) => e.stopPropagation()}><MdMoreVert /></IconButton>
        </Box>
        {doctor.specialization && <Chip size="small" label={doctor.specialization} color="secondary" sx={{ mt: 0.5 }} />}
        <Box sx={{ mt: 1.5, display: 'flex', flexDirection: 'column', gap: 0.5 }}>
          {doctor.city && (
            <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <MdLocalHospital /> {doctor.city}
            </Typography>
          )}
          {doctor.phone && (
            <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <MdPhone /> {doctor.phone}
            </Typography>
          )}
          {doctor.email && (
            <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <MdEmail /> {doctor.email}
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}
