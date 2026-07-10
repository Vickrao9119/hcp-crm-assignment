import { DataGrid } from '@mui/x-data-grid';
import { Box, Chip } from '@mui/material';
import dayjs from 'dayjs';

const priorityColor = { high: 'error', medium: 'warning', low: 'default' };

const columns = [
  { field: 'meeting_date', headerName: 'Date', flex: 1, valueFormatter: (v) => dayjs(v.value).format('DD MMM YYYY, hh:mm A') },
  { field: 'products_discussed', headerName: 'Products', flex: 1 },
  { field: 'priority', headerName: 'Priority', flex: 0.6, renderCell: (p) => <Chip size="small" label={p.value} color={priorityColor[p.value] || 'default'} /> },
  { field: 'source', headerName: 'Source', flex: 0.6 },
  { field: 'notes', headerName: 'Notes', flex: 1.5 },
];

export default function HistoryTable({ rows, loading, rowCount, page, pageSize, onPageChange }) {
  return (
    <Box sx={{ height: 560, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        loading={loading}
        rowCount={rowCount}
        paginationMode="server"
        paginationModel={{ page: page - 1, pageSize }}
        onPaginationModelChange={(model) => onPageChange(model.page + 1)}
        disableRowSelectionOnClick
      />
    </Box>
  );
}
