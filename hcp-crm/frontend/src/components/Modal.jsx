import { Dialog, DialogTitle, DialogContent, IconButton } from '@mui/material';
import { MdClose } from 'react-icons/md';

export default function Modal({ open, onClose, title, children, maxWidth = 'sm' }) {
  return (
    <Dialog open={open} onClose={onClose} maxWidth={maxWidth} fullWidth>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {title}
        <IconButton onClick={onClose} size="small"><MdClose /></IconButton>
      </DialogTitle>
      <DialogContent dividers>{children}</DialogContent>
    </Dialog>
  );
}
