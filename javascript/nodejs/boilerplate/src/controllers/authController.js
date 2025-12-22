const authService = require('../services/authService');
const { asyncHandler } = require('../utils/helpers');

const authController = {
  register: asyncHandler(async (req, res) => {
    const user = await authService.register(req.body);
    res.status(201).json({ data: user });
  }),

  login: asyncHandler(async (req, res) => {
    const { email, password } = req.body;
    const result = await authService.login(email, password);
    res.json({ data: result });
  }),
};

module.exports = authController;

