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
        <Text style={styles.title}>Welcome to React Native App</Text>
        <Text style={styles.description}>
          This is a boilerplate React Native application following best
          practices and design patterns.
        </Text>
        <Button title="Go to About" onPress={handlePress} />
      </ScrollView>
    </SafeAreaView>
  );
};

export default Home;

