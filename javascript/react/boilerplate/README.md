# React App Boilerplate

A complete React application boilerplate following best practices and design patterns.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

### 5. Preview Production Build

```bash
npm run preview
```

## Project Structure

- `src/components/`: Reusable UI components
- `src/pages/`: Page-level components
- `src/hooks/`: Custom React hooks
- `src/services/`: API clients and external services
- `src/utils/`: Utility functions and helpers
- `src/styles/`: Global styles and CSS variables
- `public/`: Static assets

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build
- `npm test`: Run tests
- `npm run lint`: Lint code
- `npm run format`: Format code with Prettier

## Adding New Features

1. **Create a new component**:
   - Add component in `src/components/`
   - Follow the component structure pattern
   - Include PropTypes and tests

2. **Create a new page**:
   - Add page in `src/pages/`
   - Add route in `src/App.jsx`

3. **Add a custom hook**:
   - Create hook in `src/hooks/`
   - Use the `use` prefix for naming

## Development

- Use functional components with hooks
- Follow the naming conventions
- Write tests for components
- Use CSS Modules for styling
- Keep components small and focused

