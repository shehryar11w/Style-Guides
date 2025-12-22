const User = require('../models/User');
const { NotFoundError } = require('../utils/errors');

const userService = {
  async getAllUsers({ page, limit }) {
    const skip = (page - 1) * limit;
    const users = await User.find()
      .skip(skip)
      .limit(parseInt(limit))
      .select('-password');
    
    const total = await User.countDocuments();
    
    return {
      data: users,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total,
        pages: Math.ceil(total / limit),
      },
    };
  },

  async getUserById(id) {
    const user = await User.findById(id).select('-password');
    if (!user) {
      throw new NotFoundError('User not found');
    }
    return user;
  },

  async createUser(userData) {
    const user = new User(userData);
    await user.save();
    const userObj = user.toObject();
    delete userObj.password;
    return userObj;
  },

  async updateUser(id, updateData) {
    const user = await User.findByIdAndUpdate(
      id,
      updateData,
      { new: true, runValidators: true }
    ).select('-password');
    
    if (!user) {
      throw new NotFoundError('User not found');
    }
    
    return user;
  },

  async deleteUser(id) {
    const user = await User.findByIdAndDelete(id);
    if (!user) {
      throw new NotFoundError('User not found');
    }
    return user;
  },
};

module.exports = userService;

