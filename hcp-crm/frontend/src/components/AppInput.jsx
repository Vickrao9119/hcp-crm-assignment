import { TextField } from '@mui/material';

export default function AppInput({ label, register, name, error, helperText, ...props }) {
  return (
    <TextField
      label={label}
      fullWidth
      size="medium"
      error={!!error}
      helperText={error?.message || helperText}
      {...(register ? register(name) : {})}
      {...props}
    />
  );
}
