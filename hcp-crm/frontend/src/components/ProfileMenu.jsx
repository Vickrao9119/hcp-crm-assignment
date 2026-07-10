/**
 * Standalone profile summary card (used on the Profile page — distinct
 * from the Navbar's dropdown ProfileMenu-in-a-Menu, which lives in Navbar.jsx).
 */
import { Card, CardContent, Avatar, Typography, Box, Chip } from '@mui/material';

export default function ProfileMenu({ user }) {
  if (!user) return null;
  return (
    <Card>
      <CardContent sx={{ textAlign: 'center', py: 4 }}>
        <Avatar sx={{ width: 84, height: 84, mx: 'auto', bgcolor: 'primary.main', fontSize: 32 }}>
          {user.full_name?.[0]}
        </Avatar>
        <Typography variant="h6" sx={{ mt: 2 }}>{user.full_name}</Typography>
        <Typography variant="body2" color="text.secondary">{user.email}</Typography>
        <Chip label={user.role} size="small" color="secondary" sx={{ mt: 1 }} />
      </CardContent>
    </Card>
  );
}
