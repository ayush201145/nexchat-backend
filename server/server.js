const express   = require('express');
const http      = require('http');
const socketIo  = require('socket.io');
const mongoose  = require('mongoose');
const cors      = require('cors');
const jwt       = require('jsonwebtoken');
require('dotenv').config();

const User    = require('./models/User');
const Message = require('./models/Message');

const authRoutes  = require('./routes/auth');
const roomRoutes  = require('./routes/rooms');
const adminRoutes = require('./routes/admin');

const app    = express();
const server = http.createServer(app);
const io     = socketIo(server, {
  cors: { origin: process.env.CLIENT_URL || 'http://localhost:3000', methods: ['GET', 'POST'] },
});

// ─── Middleware ───────────────────────────────────────────────────────────────
app.use(cors({ origin: process.env.CLIENT_URL || 'http://localhost:3000' }));
app.use(express.json());

// ─── Database ─────────────────────────────────────────────────────────────────
mongoose
  .connect(process.env.MONGO_URI || 'mongodb://localhost:27017/nexchat')
  .then(() => console.log('✅ MongoDB connected'))
  .catch((err) => { console.error('❌ MongoDB error:', err); process.exit(1); });

// ─── Routes ───────────────────────────────────────────────────────────────────
app.use('/api/auth',  authRoutes);
app.use('/api/rooms', roomRoutes);
app.use('/api/admin', adminRoutes);
app.get('/api/health', (_, res) => res.json({ status: 'ok', uptime: process.uptime() }));

// ─── Socket.io Auth ───────────────────────────────────────────────────────────
io.use((socket, next) => {
  const token = socket.handshake.auth?.token;
  if (!token) return next(new Error('No token'));
  try {
    socket.user = jwt.verify(token, process.env.JWT_SECRET || 'secret123');
    next();
  } catch { next(new Error('Invalid token')); }
});

// ─── Socket.io Events ─────────────────────────────────────────────────────────
const BAD_WORDS = ['spam', 'abuse', 'hate', 'scam'];

io.on('connection', async (socket) => {
  console.log(`🔌 ${socket.user.username} connected`);
  await User.findByIdAndUpdate(socket.user.id, { isOnline: true, lastSeen: new Date() });
  io.emit('user:online', { userId: socket.user.id, username: socket.user.username });

  socket.on('room:join', async ({ room }) => {
    socket.join(room);
    const history = await Message.find({ room, isDeleted: false })
      .populate('sender', 'username avatar')
      .sort({ createdAt: 1 }).limit(50);
    socket.emit('room:history', history);
    const sysMsg = await Message.create({
      room, sender: socket.user.id,
      content: `${socket.user.username} joined the room`, type: 'system',
    });
    io.to(room).emit('message:system', { ...sysMsg.toObject(), sender: { username: socket.user.username } });
  });

  socket.on('room:leave', ({ room }) => {
    socket.leave(room);
    io.to(room).emit('message:system', {
      content: `${socket.user.username} left the room`, type: 'system', createdAt: new Date(),
    });
  });

  socket.on('message:send', async ({ room, content }) => {
    if (!content?.trim()) return;
    try {
      const isFlagged = BAD_WORDS.some(w => content.toLowerCase().includes(w));
      const msg = await Message.create({ room, content: content.trim(), sender: socket.user.id, isFlagged });
      const populated = await msg.populate('sender', 'username avatar');
      io.to(room).emit('message:new', populated);
    } catch (err) { socket.emit('error', { message: err.message }); }
  });

  socket.on('typing:start', ({ room }) =>
    socket.to(room).emit('typing:update', { username: socket.user.username, isTyping: true }));
  socket.on('typing:stop', ({ room }) =>
    socket.to(room).emit('typing:update', { username: socket.user.username, isTyping: false }));

  socket.on('disconnect', async () => {
    await User.findByIdAndUpdate(socket.user.id, { isOnline: false, lastSeen: new Date() });
    io.emit('user:offline', { userId: socket.user.id });
    console.log(`❌ ${socket.user.username} disconnected`);
  });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
