import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  SafeAreaView,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { travelService } from '../services/travel';
import { authService } from '../services/auth';

const HomeScreen = ({ navigation }: any) => {
  const [user, setUser] = useState<any>(null);
  const [recentTrips, setRecentTrips] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const isLoggedIn = await authService.isLoggedIn();
      if (isLoggedIn) {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      }

      const trips = await travelService.getRecentTrips(3);
      setRecentTrips(trips.trips || []);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const QuickAction = ({ icon, title, onPress, color }: any) => (
    <TouchableOpacity style={styles.quickAction} onPress={onPress}>
      <View style={[styles.quickActionIcon, { backgroundColor: color }]}>
        <Ionicons name={icon} size={24} color="#fff" />
      </View>
      <Text style={styles.quickActionText}>{title}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar backgroundColor="#667eea" barStyle="light-content" />

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>
              {user ? `Hello, ${user.username}!` : 'Hello, Traveler!'}
            </Text>
            <Text style={styles.subtitle}>Ready for your next adventure?</Text>
          </View>
          <TouchableOpacity onPress={() => navigation.navigate('Profile')}>
            <View style={styles.avatar}>
              <Ionicons name="person" size={24} color="#667eea" />
            </View>
          </TouchableOpacity>
        </View>

        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <View style={styles.quickActionsGrid}>
            <QuickAction
              icon="airplane"
              title="Plan Trip"
              color="#667eea"
              onPress={() => navigation.navigate('Travel')}
            />
            <QuickAction
              icon="search"
              title="Find Flights"
              color="#4CAF50"
              onPress={() => navigation.navigate('Flights')}
            />
            <QuickAction
              icon="bed"
              title="Book Hotels"
              color="#FF9800"
              onPress={() => navigation.navigate('Hotels')}
            />
            <QuickAction
              icon="chatbubbles"
              title="AI Assistant"
              color="#9C27B0"
              onPress={() => navigation.navigate('Chat')}
            />
          </View>
        </View>

        {/* Recent Trips */}
        {recentTrips.length > 0 && (
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Recent Trips</Text>
              <TouchableOpacity onPress={() => navigation.navigate('Travel')}>
                <Text style={styles.seeAll}>See All</Text>
              </TouchableOpacity>
            </View>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {recentTrips.map((trip) => (
                <TouchableOpacity key={trip.id} style={styles.tripCard}>
                  <View style={styles.tripCardHeader}>
                    <Ionicons name="location" size={20} color="#667eea" />
                    <Text style={styles.tripDestination}>{trip.destination}</Text>
                  </View>
                  <Text style={styles.tripDays}>{trip.days} days</Text>
                  <Text style={styles.tripCost}>${trip.budget}</Text>
                  <View style={styles.tripStatus}>
                    <Text style={styles.tripStatusText}>{trip.status}</Text>
                  </View>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        )}

        {/* Popular Destinations */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Popular Destinations</Text>
          <View style={styles.destinationsGrid}>
            {['Tokyo', 'Paris', 'New York', 'Bali'].map((city) => (
              <TouchableOpacity
                key={city}
                style={styles.destinationCard}
                onPress={() => navigation.navigate('Travel', { destination: city })}
              >
                <View style={styles.destinationImage}>
                  <Ionicons name="location" size={30} color="#fff" />
                </View>
                <Text style={styles.destinationName}>{city}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* AI Assistant Card */}
        <TouchableOpacity
          style={styles.aiCard}
          onPress={() => navigation.navigate('Chat')}
        >
          <View style={styles.aiCardContent}>
            <View style={styles.aiIcon}>
              <Ionicons name="sparkles" size={30} color="#fff" />
            </View>
            <View style={styles.aiText}>
              <Text style={styles.aiTitle}>Need travel advice?</Text>
              <Text style={styles.aiSubtitle}>Chat with our AI assistant</Text>
            </View>
            <Ionicons name="chevron-forward" size={24} color="#667eea" />
          </View>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#667eea',
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 4,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  section: {
    padding: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  seeAll: {
    fontSize: 14,
    color: '#667eea',
    fontWeight: '500',
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  quickAction: {
    width: '48%',
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  quickActionIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  quickActionText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    textAlign: 'center',
  },
  tripCard: {
    width: 200,
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 15,
    marginRight: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  tripCardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  tripDestination: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 8,
  },
  tripDays: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  tripCost: {
    fontSize: 16,
    fontWeight: '600',
    color: '#667eea',
    marginBottom: 10,
  },
  tripStatus: {
    backgroundColor: '#e3f2fd',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
  },
  tripStatusText: {
    fontSize: 12,
    color: '#1976d2',
    fontWeight: '500',
  },
  destinationsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  destinationCard: {
    width: '48%',
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  destinationImage: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#667eea',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  destinationName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  aiCard: {
    backgroundColor: '#fff',
    margin: 20,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  aiCardContent: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
  },
  aiIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#9C27B0',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  aiText: {
    flex: 1,
  },
  aiTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  aiSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
});

export default HomeScreen;