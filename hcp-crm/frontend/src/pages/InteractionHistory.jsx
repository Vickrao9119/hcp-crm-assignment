import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Typography, MenuItem, TextField } from '@mui/material';
import { fetchInteractions } from '../store/slices/interactionSlice';
import HistoryTable from '../components/HistoryTable';

export default function InteractionHistory() {
  const dispatch = useDispatch();
  const { items, total, status } = useSelector((s) => s.interactions);
  const [priority, setPriority] = useState('');
  const [page, setPage] = useState(1);

  useEffect(() => {
    dispatch(fetchInteractions({ priority: priority || undefined, page, page_size: 10 }));
  }, [dispatch, priority, page]);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, flexWrap: 'wrap', gap: 1 }}>
        <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif' }}>Interaction History</Typography>
        <TextField select size="small" label="Priority" value={priority} onChange={(e) => setPriority(e.target.value)} sx={{ minWidth: 160 }}>
          <MenuItem value="">All</MenuItem>
          <MenuItem value="high">High</MenuItem>
          <MenuItem value="medium">Medium</MenuItem>
          <MenuItem value="low">Low</MenuItem>
        </TextField>
      </Box>
      <HistoryTable rows={items} loading={status === 'loading'} rowCount={total} page={page} pageSize={10} onPageChange={setPage} />
    </Box>
  );
}
