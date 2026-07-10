/**
 * Primary navigation sidebar. Collapses to icon-only on tablet and becomes
 * a drawer on mobile (controlled by the `open`/`onClose` props from Navbar).
 */
import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Box, Typography, useMediaQuery } from '@mui/material';
import { NavLink, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import {
  MdDashboard, MdLocalHospital, MdEditNote, MdChat, MdHistory,
  MdBarChart, MdNotifications, MdSettings, MdLogout,
} from 'react-icons/md';
import { logout } from '../store/slices/authSlice';

const NAV_ITEMS = [
  { label: 'Dashboard', icon: <MdDashboard />, to: '/dashboard' },
  { label: 'Doctors', icon: <MdLocalHospital />, to: '/doctors' },
  { label: 'Log Interaction', icon: <MdEditNote />, to: '/log-interaction' },
  { label: 'AI Chat', icon: <MdChat />, to: '/ai-chat' },
  { label: 'History', icon: <MdHistory />, to: '/history' },
  { label: 'Analytics', icon: <MdBarChart />, to: '/analytics' },
  { label: 'Notifications', icon: <MdNotifications />, to: '/notifications' },
  { label: 'Settings', icon: <MdSettings />, to: '/settings' },
];

const drawerWidth = 248;

export default function Sidebar({ mobileOpen, onClose }) {
  const isMobile = useMediaQuery('(max-width:900px)');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const content = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Box sx={{ px: 3, py: 2.5, display: 'flex', alignItems: 'center', gap: 1 }}>
        <svg width="28" height="28" viewBox="0 0 28 28">
          <path d="M2 14 H9 L12 4 L16 24 L19 14 H26" fill="none" stroke="#2FB6A6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <Typography variant="h6" sx={{ fontFamily: '"Fraunces", serif', fontWeight: 600 }}>
          AI CRM
        </Typography>
      </Box>

      <List sx={{ flexGrow: 1, px: 1.5 }}>
        {NAV_ITEMS.map((item) => (
          <ListItemButton
            key={item.to}
            component={NavLink}
            to={item.to}
            onClick={isMobile ? onClose : undefined}
            sx={{
              borderRadius: 2,
              mb: 0.5,
              '&.active': {
                bgcolor: 'primary.main',
                color: '#fff',
                '& .MuiListItemIcon-root': { color: '#fff' },
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 36 }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>

      <List sx={{ px: 1.5, pb: 2 }}>
        <ListItemButton
          sx={{ borderRadius: 2 }}
          onClick={() => {
            dispatch(logout());
            navigate('/login');
          }}
        >
          <ListItemIcon sx={{ minWidth: 36 }}><MdLogout /></ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItemButton>
      </List>
    </Box>
  );

  if (isMobile) {
    return (
      <Drawer open={mobileOpen} onClose={onClose} ModalProps={{ keepMounted: true }}>
        <Box sx={{ width: drawerWidth }}>{content}</Box>
      </Drawer>
    );
  }

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box', border: 'none' },
      }}
    >
      {content}
    </Drawer>
  );
}
