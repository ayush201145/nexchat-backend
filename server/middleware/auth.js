const jwt  = require('jsonwebtoken');
const User = require('../models/User');

/**
 * Verifies JWT from Authorization header.
 * Attaches decoded payload to req.user.
 */
const authMiddleware = (req, res, next) => {
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer '))
    return res.status(401).json({ error: 'No token provided' });

  const token = header.split(' ')[1];
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET || 'secret123');
    next();
  } catch (err) {
    const msg = err.name === 'TokenExpiredError' ? 'Token expired' : 'Invalid token';
    res.status(401).json({ error: msg });
  }
};

/**
 * Must be used AFTER authMiddleware.
 * Allows only users with role === 'admin'.
 */
const adminMiddleware = async (req, res, next) => {
  try {
    const user = await User.findById(req.user.id);
    if (!user || user.role !== 'admin')
      return res.status(403).json({ error: 'Admin access required' });
    next();
  } catch {
    res.status(500).json({ error: 'Authorization check failed' });
  }
};

module.exports = { authMiddleware, adminMiddleware };
