const mongoose = require('mongoose');

const roomSchema = new mongoose.Schema(
  {
    name:        { type: String, required: true, unique: true, trim: true, minlength: 2, maxlength: 40 },
    description: { type: String, default: '', maxlength: 200 },
    isPrivate:   { type: Boolean, default: false },
    members:     [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
    createdBy:   { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Room', roomSchema);
