const express = require('express');
const userController = require('../controllers/userController');
const { authenticate } = require('../middleware/auth');
const { validateUser, validateUserId } = require('../validators/userValidator');

const router = express.Router();

router.get('/', authenticate, userController.getAllUsers);
router.get('/:id', authenticate, validateUserId, userController.getUserById);
router.post('/', authenticate, validateUser, userController.createUser);
router.put('/:id', authenticate, validateUserId, validateUser, userController.updateUser);
router.delete('/:id', authenticate, validateUserId, userController.deleteUser);

module.exports = router;

