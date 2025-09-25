import React, { useState } from 'react';
import { TextField, Button, Grid, Paper, Typography } from '@mui/material';

const RequesterDashboard = () => {
  const [form, setForm] = useState({
    item: '',
    category: '',
    purpose: '',
    amount: '',
    file: null,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleFileChange = (e) => {
    setForm({ ...form, file: e.target.files[0] });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Submit logic here
  };

  return (
    <Paper sx={{ p: 2, maxWidth: 600, margin: 'auto' }}>
      <Typography variant="h6" gutterBottom>New Procurement Request</Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField label="Item" name="item" fullWidth required value={form.item} onChange={handleChange} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="Category" name="category" fullWidth required value={form.category} onChange={handleChange} />
          </Grid>
          <Grid item xs={12}>
            <TextField label="Purpose" name="purpose" fullWidth required value={form.purpose} onChange={handleChange} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="Amount" name="amount" type="number" fullWidth required value={form.amount} onChange={handleChange} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button variant="contained" component="label" fullWidth>
              Upload Document
              <input type="file" hidden onChange={handleFileChange} />
            </Button>
            {form.file && <Typography variant="caption">{form.file.name}</Typography>}
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" fullWidth>Submit Request</Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default RequesterDashboard;
