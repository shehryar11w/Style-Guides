const User = require('../models/User');
const jwt = require('jsonwebtoken');
const { UnauthorizedError, ValidationError } = require('../utils/errors');

const authService = {
  async register(userData) {
    // Check if user already exists
    const existingUser = await User.findOne({ email: userData.email });
    if (existingUser) {
      throw new ValidationError('User with this email already exists');
    }
    
    const user = new User(userData);
    await user.save();
    const userObj = user.toObject();
    delete userObj.password;
    
    // Generate token
    const token = jwt.sign(
      { id: user._id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE || '7d' }
    );
    
    return { user: userObj, token };
  },

  async login(email, password) {
    const user = await User.findOne({ email }).select('+password');
    
    if (!user || !(await user.comparePassword(password))) {
      throw new UnauthorizedError('Invalid email or password');
    }
    
    const userObj = user.toObject();
    delete userObj.password;
    
    // Generate token
    const token = jwt.sign(
      { id: user._id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRE || '7d' }
    );
    
    return { user: userObj, token };
  },
};

module.exports = authService;

