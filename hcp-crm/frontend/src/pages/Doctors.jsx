import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Typography, TextField, Button, Grid, ToggleButtonGroup, ToggleButton } from '@mui/material';
import { MdAdd, MdViewModule, MdViewList } from 'react-icons/md';
import { fetchDoctors } from '../store/slices/doctorSlice';
import { doctorApi } from '../api/endpoints';
import { useSnackbar } from 'notistack';
import DoctorCard from '../components/DoctorCard';
import DoctorTable from '../components/DoctorTable';
import Modal from '../components/Modal';
import Loading from '../components/Loading';
import EmptyState from '../components/EmptyState';

export default function Doctors() {
  const dispatch = useDispatch();
  const { enqueueSnackbar } = useSnackbar();
  const { items, total, status } = useSelector((s) => s.doctors);
  const [search, setSearch] = useState('');
  const [view, setView] = useState('grid');
  const [page, setPage] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ name: '', specialization: '', city: '', phone: '', email: '' });

  useEffect(() => {
    const t = setTimeout(() => dispatch(fetchDoctors({ search, page, page_size: 12 })), 300);
    return () => clearTimeout(t);
  }, [dispatch, search, page]);

  const handleCreate = async () => {
    try {
      await doctorApi.create(form);
      enqueueSnackbar('Doctor added', { variant: 'success' });
      setModalOpen(false);
      setForm({ name: '', specialization: '', city: '', phone: '', email: '' });
      dispatch(fetchDoctors({ search, page, page_size: 12 }));
    } catch (err) {
      const detail = err?.response?.data?.detail || err?.message || 'Failed to add doctor';
      enqueueSnackbar(detail, { variant: 'error' });
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, flexWrap: 'wrap', gap: 1 }}>
        <Typography variant="h5" sx={{ fontFamily: '"Fraunces", serif' }}>Doctors</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField size="small" placeholder="Search doctors..." value={search} onChange={(e) => setSearch(e.target.value)} />
          <ToggleButtonGroup size="small" value={view} exclusive onChange={(_, v) => v && setView(v)}>
            <ToggleButton value="grid"><MdViewModule /></ToggleButton>
            <ToggleButton value="table"><MdViewList /></ToggleButton>
          </ToggleButtonGroup>
          <Button variant="contained" startIcon={<MdAdd />} onClick={() => setModalOpen(true)}>Add Doctor</Button>
        </Box>
      </Box>

      {status === 'loading' && !items.length ? <Loading /> : null}
      {status === 'succeeded' && !items.length ? <EmptyState title="No doctors found" subtitle="Add your first doctor to get started." actionLabel="Add Doctor" onAction={() => setModalOpen(true)} /> : null}

      {view === 'grid' ? (
        <Grid container spacing={2}>
          {items.map((d) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={d.id}>
              <DoctorCard doctor={d} />
            </Grid>
          ))}
        </Grid>
      ) : (
        <DoctorTable rows={items} loading={status === 'loading'} rowCount={total} page={page} pageSize={12} onPageChange={setPage} />
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Add Doctor">
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
          <TextField label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <TextField label="Specialization" value={form.specialization} onChange={(e) => setForm({ ...form, specialization: e.target.value })} />
          <TextField label="City" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
          <TextField label="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <TextField label="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <Button variant="contained" onClick={handleCreate}>Save Doctor</Button>
        </Box>
      </Modal>
    </Box>
  );
}
