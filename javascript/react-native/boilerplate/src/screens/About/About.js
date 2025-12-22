import React from 'react';
import { View, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import styles from './About.styles';

const About = () => {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>About</Text>
        <Text style={styles.text}>
          This is the About screen. You can add more information about your
          application here.
        </Text>
      </View>
    </SafeAreaView>
  );
};

export default About;

