# React Style Guide and Design Patterns

## Overview

React is a JavaScript library for building user interfaces, particularly web applications. This guide provides comprehensive style guidelines, directory patterns, and best practices for React projects.

## Design Philosophy

- **Component-Based**: Build encapsulated components that manage their own state
- **Declarative**: Describe what the UI should look like, React handles the updates
- **Unidirectional Data Flow**: Data flows down, events flow up
- **Composition over Inheritance**: Build complex UIs from simple components

## Directory Structure

```
react-app/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── components/                    # Reusable UI components
│   │   ├── common/                   # Common/shared components
│   │   │   ├── Button/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Button.module.css
│   │   │   │   ├── Button.test.js
│   │   │   │   └── index.js
│   │   │   ├── Input/
│   │   │   └── Modal/
│   │   ├── layout/                   # Layout components
│   │   │   ├── Header/
│   │   │   ├── Footer/
│   │   │   ├── Sidebar/
│   │   │   └── Layout.jsx
│   │   └── features/                 # Feature-specific components
│   │       ├── auth/
│   │       └── dashboard/
│   ├── pages/                        # Page-level components
│   │   ├── Home/
│   │   │   ├── Home.jsx
│   │   │   ├── Home.module.css
│   │   │   └── index.js
│   │   ├── About/
│   │   ├── Login/
│   │   └── Dashboard/
│   ├── hooks/                        # Custom React hooks
│   │   ├── useAuth.js
│   │   ├── useLocalStorage.js
│   │   ├── useApi.js
│   │   └── useDebounce.js
│   ├── context/                      # React Context providers
│   │   ├── AuthContext.jsx
│   │   ├── ThemeContext.jsx
│   │   └── index.js
│   ├── services/                     # API and external services
│   │   ├── api/
│   │   │   ├── client.js
│   │   │   ├── endpoints.js
│   │   │   └── auth.js
│   │   └── storage.js
│   ├── utils/                        # Utility functions
│   │   ├── helpers.js
│   │   ├── constants.js
│   │   ├── validators.js
│   │   └── formatters.js
│   ├── store/                        # State management (if using Redux/Zustand)
│   │   ├── slices/
│   │   ├── store.js
│   │   └── hooks.js
│   ├── styles/                       # Global styles
│   │   ├── variables.css
│   │   ├── reset.css
│   │   └── global.css
│   ├── assets/                       # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   ├── types/                        # TypeScript types (if using TS)
│   │   └── index.ts
│   ├── App.jsx                       # Root component
│   ├── App.css
│   ├── index.js                      # Entry point
│   └── index.css
├── .env                              # Environment variables
├── .env.example
├── .gitignore
├── package.json
├── package-lock.json
└── README.md
```

### Directory Structure Explanation

- **`components/`**: Reusable UI components organized by type (common, layout, features)
- **`pages/`**: Page-level components representing routes
- **`hooks/`**: Custom React hooks for reusable logic
- **`context/`**: React Context providers for global state
- **`services/`**: API clients and external service integrations
- **`utils/`**: Pure utility functions and helpers
- **`store/`**: State management setup (Redux, Zustand, etc.)
- **`styles/`**: Global styles, CSS variables, and resets
- **`assets/`**: Images, icons, fonts, and other static files

## Naming Conventions

### Files and Directories
- **Components**: PascalCase (`Button.jsx`, `UserProfile.jsx`)
- **Hooks**: camelCase starting with `use` (`useAuth.js`, `useLocalStorage.js`)
- **Utilities**: camelCase (`helpers.js`, `validators.js`)
- **Constants**: UPPER_SNAKE_CASE or camelCase (`API_URL`, `maxLength`)
- **Directories**: camelCase or kebab-case (`user-profile/`, `auth/`)

### Components
- **Component names**: PascalCase (`Button`, `UserProfile`, `NavigationBar`)
- **Props**: camelCase (`userName`, `isActive`, `onClick`)
- **Event handlers**: Prefix with `handle` (`handleClick`, `handleSubmit`)
- **Boolean props**: Prefix with `is`, `has`, or `should` (`isActive`, `hasError`, `shouldRender`)

### Variables and Functions
- **Variables**: camelCase (`userName`, `isLoading`, `apiResponse`)
- **Functions**: camelCase (`getUserData`, `formatDate`, `validateEmail`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_LENGTH`, `API_BASE_URL`)
- **Private functions**: Prefix with underscore (`_internalHelper`)

## Code Style Guidelines

### JavaScript/JSX Style
- Use **2 spaces** for indentation
- Use **single quotes** for strings (or double quotes consistently)
- Use **semicolons** (or omit consistently)
- Maximum line length: **100 characters**
- Use **arrow functions** for callbacks and methods
- Use **const** by default, **let** when reassignment needed, avoid **var**

### React-Specific Style
- Use **functional components** with hooks (avoid class components)
- Use **JSX** for markup
- Use **destructuring** for props and state
- Keep components **small and focused** (single responsibility)
- Extract logic into **custom hooks** when reusable

### Example Code Style

```jsx
// Good
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Button from '../common/Button/Button';
import { fetchUserData } from '../../services/api/user';
import styles from './UserProfile.module.css';

const UserProfile = ({ userId, onUpdate }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadUser = async () => {
      try {
        setIsLoading(true);
        const userData = await fetchUserData(userId);
        setUser(userData);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, [userId]);

  const handleUpdate = () => {
    onUpdate(user);
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return null;

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{user.name}</h2>
      <p className={styles.email}>{user.email}</p>
      <Button onClick={handleUpdate}>Update Profile</Button>
    </div>
  );
};

UserProfile.propTypes = {
  userId: PropTypes.string.isRequired,
  onUpdate: PropTypes.func,
};

UserProfile.defaultProps = {
  onUpdate: () => {},
};

export default UserProfile;

// Bad
import React from 'react';

function userProfile(props) {  // Wrong naming, no destructuring
  const [user, setUser] = React.useState(null);  // Should import useState
  const [loading, setLoading] = React.useState(true);  // Inconsistent naming

  React.useEffect(() => {  // Should import useEffect
    fetch(`/api/users/${props.userId}`)  // No error handling, inline fetch
      .then(res => res.json())
      .then(data => setUser(data))
      .then(() => setLoading(false));
  }, []);  // Missing dependency

  return <div><h2>{user.name}</h2></div>;  // No error handling, no loading state
}

export default userProfile;
```

## Component Patterns

### Functional Component Pattern

```jsx
import React from 'react';
import PropTypes from 'prop-types';

const ComponentName = ({ prop1, prop2, optionalProp }) => {
  // Component logic here
  
  return (
    <div>
      {/* JSX here */}
    </div>
  );
};

ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number.isRequired,
  optionalProp: PropTypes.bool,
};

ComponentName.defaultProps = {
  optionalProp: false,
};

export default ComponentName;
```

### Component with Hooks Pattern

```jsx
import React, { useState, useEffect, useCallback } from 'react';

const DataFetcher = ({ url }) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return null;

  return <div>{/* Render data */}</div>;
};
```

### Compound Components Pattern

```jsx
import React, { createContext, useContext } from 'react';

const AccordionContext = createContext();

const Accordion = ({ children, defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <AccordionContext.Provider value={{ isOpen, setIsOpen }}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
};

const AccordionHeader = ({ children }) => {
  const { isOpen, setIsOpen } = useContext(AccordionContext);

  return (
    <button onClick={() => setIsOpen(!isOpen)}>
      {children} {isOpen ? '▼' : '▶'}
    </button>
  );
};

const AccordionContent = ({ children }) => {
  const { isOpen } = useContext(AccordionContext);

  if (!isOpen) return null;

  return <div className="accordion-content">{children}</div>;
};

Accordion.Header = AccordionHeader;
Accordion.Content = AccordionContent;

// Usage
<Accordion>
  <Accordion.Header>Title</Accordion.Header>
  <Accordion.Content>Content here</Accordion.Content>
</Accordion>
```

### Render Props Pattern

```jsx
const DataProvider = ({ url, children }) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .finally(() => setIsLoading(false));
  }, [url]);

  return children({ data, isLoading });
};

// Usage
<DataProvider url="/api/users">
  {({ data, isLoading }) => (
    isLoading ? <div>Loading...</div> : <UserList users={data} />
  )}
</DataProvider>
```

## State Management

### useState Hook

```jsx
import React, { useState } from 'react';

const Counter = () => {
  const [count, setCount] = useState(0);

  const increment = () => setCount(prev => prev + 1);
  const decrement = () => setCount(prev => prev - 1);

  return (
    <div>
      <button onClick={decrement}>-</button>
      <span>{count}</span>
      <button onClick={increment}>+</button>
    </div>
  );
};
```

### useReducer Hook (for complex state)

```jsx
import React, { useReducer } from 'react';

const initialState = { count: 0, step: 1 };

const reducer = (state, action) => {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'decrement':
      return { ...state, count: state.count - state.step };
    case 'setStep':
      return { ...state, step: action.payload };
    default:
      return state;
  }
};

const Counter = () => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <input
        type="number"
        value={state.step}
        onChange={e => dispatch({ type: 'setStep', payload: Number(e.target.value) })}
      />
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <span>{state.count}</span>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </div>
  );
};
```

### Context API Pattern

```jsx
// context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        // Validate token and get user
        const userData = await validateToken(token);
        setUser(userData);
      }
      setIsLoading(false);
    };
    checkAuth();
  }, []);

  const login = async (credentials) => {
    const { user, token } = await authenticate(credentials);
    localStorage.setItem('token', token);
    setUser(user);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### Custom Hooks Pattern

```jsx
// hooks/useLocalStorage.js
import { useState, useEffect } from 'react';

const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
};

// hooks/useDebounce.js
import { useState, useEffect } from 'react';

const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};
```

## Routing Patterns

### React Router Pattern

```jsx
// App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import PrivateRoute from './components/common/PrivateRoute/PrivateRoute';

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

// components/common/PrivateRoute/PrivateRoute.jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext';

const PrivateRoute = ({ children }) => {
  const { user, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;

  return children;
};
```

## API Integration

### API Service Pattern

```jsx
// services/api/client.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'An error occurred');
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  get(endpoint, options) {
    return this.request(endpoint, { ...options, method: 'GET' });
  }

  post(endpoint, data, options) {
    return this.request(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  put(endpoint, data, options) {
    return this.request(endpoint, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  delete(endpoint, options) {
    return this.request(endpoint, { ...options, method: 'DELETE' });
  }
}

export default new ApiClient(API_BASE_URL);

// services/api/user.js
import apiClient from './client';

export const userService = {
  getAll: () => apiClient.get('/users'),
  getById: (id) => apiClient.get(`/users/${id}`),
  create: (data) => apiClient.post('/users', data),
  update: (id, data) => apiClient.put(`/users/${id}`, data),
  delete: (id) => apiClient.delete(`/users/${id}`),
};
```

### Custom Hook for API Calls

```jsx
// hooks/useApi.js
import { useState, useEffect } from 'react';

const useApi = (apiFunction, dependencies = []) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const result = await apiFunction();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  return { data, isLoading, error };
};
```

## Testing Patterns

### Component Testing with React Testing Library

```jsx
// components/common/Button/Button.test.js
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

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

## Best Practices

### Performance
- Use `React.memo()` for expensive components
- Use `useMemo()` for expensive calculations
- Use `useCallback()` for stable function references
- Code split with `React.lazy()` and `Suspense`
- Avoid inline object/array creation in render

### Code Organization
- Keep components small and focused
- Extract reusable logic into custom hooks
- Separate concerns (UI, logic, data)
- Use composition over inheritance
- Group related files together

### Accessibility
- Use semantic HTML elements
- Provide proper ARIA labels
- Ensure keyboard navigation works
- Maintain proper heading hierarchy
- Test with screen readers

### Security
- Sanitize user input
- Use HTTPS in production
- Validate data on both client and server
- Avoid storing sensitive data in localStorage
- Use Content Security Policy headers

## Common Patterns

### Error Boundary Pattern

```jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong.</h2>
          <p>{this.state.error?.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### Higher-Order Component Pattern

```jsx
const withLoading = (Component) => {
  return ({ isLoading, ...props }) => {
    if (isLoading) {
      return <div>Loading...</div>;
    }
    return <Component {...props} />;
  };
};

// Usage
const UserProfileWithLoading = withLoading(UserProfile);
```

## Dependencies

### Core Dependencies
- **react**: ^18.2.0
- **react-dom**: ^18.2.0
- **react-router-dom**: ^6.20.0 (for routing)

### Development Dependencies
- **@testing-library/react**: ^14.1.2
- **@testing-library/jest-dom**: ^6.1.5
- **@testing-library/user-event**: ^14.5.1
- **eslint**: ^8.54.0
- **eslint-plugin-react**: ^7.33.2
- **prettier**: ^3.1.0

### Optional Dependencies
- **axios**: ^1.6.2 (HTTP client)
- **zustand**: ^4.4.7 (state management)
- **react-query**: ^3.39.3 (data fetching)
- **styled-components**: ^6.1.6 (CSS-in-JS)
- **prop-types**: ^15.8.1 (runtime type checking)

## Additional Resources

- [React Official Documentation](https://react.dev/)
- [React Patterns](https://reactpatterns.com/)
- [React Testing Library](https://testing-library.com/react)

