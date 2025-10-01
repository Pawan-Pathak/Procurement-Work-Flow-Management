'use strict';

// Load env from current working directory, then fallback to repo root
require('dotenv').config();
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env'), override: false });
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const workflowRouter = require('./routes/workflow');

const app = express();
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/workflow', workflowRouter);

const mongoUri = process.env.MONGODB_URI || 'mongodb://localhost:27017/procurement';
const port = process.env.PORT || 4000;

async function start() {
  try {
    await mongoose.connect(mongoUri, {
      serverSelectionTimeoutMS: 5000,
    });
    console.log('Connected to MongoDB');
    app.listen(port, () => {
      console.log(`Node API listening on port ${port}`);
    });
  } catch (err) {
    console.error('Failed to connect to MongoDB', err);
    process.exit(1);
  }
}

start();

module.exports = app;

