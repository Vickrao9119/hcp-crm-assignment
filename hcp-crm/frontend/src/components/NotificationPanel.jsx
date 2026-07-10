import { List, ListItem, ListItemText, Typography, Box } from '@mui/material';
import dayjs from 'dayjs';
import EmptyState from './EmptyState';

export default function NotificationPanel({ items = [], onMarkRead }) {
  if (!items.length) return <EmptyState title="No notifications" subtitle="You're all caught up." />;
  return (
    <List>
      {items.map((n) => (
        <ListItem
          key={n.id}
          onClick={() => onMarkRead?.(n.id)}
          sx={{
            borderRadius: 2, mb: 1, cursor: 'pointer',
            bgcolor: n.is_read ? 'transparent' : 'action.hover',
          }}
        >
          <ListItemText
            primary={n.title}
            secondary={
              <Box>
                <Typography variant="body2" color="text.secondary">{n.message}</Typography>
                <Typography variant="caption" color="text.disabled">{dayjs(n.created_at).fromNow?.() || dayjs(n.created_at).format('DD MMM, hh:mm A')}</Typography>
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
}
