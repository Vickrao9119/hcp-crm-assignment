/**
 * Wires the repeated `status` transitions for a createAsyncThunk onto a slice
 * builder: pending -> 'loading', fulfilled -> 'succeeded', rejected -> 'failed'.
 *
 * Pass `pending` / `fulfilled` / `rejected` callbacks to run slice-specific
 * logic after the status is set. The `rejected` case is only registered when a
 * `rejected` handler is provided, matching slices that don't track failures.
 */
export function addAsyncCases(builder, thunk, handlers = {}) {
  builder.addCase(thunk.pending, (state, action) => {
    state.status = 'loading';
    handlers.pending?.(state, action);
  });
  builder.addCase(thunk.fulfilled, (state, action) => {
    state.status = 'succeeded';
    handlers.fulfilled?.(state, action);
  });
  if (handlers.rejected) {
    builder.addCase(thunk.rejected, (state, action) => {
      state.status = 'failed';
      handlers.rejected(state, action);
    });
  }
  return builder;
}
