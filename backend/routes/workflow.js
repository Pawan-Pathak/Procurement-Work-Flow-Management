const express = require('express');
const router = express.Router();
const Request = require('../models/Request');

// Submit new request
router.post('/submit', async (req, res) => {
  try {
    const newRequest = new Request(req.body);
    await newRequest.save();
    res.status(201).send(newRequest);
  } catch (error) {
    res.status(400).send(error);
  }
});

// Get requests for approval (role-based)
router.get('/pending', async (req, res) => {
  try {
    const pendingRequests = await Request.find({ status: 'pending' });
    res.status(200).send(pendingRequests);
  } catch (error) {
    res.status(500).send(error);
  }
});

// Add clarification comment
router.post('/:id/comment', async (req, res) => {
  try {
    const request = await Request.findById(req.params.id);
    request.comments.push(req.body.comment);
    await request.save();
    res.status(200).send(request);
  } catch (error) {
    res.status(400).send(error);
  }
});

// Approve/Reject/Request Info
router.post('/:id/action', async (req, res) => {
  try {
    const { action } = req.body;
    let status;
    if (action === 'approve') {
      status = 'approved';
    } else if (action === 'reject') {
      status = 'rejected';
    } else {
      return res.status(400).send({ message: 'Invalid action' });
    }
    const request = await Request.findByIdAndUpdate(
      req.params.id,
      { status },
      { new: true }
    );
    res.status(200).send(request);
  } catch (error) {
    res.status(400).send(error);
  }
});

module.exports = router;