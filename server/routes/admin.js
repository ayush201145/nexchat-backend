const router  = require('express').Router();
const User    = require('../models/User');
const Message = require('../models/Message');
const Room    = require('../models/Room');
const { authMiddleware, adminMiddleware } = require('../middleware/auth');

// All admin routes require auth + admin role
router.use(authMiddleware, adminMiddleware);

// GET /api/admin/stats — platform overview
router.get('/stats', async (req, res) => {
  try {
    const [users, messages, rooms, flagged, onlineUsers] = await Promise.all([
      User.countDocuments(),
      Message.countDocuments({ isDeleted: false }),
      Room.countDocuments(),
      Message.countDocuments({ isFlagged: true, isDeleted: false }),
      User.countDocuments({ isOnline: true }),
    ]);
    res.json({ users, messages, rooms, flagged, onlineUsers });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/admin/users — all users (no passwords)
router.get('/users', async (req, res) => {
  try {
    const users = await User.find().sort({ createdAt: -1 });
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PATCH /api/admin/users/:id/ban — ban or unban
router.patch('/users/:id/ban', async (req, res) => {
  try {
    const user = await User.findByIdAndUpdate(
      req.params.id,
      { isBanned: req.body.ban },
      { new: true }
    );
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PATCH /api/admin/users/:id/role — promote/demote
router.patch('/users/:id/role', async (req, res) => {
  try {
    const { role } = req.body;
    if (!['user', 'admin'].includes(role))
      return res.status(400).json({ error: 'Invalid role' });
    const user = await User.findByIdAndUpdate(req.params.id, { role }, { new: true });
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/admin/flagged — flagged messages
router.get('/flagged', async (req, res) => {
  try {
    const messages = await Message.find({ isFlagged: true, isDeleted: false })
      .populate('sender', 'username')
      .sort({ createdAt: -1 });
    res.json(messages);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE /api/admin/messages/:id — soft delete
router.delete('/messages/:id', async (req, res) => {
  try {
    await Message.findByIdAndUpdate(req.params.id, { isDeleted: true });
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/admin/rooms — all rooms including private
router.get('/rooms', async (req, res) => {
  try {
    const rooms = await Room.find()
      .populate('createdBy', 'username')
      .sort({ createdAt: -1 });
    res.json(rooms);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE /api/admin/rooms/:id — remove a room
router.delete('/rooms/:id', async (req, res) => {
  try {
    await Room.findByIdAndDelete(req.params.id);
    await Message.updateMany({ room: req.params.id }, { isDeleted: true });
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
