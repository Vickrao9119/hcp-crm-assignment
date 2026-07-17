import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, MenuItem, TextField } from '@mui/material';
import { fetchInteractions } from '../store/slices/interactionSlice';
import HistoryTable from '../components/HistoryTable';
import PageHeader from '../components/PageHeader';

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
      <PageHeader
        title="Interaction History"
        actions={
          <TextField select size="small" label="Priority" value={priority} onChange={(e) => setPriority(e.target.value)} sx={{ minWidth: 160 }}>
            <MenuItem value="">All</MenuItem>
            <MenuItem value="high">High</MenuItem>
            <MenuItem value="medium">Medium</MenuItem>
            <MenuItem value="low">Low</MenuItem>
          </TextField>
        }
      />
      <HistoryTable rows={items} loading={status === 'loading'} rowCount={total} page={page} pageSize={10} onPageChange={setPage} />
    </Box>
  );
}
