import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText, Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';

const requests = [
  { id: 1, item: 'Laptop', amount: 1200, status: 'Pending', attachments: ['specs.pdf'] },
  // ...more requests
];

const ApproverDashboard = () => {
  const [open, setOpen] = React.useState(false);
  const [selected, setSelected] = React.useState(null);

  const handleOpen = (req) => {
    setSelected(req);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);

  return (
    <Paper sx={{ p: 2, maxWidth: 700, margin: 'auto' }}>
      <Typography variant="h6" gutterBottom>Pending Requests</Typography>
      <List>
        {requests.map((req) => (
          <ListItem key={req.id} button onClick={() => handleOpen(req)}>
            <ListItemText primary={req.item} secondary={`Amount: $${req.amount} | Status: ${req.status}`} />
          </ListItem>
        ))}
      </List>
      <Dialog open={open} onClose={handleClose} fullWidth>
        <DialogTitle>Request Details</DialogTitle>
        <DialogContent>
          {selected && (
            <>
              <Typography>Item: {selected.item}</Typography>
              <Typography>Amount: ${selected.amount}</Typography>
              <Typography>Status: {selected.status}</Typography>
              <Typography>Attachments: {selected.attachments.join(', ')}</Typography>
              {/* Approval history, feedback, etc. */}
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button color="success">Approve</Button>
          <Button color="error">Reject</Button>
          <Button color="info">Request Info</Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
};

export default ApproverDashboard;
