import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, StatusBar } from 'react-native';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar backgroundColor="#667eea" />
      <View style={styles.content}>
        <Text style={styles.title}>🚀 AI Travel Assistant</Text>
        <Text style={styles.subtitle}>Mobile App Ready!</Text>
        <Text style={styles.text}>
          Open terminal and run: npm start
        </Text>
        <Text style={styles.text}>
          Then scan QR code with Expo Go app
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#667eea',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 20,
    color: 'rgba(255,255,255,0.8)',
    marginBottom: 30,
  },
  text: {
    fontSize: 16,
    color: 'white',
    textAlign: 'center',
    marginBottom: 10,
  },
});