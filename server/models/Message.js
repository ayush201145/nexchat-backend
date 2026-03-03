const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema(
  {
    room:      { type: String, required: true, index: true },
    sender:    { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    content:   { type: String, required: true, maxlength: 2000 },
    type:      { type: String, enum: ['text', 'system'], default: 'text' },
    isFlagged: { type: Boolean, default: false },
    isDeleted: { type: Boolean, default: false },
  },
  { timestamps: true }
);

// Compound index for fast room queries
messageSchema.index({ room: 1, createdAt: -1 });

module.exports = mongoose.model('Message', messageSchema);
