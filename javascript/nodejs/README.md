# Node.js Style Guide and Design Patterns

## Overview

Node.js is a JavaScript runtime built on Chrome's V8 engine, enabling server-side JavaScript development. This guide focuses on Express.js patterns for building RESTful APIs and web applications with Node.js.

## Design Philosophy

- **Event-Driven**: Non-blocking, asynchronous I/O
- **Modular**: Use npm packages and modular architecture
- **RESTful**: Follow REST principles for API design
- **Middleware-Based**: Leverage Express middleware for functionality
- **Error-First**: Use error-first callbacks and proper error handling

## Directory Structure

```
nodejs-app/
├── src/
│   ├── controllers/                  # Request handlers
│   │   ├── userController.js
│   │   ├── authController.js
│   │   └── productController.js
│   ├── models/                       # Data models
│   │   ├── User.js
│   │   ├── Product.js
│   │   └── index.js
│   ├── routes/                       # Route definitions
│   │   ├── index.js
│   │   ├── userRoutes.js
│   │   ├── authRoutes.js
│   │   └── productRoutes.js
│   ├── middleware/                   # Custom middleware
│   │   ├── auth.js
│   │   ├── errorHandler.js
│   │   ├── validation.js
│   │   └── logger.js
│   ├── services/                     # Business logic
│   │   ├── userService.js
│   │   ├── authService.js
│   │   └── emailService.js
│   ├── utils/                        # Utility functions
│   │   ├── helpers.js
│   │   ├── validators.js
│   │   ├── constants.js
│   │   └── logger.js
│   ├── config/                       # Configuration
│   │   ├── database.js
│   │   ├── env.js
│   │   └── passport.js
│   ├── validators/                   # Request validation schemas
│   │   ├── userValidator.js
│   │   └── authValidator.js
│   ├── types/                        # TypeScript types (if using TS)
│   │   └── index.ts
│   └── app.js                        # Express app setup
├── tests/                            # Test files
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── public/                           # Static files
│   └── uploads/
├── .env                              # Environment variables
├── .env.example
├── .gitignore
├── package.json
├── server.js                         # Application entry point
└── README.md
```

### Directory Structure Explanation

- **`src/controllers/`**: Handle HTTP requests and responses
- **`src/models/`**: Data models (Mongoose, Sequelize, etc.)
- **`src/routes/`**: Route definitions and URL mapping
- **`src/middleware/`**: Custom middleware functions
- **`src/services/`**: Business logic layer
- **`src/utils/`**: Helper functions and utilities
- **`src/config/`**: Configuration files (database, environment, etc.)
- **`src/validators/`**: Request validation schemas

## Naming Conventions

### Files and Directories
- **Files**: camelCase (`userController.js`, `authService.js`)
- **Directories**: camelCase (`controllers/`, `middleware/`)
- **Classes**: PascalCase (`UserController`, `AuthService`)
- **Functions**: camelCase (`getUserById`, `createUser`)
- **Variables**: camelCase (`userName`, `isActive`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_LENGTH`, `API_BASE_URL`)

### Routes
- **URLs**: Use kebab-case (`/api/v1/user-profile`)
- **Route files**: camelCase ending with `Routes` (`userRoutes.js`)

## Code Style Guidelines

### JavaScript Style
- Use **2 spaces** for indentation
- Use **single quotes** for strings (or double quotes consistently)
- Use **semicolons** (or omit consistently)
- Maximum line length: **100 characters**
- Use **const** by default, **let** when needed, avoid **var**
- Use **arrow functions** for callbacks

### Node.js/Express-Specific Style
- Use **async/await** instead of callbacks
- Use **middleware** for cross-cutting concerns
- Follow **RESTful** conventions
- Use **environment variables** for configuration
- Implement proper **error handling**

### Example Code Style

```javascript
// Good
const express = require('express');
const { body, validationResult } = require('express-validator');
const userService = require('../services/userService');
const { asyncHandler } = require('../utils/helpers');
const { authenticate } = require('../middleware/auth');

const router = express.Router();

router.get(
  '/users/:id',
  authenticate,
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const user = await userService.getUserById(id);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({ data: user });
  })
);

router.post(
  '/users',
  [
    body('email').isEmail().normalizeEmail(),
    body('name').trim().isLength({ min: 1, max: 100 }),
  ],
  asyncHandler(async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    
    const user = await userService.createUser(req.body);
    res.status(201).json({ data: user });
  })
);

module.exports = router;

// Bad
const express = require('express');
const router = express.Router();

router.get('/users/:id', (req, res) => {  // No error handling, no validation
  // Inline logic, no service layer
  User.findById(req.params.id, (err, user) => {  // Callback instead of async/await
    if (err) {
      res.send(err);  // Poor error handling
    } else {
      res.send(user);  // No status code, no formatting
    }
  });
});
```

## Component Patterns

### Express App Setup Pattern

```javascript
// src/app.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const routes = require('./routes');
const { errorHandler } = require('./middleware/errorHandler');
const { notFoundHandler } = require('./middleware/notFoundHandler');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Compression
app.use(compression());

// Logging
if (process.env.NODE_ENV !== 'production') {
  app.use(morgan('dev'));
}

// Routes
app.use('/api/v1', routes);

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

module.exports = app;
```

### Server Entry Point Pattern

```javascript
// server.js
const app = require('./src/app');
const { connectDatabase } = require('./src/config/database');
const logger = require('./src/utils/logger');

const PORT = process.env.PORT || 3000;

async function startServer() {
  try {
    // Connect to database
    await connectDatabase();
    logger.info('Database connected');
    
    // Start server
    app.listen(PORT, () => {
      logger.info(`Server running on port ${PORT}`);
    });
  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  logger.error('Unhandled Promise Rejection:', err);
  process.exit(1);
});

startServer();
```

### Route Pattern

```javascript
// src/routes/index.js
const express = require('express');
const userRoutes = require('./userRoutes');
const authRoutes = require('./authRoutes');
const productRoutes = require('./productRoutes');

const router = express.Router();

router.use('/users', userRoutes);
router.use('/auth', authRoutes);
router.use('/products', productRoutes);

module.exports = router;

// src/routes/userRoutes.js
const express = require('express');
const userController = require('../controllers/userController');
const { authenticate } = require('../middleware/auth');
const { validateUser } = require('../validators/userValidator');

const router = express.Router();

router.get('/', authenticate, userController.getAllUsers);
router.get('/:id', authenticate, userController.getUserById);
router.post('/', authenticate, validateUser, userController.createUser);
router.put('/:id', authenticate, validateUser, userController.updateUser);
router.delete('/:id', authenticate, userController.deleteUser);

module.exports = router;
```

### Controller Pattern

```javascript
// src/controllers/userController.js
const userService = require('../services/userService');
const { asyncHandler } = require('../utils/helpers');

const userController = {
  getAllUsers: asyncHandler(async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const users = await userService.getAllUsers({ page, limit });
    res.json({ data: users, pagination: users.pagination });
  }),

  getUserById: asyncHandler(async (req, res) => {
    const { id } = req.params;
    const user = await userService.getUserById(id);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({ data: user });
  }),

  createUser: asyncHandler(async (req, res) => {
    const user = await userService.createUser(req.body);
    res.status(201).json({ data: user });
  }),

  updateUser: asyncHandler(async (req, res) => {
    const { id } = req.params;
    const user = await userService.updateUser(id, req.body);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({ data: user });
  }),

  deleteUser: asyncHandler(async (req, res) => {
    const { id } = req.params;
    await userService.deleteUser(id);
    res.status(204).send();
  }),
};

module.exports = userController;
```

### Service Pattern

```javascript
// src/services/userService.js
const User = require('../models/User');
const { NotFoundError } = require('../utils/errors');

const userService = {
  async getAllUsers({ page, limit }) {
    const skip = (page - 1) * limit;
    const users = await User.find()
      .skip(skip)
      .limit(limit)
      .select('-password');
    
    const total = await User.countDocuments();
    
    return {
      data: users,
      pagination: {
        page,
        limit,
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
    return user.toObject({ transform: (doc, ret) => {
      delete ret.password;
      return ret;
    }});
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
```

### Middleware Pattern

```javascript
// src/middleware/auth.js
const jwt = require('jsonwebtoken');
const { UnauthorizedError } = require('../utils/errors');

const authenticate = (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      throw new UnauthorizedError('No token provided');
    }
    
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    next(new UnauthorizedError('Invalid token'));
  }
};

module.exports = { authenticate };

// src/middleware/errorHandler.js
const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
  logger.error(err);
  
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  res.status(statusCode).json({
    error: {
      message,
      ...(process.env.NODE_ENV !== 'production' && { stack: err.stack }),
    },
  });
};

module.exports = { errorHandler };

// src/middleware/notFoundHandler.js
const notFoundHandler = (req, res) => {
  res.status(404).json({
    error: {
      message: `Route ${req.method} ${req.path} not found`,
    },
  });
};

module.exports = { notFoundHandler };
```

### Validation Pattern

```javascript
// src/validators/userValidator.js
const { body, param } = require('express-validator');

const validateUser = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Invalid email address'),
  body('name')
    .trim()
    .isLength({ min: 1, max: 100 })
    .withMessage('Name must be between 1 and 100 characters'),
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters'),
];

const validateUserId = [
  param('id')
    .isMongoId()
    .withMessage('Invalid user ID'),
];

module.exports = {
  validateUser,
  validateUserId,
};
```

## Error Handling Patterns

### Custom Error Classes

```javascript
// src/utils/errors.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404);
  }
}

class ValidationError extends AppError {
  constructor(message = 'Validation failed') {
    super(message, 400);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401);
  }
}

module.exports = {
  AppError,
  NotFoundError,
  ValidationError,
  UnauthorizedError,
};
```

### Async Handler Pattern

```javascript
// src/utils/helpers.js
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

module.exports = { asyncHandler };
```

## Database Patterns

### Mongoose Model Pattern

```javascript
// src/models/User.js
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true,
    maxlength: [100, 'Name cannot exceed 100 characters'],
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\S+@\S+\.\S+$/, 'Please provide a valid email'],
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [8, 'Password must be at least 8 characters'],
    select: false,
  },
}, {
  timestamps: true,
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

## Testing Patterns

### API Testing

```javascript
// tests/integration/user.test.js
const request = require('supertest');
const app = require('../../src/app');
const User = require('../../src/models/User');

describe('User API', () => {
  beforeEach(async () => {
    await User.deleteMany({});
  });

  describe('GET /api/v1/users', () => {
    it('should get all users', async () => {
      await User.create({ name: 'Test User', email: 'test@example.com', password: 'password123' });
      
      const res = await request(app)
        .get('/api/v1/users')
        .expect(200);
      
      expect(res.body.data).toHaveLength(1);
    });
  });

  describe('POST /api/v1/users', () => {
    it('should create a new user', async () => {
      const userData = {
        name: 'New User',
        email: 'newuser@example.com',
        password: 'password123',
      };
      
      const res = await request(app)
        .post('/api/v1/users')
        .send(userData)
        .expect(201);
      
      expect(res.body.data).toHaveProperty('email', userData.email);
    });
  });
});
```

## Best Practices

### Performance
- Use **connection pooling** for databases
- Implement **caching** (Redis) for frequently accessed data
- Use **compression** middleware
- Implement **rate limiting**
- Use **async/await** instead of callbacks

### Security
- Use **helmet** for security headers
- Validate and sanitize all inputs
- Use **bcrypt** for password hashing
- Implement **JWT** for authentication
- Use **HTTPS** in production
- Set up **CORS** properly

### Code Organization
- Separate concerns (controllers, services, models)
- Use **middleware** for cross-cutting concerns
- Implement proper **error handling**
- Use **environment variables** for configuration
- Follow **RESTful** conventions

## Dependencies

### Core Dependencies
- **express**: ^4.18.2
- **mongoose**: ^8.0.3 (MongoDB) or **sequelize**: ^6.35.0 (SQL)
- **dotenv**: ^16.3.1 (environment variables)
- **cors**: ^2.8.5 (CORS middleware)
- **helmet**: ^7.1.0 (security headers)

### Development Dependencies
- **nodemon**: ^3.0.2 (auto-restart)
- **jest**: ^29.7.0 (testing)
- **supertest**: ^6.3.3 (API testing)
- **eslint**: ^8.54.0 (linting)
- **prettier**: ^3.1.0 (formatting)

### Optional Dependencies
- **jsonwebtoken**: ^9.0.2 (JWT authentication)
- **bcrypt**: ^5.1.1 (password hashing)
- **express-validator**: ^7.0.1 (validation)
- **morgan**: ^1.10.0 (HTTP logging)
- **compression**: ^1.7.4 (response compression)

## Additional Resources

- [Node.js Official Documentation](https://nodejs.org/docs/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)

