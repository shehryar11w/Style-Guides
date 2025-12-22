# Next.js Style Guide and Design Patterns

## Overview

Next.js is a React framework for production that provides server-side rendering, static site generation, and API routes. This guide provides comprehensive style guidelines, directory patterns, and best practices for Next.js projects.

## Design Philosophy

- **File-based Routing**: Routes are created based on file structure
- **Server Components**: Leverage React Server Components for better performance
- **API Routes**: Build full-stack applications with built-in API routes
- **Optimization First**: Built-in image optimization, code splitting, and more
- **Production Ready**: Optimized for production from the start

## Directory Structure (App Router - Recommended)

```
next-app/
├── app/                               # App Router directory
│   ├── layout.jsx                     # Root layout
│   ├── page.jsx                       # Home page
│   ├── loading.jsx                     # Loading UI
│   ├── error.jsx                      # Error UI
│   ├── not-found.jsx                  # 404 page
│   ├── globals.css                    # Global styles
│   ├── (auth)/                       # Route groups
│   │   ├── login/
│   │   │   └── page.jsx
│   │   └── register/
│   │       └── page.jsx
│   ├── dashboard/
│   │   ├── layout.jsx                 # Nested layout
│   │   ├── page.jsx
│   │   └── settings/
│   │       └── page.jsx
│   └── api/                           # API routes
│       ├── users/
│       │   └── route.js
│       └── auth/
│           └── route.js
├── components/                        # Reusable components
│   ├── ui/                           # UI components
│   │   ├── Button/
│   │   ├── Input/
│   │   └── Modal/
│   ├── layout/                       # Layout components
│   │   ├── Header/
│   │   ├── Footer/
│   │   └── Sidebar/
│   └── features/                     # Feature components
│       ├── auth/
│       └── dashboard/
├── lib/                              # Utility libraries
│   ├── utils.js
│   ├── api.js
│   └── constants.js
├── hooks/                            # Custom React hooks
│   ├── useAuth.js
│   └── useLocalStorage.js
├── types/                            # TypeScript types (if using TS)
│   └── index.ts
├── public/                           # Static files
│   ├── images/
│   ├── icons/
│   └── favicon.ico
├── styles/                           # Global styles
│   └── variables.css
├── .env.local                        # Environment variables
├── .env.example
├── next.config.js                     # Next.js configuration
├── package.json
└── README.md
```

### Directory Structure (Pages Router - Legacy)

```
next-app/
├── pages/                            # Pages Router directory
│   ├── _app.jsx                      # Custom App component
│   ├── _document.jsx                 # Custom Document
│   ├── index.jsx                     # Home page
│   ├── about.jsx
│   ├── dashboard/
│   │   ├── index.jsx
│   │   └── settings.jsx
│   └── api/                          # API routes
│       ├── users.js
│       └── auth.js
├── components/                       # Same as App Router
├── lib/                              # Same as App Router
├── public/                           # Same as App Router
└── [other directories same as App Router]
```

### Directory Structure Explanation

- **`app/`**: App Router directory (Next.js 13+). Each folder represents a route
- **`pages/`**: Pages Router directory (legacy). Each file represents a route
- **`components/`**: Reusable React components organized by type
- **`lib/`**: Utility functions, API clients, and helper functions
- **`hooks/`**: Custom React hooks
- **`public/`**: Static assets served at the root URL
- **`app/api/`** or **`pages/api/`**: API route handlers

## Naming Conventions

### Files and Directories
- **Routes**: Use kebab-case for folders (`user-profile/`, `blog-posts/`)
- **Components**: PascalCase (`Button.jsx`, `UserProfile.jsx`)
- **Utilities**: camelCase (`helpers.js`, `apiClient.js`)
- **Constants**: UPPER_SNAKE_CASE (`API_URL`, `MAX_LENGTH`)
- **API Routes**: camelCase (`users.js`, `auth.js`)

### Next.js Specific
- **Page files**: `page.jsx` (App Router) or `index.jsx` (Pages Router)
- **Layout files**: `layout.jsx` (App Router)
- **Loading files**: `loading.jsx` (App Router)
- **Error files**: `error.jsx` (App Router)
- **Route handlers**: `route.js` (App Router) or `[name].js` (Pages Router)

### Components
- **Component names**: PascalCase (`Button`, `UserProfile`)
- **Props**: camelCase (`userName`, `isActive`, `onClick`)
- **Event handlers**: Prefix with `handle` (`handleClick`, `handleSubmit`)

## Code Style Guidelines

### JavaScript/JSX Style
- Use **2 spaces** for indentation
- Use **single quotes** for strings (or double quotes consistently)
- Use **semicolons** (or omit consistently)
- Maximum line length: **100 characters**
- Use **arrow functions** for callbacks
- Use **const** by default, **let** when needed

### Next.js-Specific Style
- Use **Server Components** by default (App Router)
- Mark Client Components with `'use client'` directive
- Use **async/await** for data fetching in Server Components
- Use **Next.js Image** component for images
- Use **next/link** for internal navigation

### Example Code Style

```jsx
// app/page.jsx (Server Component)
import Link from 'next/link';
import Button from '@/components/ui/Button/Button';

export default async function HomePage() {
  // Server Component can be async
  const data = await fetchData();

  return (
    <div>
      <h1>Welcome</h1>
      <Button>Get Started</Button>
      <Link href="/about">About</Link>
    </div>
  );
}

// components/ui/Button/Button.jsx (Client Component)
'use client';

import { useState } from 'react';
import styles from './Button.module.css';

export default function Button({ children, onClick }) {
  const [isPressed, setIsPressed] = useState(false);

  return (
    <button
      className={styles.button}
      onClick={onClick}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
    >
      {children}
    </button>
  );
}
```

## Component Patterns

### Server Component Pattern (App Router)

```jsx
// app/dashboard/page.jsx
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import DashboardContent from '@/components/features/dashboard/DashboardContent';

export default async function DashboardPage() {
  const session = await getServerSession();

  if (!session) {
    redirect('/login');
  }

  const data = await fetchDashboardData(session.user.id);

  return <DashboardContent data={data} />;
}
```

### Client Component Pattern

```jsx
// components/ui/Counter/Counter.jsx
'use client';

import { useState } from 'react';

export default function Counter({ initialValue = 0 }) {
  const [count, setCount] = useState(initialValue);

  return (
    <div>
      <button onClick={() => setCount(count - 1)}>-</button>
      <span>{count}</span>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}
```

### Layout Pattern

```jsx
// app/layout.jsx (Root Layout)
import Header from '@/components/layout/Header/Header';
import Footer from '@/components/layout/Footer/Footer';
import './globals.css';

export const metadata = {
  title: 'My App',
  description: 'Description of my app',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}

// app/dashboard/layout.jsx (Nested Layout)
export default function DashboardLayout({ children }) {
  return (
    <div className="dashboard-layout">
      <aside>Sidebar</aside>
      <main>{children}</main>
    </div>
  );
}
```

### API Route Pattern (App Router)

```jsx
// app/api/users/route.js
import { NextResponse } from 'next/server';

export async function GET(request) {
  try {
    const users = await getUsers();
    return NextResponse.json(users);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    );
  }
}

export async function POST(request) {
  try {
    const body = await request.json();
    const user = await createUser(body);
    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    );
  }
}
```

### API Route Pattern (Pages Router)

```jsx
// pages/api/users.js
export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const users = await getUsers();
      res.status(200).json(users);
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch users' });
    }
  } else if (req.method === 'POST') {
    try {
      const user = await createUser(req.body);
      res.status(201).json(user);
    } catch (error) {
      res.status(500).json({ error: 'Failed to create user' });
    }
  } else {
    res.setHeader('Allow', ['GET', 'POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
```

## State Management

### Server State (App Router)

```jsx
// Server Components fetch data directly
export default async function UserPage({ params }) {
  const user = await getUser(params.id);
  return <UserProfile user={user} />;
}
```

### Client State

```jsx
'use client';

import { useState, useEffect } from 'react';

export default function ClientComponent() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    // Client-side logic
  }, []);

  return <div>{count}</div>;
}
```

### Context API Pattern

```jsx
// lib/context/AuthContext.jsx
'use client';

import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check for existing session
    const checkAuth = async () => {
      const session = await getSession();
      setUser(session?.user || null);
    };
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

## Routing Patterns

### App Router Routing

```jsx
// app/page.jsx - Route: /
export default function HomePage() {
  return <div>Home</div>;
}

// app/about/page.jsx - Route: /about
export default function AboutPage() {
  return <div>About</div>;
}

// app/dashboard/page.jsx - Route: /dashboard
export default function DashboardPage() {
  return <div>Dashboard</div>;
}

// app/dashboard/settings/page.jsx - Route: /dashboard/settings
export default function SettingsPage() {
  return <div>Settings</div>;
}

// app/blog/[slug]/page.jsx - Dynamic route: /blog/[slug]
export default function BlogPostPage({ params }) {
  return <div>Post: {params.slug}</div>;
}

// app/shop/[...slug]/page.jsx - Catch-all route: /shop/[...slug]
export default function ShopPage({ params }) {
  return <div>Shop: {params.slug.join('/')}</div>;
}
```

### Navigation Pattern

```jsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();

  return (
    <nav>
      <Link
        href="/"
        className={pathname === '/' ? 'active' : ''}
      >
        Home
      </Link>
      <Link href="/about">About</Link>
      <Link href="/dashboard">Dashboard</Link>
    </nav>
  );
}
```

## API Integration

### Server-Side Data Fetching

```jsx
// app/users/page.jsx
async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    cache: 'no-store', // or 'force-cache', { revalidate: 3600 }
  });

  if (!res.ok) {
    throw new Error('Failed to fetch users');
  }

  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### Client-Side Data Fetching

```jsx
'use client';

import { useEffect, useState } from 'react';

export default function ClientUsersPage() {
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchUsers() {
      const res = await fetch('/api/users');
      const data = await res.json();
      setUsers(data);
      setIsLoading(false);
    }
    fetchUsers();
  }, []);

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### API Client Pattern

```jsx
// lib/api/client.js
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'An error occurred');
    }

    return data;
  }

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default new ApiClient();
```

## Testing Patterns

### Component Testing

```jsx
// components/ui/Button/Button.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## Best Practices

### Performance
- Use **Server Components** by default (App Router)
- Use **Next.js Image** component for optimized images
- Implement **code splitting** with dynamic imports
- Use **static generation** when possible
- Leverage **incremental static regeneration** (ISR)

### SEO
- Use **metadata** API (App Router) or **next/head** (Pages Router)
- Implement proper **semantic HTML**
- Use **structured data** when appropriate
- Optimize **meta tags** and **Open Graph** tags

### Security
- Validate and sanitize user input
- Use **environment variables** for secrets
- Implement **CSRF protection** for API routes
- Use **HTTPS** in production
- Sanitize data before rendering

### Code Organization
- Keep components small and focused
- Separate Server and Client Components
- Use **barrel exports** (index.js) for cleaner imports
- Group related files together
- Use **absolute imports** with `@/` alias

## Common Patterns

### Dynamic Routes Pattern

```jsx
// app/blog/[slug]/page.jsx
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({
    slug: post.slug,
  }));
}

export default async function BlogPostPage({ params }) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  );
}
```

### Loading and Error States

```jsx
// app/dashboard/loading.jsx
export default function Loading() {
  return <div>Loading dashboard...</div>;
}

// app/dashboard/error.jsx
'use client';

export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Middleware Pattern

```jsx
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(request) {
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/dashboard/:path*',
};
```

## Dependencies

### Core Dependencies
- **next**: ^14.0.0
- **react**: ^18.2.0
- **react-dom**: ^18.2.0

### Development Dependencies
- **@testing-library/react**: ^14.1.2
- **@testing-library/jest-dom**: ^6.1.5
- **eslint**: ^8.54.0
- **eslint-config-next**: ^14.0.0
- **prettier**: ^3.1.0

### Optional Dependencies
- **next-auth**: ^4.24.5 (authentication)
- **zustand**: ^4.4.7 (state management)
- **axios**: ^1.6.2 (HTTP client)
- **tailwindcss**: ^3.3.6 (styling)
- **typescript**: ^5.3.3 (if using TypeScript)

## Additional Resources

- [Next.js Official Documentation](https://nextjs.org/docs)
- [Next.js App Router Guide](https://nextjs.org/docs/app)
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)

