# React Native Style Guide and Design Patterns

## Overview

React Native is a framework for building native mobile applications using React. This guide provides comprehensive style guidelines, directory patterns, and best practices for React Native projects.

## Design Philosophy

- **Learn Once, Write Anywhere**: Use React to build native apps for iOS and Android
- **Native Performance**: Components compile to native views
- **Platform-Specific**: Leverage platform-specific features when needed
- **Component-Based**: Build reusable, composable components
- **Declarative**: Describe UI state, React Native handles rendering

## Directory Structure

```
react-native-app/
├── android/                          # Android native code
│   ├── app/
│   ├── build.gradle
│   └── src/
├── ios/                              # iOS native code
│   ├── [AppName]/
│   ├── Podfile
│   └── [AppName].xcodeproj/
├── src/
│   ├── components/                   # Reusable UI components
│   │   ├── common/                  # Common/shared components
│   │   │   ├── Button/
│   │   │   │   ├── Button.js
│   │   │   │   ├── Button.styles.js
│   │   │   │   └── index.js
│   │   │   ├── Input/
│   │   │   └── Card/
│   │   ├── layout/                  # Layout components
│   │   │   ├── Header/
│   │   │   ├── Footer/
│   │   │   └── Container/
│   │   └── features/                # Feature-specific components
│   │       ├── auth/
│   │       └── profile/
│   ├── screens/                     # Screen components
│   │   ├── Home/
│   │   │   ├── Home.js
│   │   │   ├── Home.styles.js
│   │   │   └── index.js
│   │   ├── Login/
│   │   ├── Profile/
│   │   └── Dashboard/
│   ├── navigation/                  # Navigation configuration
│   │   ├── AppNavigator.js
│   │   ├── AuthNavigator.js
│   │   └── TabNavigator.js
│   ├── hooks/                       # Custom React hooks
│   │   ├── useAuth.js
│   │   ├── useApi.js
│   │   └── useKeyboard.js
│   ├── services/                    # API and external services
│   │   ├── api/
│   │   │   ├── client.js
│   │   │   ├── endpoints.js
│   │   │   └── auth.js
│   │   └── storage.js
│   ├── utils/                       # Utility functions
│   │   ├── helpers.js
│   │   ├── constants.js
│   │   ├── validators.js
│   │   └── formatters.js
│   ├── store/                       # State management (Redux/Zustand)
│   │   ├── slices/
│   │   ├── store.js
│   │   └── hooks.js
│   ├── assets/                      # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   ├── theme/                       # Theme configuration
│   │   ├── colors.js
│   │   ├── typography.js
│   │   └── spacing.js
│   ├── types/                       # TypeScript types (if using TS)
│   │   └── index.ts
│   └── App.js                       # Root component
├── .env                             # Environment variables
├── .env.example
├── .gitignore
├── package.json
├── babel.config.js
├── metro.config.js
├── app.json                         # App configuration
└── README.md
```

### Directory Structure Explanation

- **`src/components/`**: Reusable UI components organized by type
- **`src/screens/`**: Screen-level components representing app screens
- **`src/navigation/`**: Navigation configuration and navigators
- **`src/hooks/`**: Custom React hooks for reusable logic
- **`src/services/`**: API clients and external service integrations
- **`src/utils/`**: Pure utility functions and helpers
- **`src/store/`**: State management setup (Redux, Zustand, etc.)
- **`src/assets/`**: Images, icons, fonts, and other static assets
- **`src/theme/`**: Theme configuration (colors, typography, spacing)
- **`android/`** and **`ios/`**: Platform-specific native code

## Naming Conventions

### Files and Directories
- **Components**: PascalCase (`Button.js`, `UserProfile.js`)
- **Screens**: PascalCase (`Home.js`, `LoginScreen.js`)
- **Hooks**: camelCase starting with `use` (`useAuth.js`, `useApi.js`)
- **Utilities**: camelCase (`helpers.js`, `validators.js`)
- **Constants**: UPPER_SNAKE_CASE (`API_URL`, `MAX_LENGTH`)
- **Directories**: camelCase (`userProfile/`, `auth/`)

### Components
- **Component names**: PascalCase (`Button`, `UserProfile`, `NavigationBar`)
- **Props**: camelCase (`userName`, `isActive`, `onPress`)
- **Event handlers**: Prefix with `handle` (`handlePress`, `handleSubmit`)
- **Boolean props**: Prefix with `is`, `has`, or `should` (`isActive`, `hasError`)

### Styles
- **Style files**: `[ComponentName].styles.js`
- **Style objects**: camelCase (`container`, `buttonStyle`, `textStyle`)

## Code Style Guidelines

### JavaScript/JSX Style
- Use **2 spaces** for indentation
- Use **single quotes** for strings (or double quotes consistently)
- Use **semicolons** (or omit consistently)
- Maximum line length: **100 characters**
- Use **arrow functions** for callbacks
- Use **const** by default, **let** when needed

### React Native-Specific Style
- Use **functional components** with hooks
- Use **StyleSheet.create()** for styles
- Use **Platform.select()** for platform-specific code
- Keep components **small and focused**
- Extract reusable logic into **custom hooks**

### Example Code Style

```jsx
// components/common/Button/Button.js
import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator } from 'react-native';
import PropTypes from 'prop-types';
import styles from './Button.styles';

const Button = ({ title, onPress, loading = false, disabled = false }) => {
  return (
    <TouchableOpacity
      style={[styles.button, disabled && styles.disabled]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator color="#fff" />
      ) : (
        <Text style={styles.text}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

Button.propTypes = {
  title: PropTypes.string.isRequired,
  onPress: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  disabled: PropTypes.bool,
};

export default Button;

// components/common/Button/Button.styles.js
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#007AFF',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default styles;
```

## Component Patterns

### Screen Component Pattern

```jsx
// screens/Home/Home.js
import React from 'react';
import { View, Text, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import Button from '../../components/common/Button/Button';
import styles from './Home.styles';

const Home = ({ navigation }) => {
  const handlePress = () => {
    navigation.navigate('About');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Welcome</Text>
        <Button title="Go to About" onPress={handlePress} />
      </ScrollView>
    </SafeAreaView>
  );
};

export default Home;
```

### Custom Hook Pattern

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

export default useApi;
```

### Platform-Specific Code Pattern

```jsx
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.select({
      ios: 20,
      android: 10,
    }),
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
      },
      android: {
        elevation: 5,
      },
    }),
  },
});
```

## State Management

### useState Hook

```jsx
import React, { useState } from 'react';
import { View, TextInput, Text } from 'react-native';

const SearchInput = () => {
  const [query, setQuery] = useState('');

  return (
    <View>
      <TextInput
        value={query}
        onChangeText={setQuery}
        placeholder="Search..."
      />
      <Text>You typed: {query}</Text>
    </View>
  );
};
```

### Context API Pattern

```jsx
// context/AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = async (credentials) => {
    // Login logic
    const userData = await authenticate(credentials);
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated, login, logout }}
    >
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

## Navigation Patterns

### React Navigation Setup

```jsx
// navigation/AppNavigator.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Home from '../screens/Home/Home';
import About from '../screens/About/About';
import Login from '../screens/Login/Login';

const Stack = createStackNavigator();

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#007AFF',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen name="Home" component={Home} />
        <Stack.Screen name="About" component={About} />
        <Stack.Screen name="Login" component={Login} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
```

### Tab Navigator Pattern

```jsx
// navigation/TabNavigator.js
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Home from '../screens/Home/Home';
import Profile from '../screens/Profile/Profile';
import Settings from '../screens/Settings/Settings';

const Tab = createBottomTabNavigator();

const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#999',
      }}
    >
      <Tab.Screen name="Home" component={Home} />
      <Tab.Screen name="Profile" component={Profile} />
      <Tab.Screen name="Settings" component={Settings} />
    </Tab.Navigator>
  );
};

export default TabNavigator;
```

## API Integration

### API Client Pattern

```jsx
// services/api/client.js
const API_BASE_URL = process.env.API_BASE_URL || 'https://api.example.com';

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
    const token = await AsyncStorage.getItem('token');
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

export default new ApiClient(API_BASE_URL);
```

### AsyncStorage Pattern

```jsx
// services/storage.js
import AsyncStorage from '@react-native-async-storage/async-storage';

export const storage = {
  async getItem(key) {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Error reading from storage:', error);
      return null;
    }
  },

  async setItem(key, value) {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error writing to storage:', error);
    }
  },

  async removeItem(key) {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing from storage:', error);
    }
  },
};
```

## Testing Patterns

### Component Testing

```jsx
// components/common/Button/Button.test.js
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import Button from './Button';

describe('Button', () => {
  it('renders with title', () => {
    const { getByText } = render(<Button title="Click me" onPress={() => {}} />);
    expect(getByText('Click me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    const { getByText } = render(<Button title="Click me" onPress={onPress} />);

    fireEvent.press(getByText('Click me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

## Best Practices

### Performance
- Use **FlatList** or **SectionList** for long lists
- Implement **memoization** with `React.memo()` and `useMemo()`
- Use **Image** component with proper sizing
- Avoid inline functions in render
- Use **InteractionManager** for heavy operations

### Code Organization
- Keep components small and focused
- Extract reusable logic into custom hooks
- Separate styles into dedicated files
- Use consistent naming conventions
- Group related files together

### Platform Considerations
- Test on both iOS and Android
- Use **Platform.select()** for platform-specific code
- Handle different screen sizes and orientations
- Consider safe areas (notches, status bars)
- Test on physical devices, not just simulators

### Security
- Never store sensitive data in AsyncStorage
- Use secure storage for tokens and credentials
- Validate and sanitize user input
- Use HTTPS for API calls
- Implement proper authentication flows

## Common Patterns

### Safe Area Pattern

```jsx
import { SafeAreaView } from 'react-native-safe-area-context';

const Screen = () => {
  return (
    <SafeAreaView style={styles.container} edges={['top', 'bottom']}>
      {/* Content */}
    </SafeAreaView>
  );
};
```

### Loading State Pattern

```jsx
import { ActivityIndicator, View } from 'react-native';

const DataScreen = () => {
  const { data, isLoading, error } = useApi(fetchData);

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  if (error) {
    return <ErrorView message={error} />;
  }

  return <DataView data={data} />;
};
```

### Form Pattern

```jsx
import { useState } from 'react';
import { View, TextInput, Button } from 'react-native';

const LoginForm = ({ onSubmit }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    onSubmit({ email, password });
  };

  return (
    <View>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="Email"
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        secureTextEntry
      />
      <Button title="Login" onPress={handleSubmit} />
    </View>
  );
};
```

## Dependencies

### Core Dependencies
- **react**: ^18.2.0
- **react-native**: ^0.72.0
- **@react-navigation/native**: ^6.1.9
- **@react-navigation/stack**: ^6.3.20
- **@react-navigation/bottom-tabs**: ^6.5.11

### Development Dependencies
- **@testing-library/react-native**: ^12.4.2
- **@testing-library/jest-native**: ^5.4.3
- **jest**: ^29.7.0
- **metro-react-native-babel-preset**: ^0.76.8

### Optional Dependencies
- **@react-native-async-storage/async-storage**: ^1.19.5
- **react-native-safe-area-context**: ^4.8.2
- **zustand**: ^4.4.7 (state management)
- **axios**: ^1.6.2 (HTTP client)
- **react-native-vector-icons**: ^10.0.2 (icons)

## Additional Resources

- [React Native Official Documentation](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [React Native Community](https://github.com/react-native-community)

