import React, { useState } from 'react';
import { Paper, Typography, List, ListItem, ListItemText, TextField, Button } from '@mui/material';

const initialComments = [
  { user: 'Admin', text: 'Please clarify the item specs.' },
  { user: 'Requester', text: 'Specs attached in the document.' },
];

const ClarificationThread = () => {
  const [comments, setComments] = useState(initialComments);
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);

  const handleAddComment = () => {
    if (input.trim()) {
      setComments([...comments, { user: 'You', text: input }]);
      setInput('');
    }
  };

  return (
    <Paper sx={{ p: 2, maxWidth: 600, margin: 'auto' }}>
      <Typography variant="h6" gutterBottom>Clarification Thread</Typography>
      <List>
        {comments.map((c, i) => (
          <ListItem key={i}>
            <ListItemText primary={c.user} secondary={c.text} />
          </ListItem>
        ))}
      </List>
      <TextField
        label="Add clarification"
        fullWidth
        value={input}
        onChange={e => setInput(e.target.value)}
        sx={{ mt: 2 }}
      />
      <Button variant="contained" sx={{ mt: 1 }} onClick={handleAddComment}>Send</Button>
      <Button variant="outlined" component="label" sx={{ mt: 1, ml: 1 }}>
        Upload File
        <input type="file" hidden onChange={e => setFile(e.target.files[0])} />
      </Button>
      {file && <Typography variant="caption">{file.name}</Typography>}
    </Paper>
  );
};

export default ClarificationThread;
