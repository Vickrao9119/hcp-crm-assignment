/**
 * Top navbar: global search, dark-mode toggle, notifications, profile menu.
 */
import { useState } from 'react';
import {
  AppBar, Toolbar, IconButton, InputBase, Box, Badge, Avatar, Menu, MenuItem, useMediaQuery,
} from '@mui/material';
import { MdMenu, MdSearch, MdDarkMode, MdLightMode, MdNotificationsNone } from 'react-icons/md';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { toggleTheme } from '../store/slices/themeSlice';
import { logout } from '../store/slices/authSlice';

export default function Navbar({ onMenuClick }) {
  const isMobile = useMediaQuery('(max-width:900px)');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const mode = useSelector((s) => s.theme.mode);
  const user = useSelector((s) => s.auth.user);
  const unreadCount = useSelector((s) => s.notifications.unreadCount);
  const [anchorEl, setAnchorEl] = useState(null);

  return (
    <AppBar
      position="sticky"
      elevation={0}
      color="transparent"
      sx={{ backdropFilter: 'blur(8px)', borderBottom: '1px solid', borderColor: 'divider' }}
    >
      <Toolbar sx={{ gap: 1.5 }}>
        {isMobile && (
          <IconButton onClick={onMenuClick}><MdMenu /></IconButton>
        )}

        <Box
          sx={{
            display: 'flex', alignItems: 'center', gap: 1, bgcolor: 'background.paper',
            border: '1px solid', borderColor: 'divider', borderRadius: 2, px: 1.5, py: 0.5,
            flexGrow: 1, maxWidth: 420,
          }}
        >
          <MdSearch />
          <InputBase placeholder="Search doctors, interactions..." fullWidth />
        </Box>

        <Box sx={{ flexGrow: 1 }} />

        <IconButton onClick={() => dispatch(toggleTheme())}>
          {mode === 'light' ? <MdDarkMode /> : <MdLightMode />}
        </IconButton>

        <IconButton onClick={() => navigate('/notifications')}>
          <Badge badgeContent={unreadCount} color="secondary">
            <MdNotificationsNone />
          </Badge>
        </IconButton>

        <IconButton onClick={(e) => setAnchorEl(e.currentTarget)}>
          <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
            {user?.full_name?.[0] || 'U'}
          </Avatar>
        </IconButton>
        <Menu anchorEl={anchorEl} open={!!anchorEl} onClose={() => setAnchorEl(null)}>
          <MenuItem onClick={() => { setAnchorEl(null); navigate('/profile'); }}>Profile</MenuItem>
          <MenuItem onClick={() => { setAnchorEl(null); navigate('/settings'); }}>Settings</MenuItem>
          <MenuItem onClick={() => { dispatch(logout()); navigate('/login'); }}>Logout</MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
