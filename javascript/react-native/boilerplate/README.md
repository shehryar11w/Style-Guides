# React Native App Boilerplate

A complete React Native application boilerplate following best practices and design patterns.

## Prerequisites

- Node.js (>=18)
- React Native CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. iOS Setup (macOS only)

```bash
cd ios
pod install
cd ..
```

### 3. Run on iOS

```bash
npm run ios
```

### 4. Run on Android

```bash
npm run android
```

### 5. Start Metro Bundler

```bash
npm start
```

## Project Structure

- `src/components/`: Reusable UI components
- `src/screens/`: Screen-level components
- `src/navigation/`: Navigation configuration
- `src/services/`: API clients and external services
- `src/utils/`: Utility functions and helpers
- `src/theme/`: Theme configuration (colors, typography, spacing)
- `android/`: Android native code
- `ios/`: iOS native code

## Available Scripts

- `npm start`: Start Metro bundler
- `npm run android`: Run on Android
- `npm run ios`: Run on iOS
- `npm test`: Run tests
- `npm run lint`: Lint code

## Features

- React Navigation setup
- Safe area handling
- API client with authentication
- AsyncStorage utilities
- Theme configuration
- Component and screen examples

## Adding New Features

1. **Create a new screen**:
   - Add screen in `src/screens/`
   - Add route in `src/navigation/AppNavigator.js`

2. **Create a new component**:
   - Add component in `src/components/`
   - Follow the component structure pattern

3. **Add navigation**:
   - Update `src/navigation/AppNavigator.js`
   - Use React Navigation components

## Development

- Use functional components with hooks
- Follow the naming conventions
- Use StyleSheet.create() for styles
- Test on both iOS and Android
- Use Platform.select() for platform-specific code

## Notes

This boilerplate uses React Native CLI. For Expo-based projects, use `npx create-expo-app` instead.

