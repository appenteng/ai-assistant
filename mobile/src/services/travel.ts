import api from './api';

export interface TripPlan {
  destination: string;
  days: number;
  itinerary: string[];
  estimated_cost: number;
  trip_type: string;
  recommendations: string[];
}

export interface Flight {
  id: string;
  airline: string;
  flight_number: string;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  price: number;
  stops: number;
}

export interface Hotel {
  id: string;
  name: string;
  location: string;
  price_per_night: number;
  rating: number;
  amenities: string[];
}

export const travelService = {
  // Trip Planning
  async planTrip(destination: string, days: number, budget?: number) {
    const response = await api.get('/travel/plan', {
      params: { destination, days, budget },
    });
    return response.data;
  },

  async getRecentTrips(limit: number = 5) {
    const response = await api.get('/travel/recent', {
      params: { limit },
    });
    return response.data;
  },

  // Flights
  async searchFlights(
    origin: string,
    destination: string,
    departureDate: string,
    returnDate?: string
  ) {
    const response = await api.get('/flights/search', {
      params: {
        origin,
        destination,
        departure_date: departureDate,
        return_date: returnDate,
        adults: 1,
        cabin_class: 'economy',
      },
    });
    return response.data;
  },

  // Hotels
  async searchHotels(
    location: string,
    checkIn: string,
    checkOut: string,
    guests: number = 2
  ) {
    const response = await api.get('/hotels/search', {
      params: {
        location,
        check_in: checkIn,
        check_out: checkOut,
        guests,
        rooms: 1,
      },
    });
    return response.data;
  },

  // AI Chat
  async chatWithAI(message: string) {
    const response = await api.get('/chat', {
      params: { message },
    });
    return response.data;
  },
};