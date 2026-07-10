import { Skeleton as MuiSkeleton, Stack } from '@mui/material';

export default function SkeletonBlock({ rows = 3, height = 40 }) {
  return (
    <Stack spacing={1.5}>
      {Array.from({ length: rows }).map((_, i) => (
        <MuiSkeleton key={i} variant="rounded" height={height} animation="wave" />
      ))}
    </Stack>
  );
}
