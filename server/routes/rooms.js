const router  = require('express').Router();
const axios   = require('axios');
const Room    = require('../models/Room');
const Message = require('../models/Message');
const { authMiddleware } = require('../middleware/auth');

// All routes require auth
router.use(authMiddleware);

// GET /api/rooms — list all public rooms
router.get('/', async (req, res) => {
  try {
    const rooms = await Room.find({ isPrivate: false })
      .populate('createdBy', 'username')
      .sort({ createdAt: -1 });
    res.json(rooms);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/rooms — create a room
router.post('/', async (req, res) => {
  try {
    const { name, description = '', isPrivate = false } = req.body;
    if (!name?.trim()) return res.status(400).json({ error: 'Room name is required' });

    const room = await Room.create({
      name: name.trim(),
      description,
      isPrivate,
      createdBy: req.user.id,
      members: [req.user.id],
    });
    res.status(201).json(room);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// GET /api/rooms/:room/messages — fetch last 100 messages
router.get('/:room/messages', async (req, res) => {
  try {
    const messages = await Message.find({
      room: req.params.room,
      isDeleted: false,
    })
      .populate('sender', 'username avatar')
      .sort({ createdAt: 1 })
      .limit(100);
    res.json(messages);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/rooms/smart-reply — get Naive Bayes suggestions
router.post('/smart-reply', async (req, res) => {
  try {
    const { message } = req.body;
    const response = await axios.post(
      'http://localhost:5001/predict',
      { message },
      { timeout: 3000 }
    );
    res.json(response.data);
  } catch {
    // Graceful fallback if ML service is down
    res.json({ suggestions: ['👍 Got it!', 'Thanks!', 'Sounds good!'] });
  }
});

module.exports = router;
