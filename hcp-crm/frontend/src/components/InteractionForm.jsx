/**
 * Structured interaction-logging form (Log Interaction > Structured Form tab).
 */
import { useForm, Controller } from 'react-hook-form';
import {
  Grid, TextField, MenuItem, Button, FormControlLabel, Switch, Box,
} from '@mui/material';
import { useDispatch } from 'react-redux';
import { useSnackbar } from 'notistack';
import { createInteraction } from '../store/slices/interactionSlice';

const MEETING_TYPES = ['in_person', 'virtual', 'phone', 'conference'];
const PRIORITIES = ['low', 'medium', 'high'];

export default function InteractionForm({ doctors = [], onSaved }) {
  const dispatch = useDispatch();
  const { enqueueSnackbar } = useSnackbar();
  const { control, register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm({
    defaultValues: {
      doctor_id: '', meeting_date: '', meeting_type: 'in_person',
      products_discussed: '', notes: '', samples_given: false,
      priority: 'medium', follow_up_date: '',
    },
  });

  const onSubmit = async (values) => {
    try {
      await dispatch(createInteraction({
        ...values,
        meeting_date: new Date(values.meeting_date).toISOString(),
        follow_up_date: values.follow_up_date ? new Date(values.follow_up_date).toISOString() : null,
      })).unwrap();
      enqueueSnackbar('Interaction saved', { variant: 'success' });
      reset();
      onSaved?.();
    } catch (e) {
      enqueueSnackbar('Failed to save interaction', { variant: 'error' });
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)}>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <TextField
            select fullWidth label="Doctor" defaultValue=""
            {...register('doctor_id', { required: 'Doctor is required' })}
            error={!!errors.doctor_id} helperText={errors.doctor_id?.message}
          >
            {doctors.map((d) => <MenuItem key={d.id} value={d.id}>{d.name}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth type="datetime-local" label="Meeting Date" InputLabelProps={{ shrink: true }}
            {...register('meeting_date', { required: 'Meeting date is required' })}
            error={!!errors.meeting_date} helperText={errors.meeting_date?.message}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField select fullWidth label="Meeting Type" defaultValue="in_person" {...register('meeting_type')}>
            {MEETING_TYPES.map((t) => <MenuItem key={t} value={t}>{t.replace('_', ' ')}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField select fullWidth label="Priority" defaultValue="medium" {...register('priority')}>
            {PRIORITIES.map((p) => <MenuItem key={p} value={p}>{p}</MenuItem>)}
          </TextField>
        </Grid>
        <Grid item xs={12}>
          <TextField fullWidth label="Products Discussed" placeholder="Comma separated" {...register('products_discussed')} />
        </Grid>
        <Grid item xs={12}>
          <TextField fullWidth multiline rows={4} label="Meeting Notes" {...register('notes')} />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField fullWidth type="datetime-local" label="Follow-up Date" InputLabelProps={{ shrink: true }} {...register('follow_up_date')} />
        </Grid>
        <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center' }}>
          <Controller
            name="samples_given"
            control={control}
            render={({ field }) => (
              <FormControlLabel control={<Switch checked={field.value} onChange={field.onChange} />} label="Samples Given" />
            )}
          />
        </Grid>
        <Grid item xs={12}>
          <Button type="submit" variant="contained" disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : 'Save Interaction'}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
}
