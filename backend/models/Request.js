const mongoose = require('mongoose');

const RequestSchema = new mongoose.Schema({
  item: { type: String, required: true },
  category: { type: String, required: true },
  purpose: { type: String, required: true },
  amount: { type: Number, required: true },
  status: { type: String, default: 'Pending' },
  attachments: [{ type: String }],
  comments: [{ user: String, text: String, file: String }],
  history: [{ action: String, user: String, date: Date }],
  createdBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  approver: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
});

module.exports = mongoose.model('Request', RequestSchema);
