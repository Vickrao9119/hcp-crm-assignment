import { DataGrid } from '@mui/x-data-grid';
import { Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const columns = [
  { field: 'name', headerName: 'Doctor', flex: 1.2 },
  { field: 'specialization', headerName: 'Specialization', flex: 1 },
  { field: 'city', headerName: 'City', flex: 0.8 },
  { field: 'phone', headerName: 'Phone', flex: 1 },
  { field: 'email', headerName: 'Email', flex: 1.2 },
];

export default function DoctorTable({ rows, loading, rowCount, page, pageSize, onPageChange }) {
  const navigate = useNavigate();
  return (
    <Box sx={{ height: 520, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        loading={loading}
        rowCount={rowCount}
        paginationMode="server"
        paginationModel={{ page: page - 1, pageSize }}
        onPaginationModelChange={(model) => onPageChange(model.page + 1)}
        onRowClick={(params) => navigate(`/doctors/${params.id}`)}
        disableRowSelectionOnClick
      />
    </Box>
  );
}
