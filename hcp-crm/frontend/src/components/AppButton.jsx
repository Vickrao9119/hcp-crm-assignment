import { Button } from '@mui/material';

export default function AppButton({ children, variant = 'contained', ...props }) {
  return (
    <Button variant={variant} disableElevation {...props}>
      {children}
    </Button>
  );
}
