# Next.js App Boilerplate

A complete Next.js application boilerplate following best practices and design patterns using the App Router.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
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

### 5. Start Production Server

```bash
npm start
```

## Project Structure

- `app/`: App Router directory with routes and layouts
- `components/`: Reusable React components
- `lib/`: Utility functions and API clients
- `public/`: Static assets
- `app/api/`: API route handlers

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm start`: Start production server
- `npm run lint`: Lint code

## Features

- App Router (Next.js 13+)
- Server Components by default
- API routes
- Error and loading states
- Absolute imports with `@/` alias
- CSS Modules for styling

## Adding New Features

1. **Create a new page**:
   - Add `page.jsx` in `app/[route]/`
   - Pages are automatically routed

2. **Create a new API route**:
   - Add `route.js` in `app/api/[endpoint]/`
   - Export GET, POST, PUT, DELETE functions

3. **Add a component**:
   - Add component in `components/`
   - Use Server Components by default
   - Mark with `'use client'` for Client Components

## Development

- Use Server Components for data fetching
- Mark Client Components with `'use client'`
- Use Next.js Image component for images
- Use next/link for internal navigation
- Follow the naming conventions

