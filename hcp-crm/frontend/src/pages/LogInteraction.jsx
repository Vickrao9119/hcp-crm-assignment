import { useEffect, useState } from 'react';
import { Box, Tabs, Tab, Paper } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDoctors } from '../store/slices/doctorSlice';
import InteractionForm from '../components/InteractionForm';
import ChatWindow from '../components/ChatWindow';
import PageHeader from '../components/PageHeader';

export default function LogInteraction() {
  const dispatch = useDispatch();
  const { items: doctors } = useSelector((s) => s.doctors);
  const [tab, setTab] = useState(0);

  useEffect(() => { dispatch(fetchDoctors({ page_size: 100 })); }, [dispatch]);

  return (
    <Box>
      <PageHeader title="Log Interaction" />
      <Paper sx={{ mb: 2 }}>
        <Tabs value={tab} onChange={(_, v) => setTab(v)}>
          <Tab label="Structured Form" />
          <Tab label="AI Chat" />
        </Tabs>
      </Paper>
      {tab === 0 ? (
        <Paper sx={{ p: 3 }}>
          <InteractionForm doctors={doctors} />
        </Paper>
      ) : (
        <ChatWindow />
      )}
    </Box>
  );
}
