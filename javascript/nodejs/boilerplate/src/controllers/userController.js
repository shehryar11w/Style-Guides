const userService = require('../services/userService');
const { asyncHandler } = require('../utils/helpers');

const userController = {
  getAllUsers: asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const result = await userService.getAllUsers({ page, limit });
    res.json({ data: result.data, pagination: result.pagination });
  }),

  getUserById: asyncHandler(async (req, res) => {
    const { id } = req.params;
    const user = await userService.getUserById(id);
    res.json({ data: user });
  }),

  createUser: asyncHandler(async (req, res) => {
    const user = await userService.createUser(req.body);
    res.status(201).json({ data: user });
  }),

  updateUser: asyncHandler(async (req, res) => {
    const { id } = req.params;
    const user = await userService.updateUser(id, req.body);
    res.json({ data: user });
  }),

  deleteUser: asyncHandler(async (req, res) => {
    const { id } = req.params;
    await userService.deleteUser(id);
    res.status(204).send();
  }),
};

module.exports = userController;

