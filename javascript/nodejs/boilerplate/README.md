# Node.js Express Application Boilerplate

A complete Node.js Express application boilerplate following best practices and design patterns.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/nodejs-app
JWT_SECRET=your-secret-key-here
JWT_EXPIRE=7d
```

### 3. Start MongoDB

Make sure MongoDB is running on your system or use a cloud MongoDB instance.

### 4. Run Development Server

```bash
npm run dev
```

The server will be available at `http://localhost:3000`

### 5. Run Production Server

```bash
npm start
```

## Project Structure

- `src/app.js`: Express application setup
- `src/routes/`: Route definitions
- `src/controllers/`: Request handlers
- `src/services/`: Business logic
- `src/models/`: Database models (Mongoose)
- `src/middleware/`: Custom middleware
- `src/utils/`: Utility functions
- `src/config/`: Configuration files
- `src/validators/`: Request validation

## Available Endpoints

- `GET /health`: Health check
- `POST /api/v1/auth/register`: Register new user
- `POST /api/v1/auth/login`: User login
- `GET /api/v1/users`: Get all users (authenticated)
- `GET /api/v1/users/:id`: Get user by ID (authenticated)
- `POST /api/v1/users`: Create user (authenticated)
- `PUT /api/v1/users/:id`: Update user (authenticated)
- `DELETE /api/v1/users/:id`: Delete user (authenticated)

## Available Scripts

- `npm start`: Start production server
- `npm run dev`: Start development server with nodemon
- `npm test`: Run tests
- `npm run lint`: Lint code
- `npm run format`: Format code with Prettier

## Development

- Use async/await for asynchronous operations
- Follow RESTful conventions
- Implement proper error handling
- Use middleware for cross-cutting concerns
- Validate all inputs

## Testing

```bash
npm test
```

## Production Deployment

1. Set `NODE_ENV=production` in `.env`
2. Use process manager (PM2) for running the app
3. Set up proper logging
4. Configure CORS properly
5. Use HTTPS
6. Set up monitoring and error tracking

