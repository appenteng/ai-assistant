// Frontend JavaScript for AI Travel Assistant
const API_URL = 'http://localhost:8000'; // Change to your deployed URL

// DOM Elements
let currentDestination = 'Tokyo';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadRecentTrips();
    loadPopularDestinations();

    // Auto-focus on destination input
    document.getElementById('destination').focus();

    // Load saved trips from localStorage
    const savedTrips = localStorage.getItem('aiTravelTrips');
    if (savedTrips) {
        displaySavedTrips(JSON.parse(savedTrips));
    }
});

// Plan a new trip
async function planTrip() {
    const destination = document.getElementById('destination').value.trim();
    const days = parseInt(document.getElementById('days').value);
    const budget = document.getElementById('budget').value || null;

    if (!destination) {
        alert('Please enter a destination');
        return;
    }

    if (days < 1 || days > 30) {
        alert('Please enter days between 1 and 30');
        return;
    }

    // Show loading state
    const planButton = document.querySelector('.plan-button');
    const originalText = planButton.innerHTML;
    planButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Planning...';
    planButton.disabled = true;

    try {
        // Build URL with parameters
        let url = `${API_URL}/api/travel/plan?destination=${encodeURIComponent(destination)}&days=${days}`;
        if (budget) {
            url += `&budget=${budget}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (data.status === 'success') {
            displayTripResult(data.plan, data.trip_id);

            // Save to localStorage
            saveTripToLocalStorage(data.plan, data.trip_id);

            // Reload recent trips
            loadRecentTrips();
        } else {
            throw new Error(data.detail || 'Failed to plan trip');
        }

    } catch (error) {
        showError('Failed to plan trip: ' + error.message);
    } finally {
        // Restore button
        planButton.innerHTML = originalText;
        planButton.disabled = false;
    }
}

// Display trip results
function displayTripResult(plan, tripId) {
    const resultDiv = document.getElementById('tripResult');

    // Format currency
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    };

    // Create HTML for trip result
    let html = `
        <div class="trip-success">
            <h3><i class="fas fa-check-circle"></i> Trip to ${plan.destination} Planned!</h3>
            <div class="trip-summary">
                <div class="summary-item">
                    <span class="label">Duration:</span>
                    <span class="value">${plan.days} days</span>
                </div>
                <div class="summary-item">
                    <span class="label">Type:</span>
                    <span class="value">${plan.trip_type} trip</span>
                </div>
                <div class="summary-item">
                    <span class="label">Cost Level:</span>
                    <span class="value">${plan.cost_level}</span>
                </div>
            </div>

            <h4><i class="fas fa-dollar-sign"></i> Cost Breakdown</h4>
            <div class="cost-grid">
                <div class="cost-item">
                    <div class="label">Accommodation</div>
                    <div class="amount">${formatCurrency(plan.cost_breakdown.accommodation)}</div>
                </div>
                <div class="cost-item">
                    <div class="label">Food & Dining</div>
                    <div class="amount">${formatCurrency(plan.cost_breakdown.food)}</div>
                </div>
                <div class="cost-item">
                    <div class="label">Activities</div>
                    <div class="amount">${formatCurrency(plan.cost_breakdown.activities)}</div>
                </div>
                <div class="cost-item">
                    <div class="label">Transportation</div>
                    <div class="amount">${formatCurrency(plan.cost_breakdown.transportation)}</div>
                </div>
                <div class="cost-item total">
                    <div class="label">Total Estimated</div>
                    <div class="amount">${formatCurrency(plan.estimated_cost)}</div>
                </div>
            </div>

            <h4><i class="fas fa-route"></i> Itinerary</h4>
            <ul class="itinerary-list">
                ${plan.itinerary.map(day => `<li>${day}</li>`).join('')}
            </ul>

            <h4><i class="fas fa-lightbulb"></i> Recommendations</h4>
            <div class="recommendations">
                ${plan.recommendations.map(rec => `
                    <div class="recommendation">
                        <i class="fas fa-star"></i> ${rec}
                    </div>
                `).join('')}
            </div>

            <h4><i class="fas fa-suitcase"></i> Packing Tips</h4>
            <div class="packing-tips">
                ${plan.packing_tips.map(tip => `
                    <span class="packing-tag">${tip}</span>
                `).join('')}
            </div>

            <div class="trip-actions">
                <button class="save-button" onclick="saveTrip('${tripId}')">
                    <i class="fas fa-bookmark"></i> Save Trip
                </button>
                <button class="share-button" onclick="shareTrip()">
                    <i class="fas fa-share"></i> Share
                </button>
            </div>
        </div>
    `;

    resultDiv.innerHTML = html;
    resultDiv.style.display = 'block';

    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

// Load recent trips from API
async function loadRecentTrips() {
    const tripsDiv = document.getElementById('recentTrips');

    try {
        const response = await fetch(`${API_URL}/api/travel/recent?limit=6`);
        const data = await response.json();

        if (data.trips && data.trips.length > 0) {
            displayTrips(data.trips);
        } else {
            tripsDiv.innerHTML = `
                <div class="no-trips">
                    <i class="fas fa-map-marked-alt"></i>
                    <p>No trips planned yet. Start planning your first adventure!</p>
                </div>
            `;
        }
    } catch (error) {
        tripsDiv.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Could not load trips. Make sure the backend is running.</p>
            </div>
        `;
    }
}

// Display trips in the grid
function displayTrips(trips) {
    const tripsDiv = document.getElementById('recentTrips');

    let html = '';
    trips.forEach(trip => {
        const date = trip.created_at ? new Date(trip.created_at).toLocaleDateString() : 'Recently';

        html += `
            <div class="trip-card" onclick="viewTripDetails(${trip.id})">
                <div class="trip-header">
                    <div class="trip-destination">${trip.destination}</div>
                    <div class="trip-days">${trip.days} days</div>
                </div>
                <div class="trip-meta">
                    <span><i class="fas fa-dollar-sign"></i> ${trip.budget}</span>
                    <span><i class="fas fa-tag"></i> ${trip.preferences?.type || 'Standard'}</span>
                </div>
                <div class="trip-date">
                    <i class="far fa-calendar"></i> ${date}
                </div>
                <div class="trip-status">
                    <span class="status-badge ${trip.status}">${trip.status}</span>
                </div>
            </div>
        `;
    });

    tripsDiv.innerHTML = html;
}

// Load popular destinations
async function loadPopularDestinations() {
    try {
        const response = await fetch(`${API_URL}/api/travel/destinations`);
        const data = await response.json();

        const destinationsDiv = document.getElementById('destinationsGrid');
        let html = '';

        for (const [type, cities] of Object.entries(data)) {
            cities.forEach(city => {
                html += `
                    <div class="destination-card" onclick="setDestination('${city}')">
                        <div class="destination-icon">
                            ${getDestinationIcon(type)}
                        </div>
                        <div class="destination-name">${city}</div>
                        <div class="destination-type">${type}</div>
                    </div>
                `;
            });
        }

        destinationsDiv.innerHTML = html;
    } catch (error) {
        console.error('Failed to load destinations:', error);
    }
}

// Get icon for destination type
function getDestinationIcon(type) {
    const icons = {
        'beach': '<i class="fas fa-umbrella-beach"></i>',
        'city': '<i class="fas fa-city"></i>',
        'mountain': '<i class="fas fa-mountain"></i>',
        'adventure': '<i class="fas fa-hiking"></i>'
    };
    return icons[type] || '<i class="fas fa-map-marker-alt"></i>';
}

// Set destination from popular destinations
function setDestination(city) {
    document.getElementById('destination').value = city;
    scrollToPlanner();
}

// Chat with AI
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    addChatMessage(message, 'user');
    input.value = '';

    try {
        const response = await fetch(`${API_URL}/api/chat?message=${encodeURIComponent(message)}`);
        const data = await response.json();

        // Add AI response to chat
        addChatMessage(data.response, 'ai');

        // Check if message is about travel planning
        if (message.toLowerCase().includes('plan') || message.toLowerCase().includes('trip')) {
            // Suggest planning a trip
            setTimeout(() => {
                addChatMessage("Would you like me to help you plan a trip? Click 'Start Planning' above!", 'ai');
            }, 1000);
        }

    } catch (error) {
        addChatMessage("I'm having trouble connecting right now. Please try again later.", 'ai');
    }
}

// Add message to chat UI
function addChatMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = sender === 'ai'
        ? '<i class="fas fa-robot"></i>'
        : '<i class="fas fa-user"></i>';

    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${avatar}
        </div>
        <div class="message-content">
            ${message}
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Save trip to localStorage
function saveTripToLocalStorage(plan, tripId) {
    let savedTrips = JSON.parse(localStorage.getItem('aiTravelTrips') || '[]');

    const tripData = {
        id: tripId || Date.now(),
        ...plan,
        saved_at: new Date().toISOString()
    };

    savedTrips.unshift(tripData); // Add to beginning
    savedTrips = savedTrips.slice(0, 10); // Keep only 10 most recent

    localStorage.setItem('aiTravelTrips', JSON.stringify(savedTrips));
}

// Display saved trips from localStorage
function displaySavedTrips(trips) {
    // Optional: You can create a separate section for saved trips
    console.log('Saved trips:', trips);
}

// Save trip (mock function)
function saveTrip(tripId) {
    alert(`Trip ${tripId} saved to your profile!`);
}

// Share trip (mock function)
function shareTrip() {
    alert('Share feature coming soon!');
}

// View trip details
async function viewTripDetails(tripId) {
    try {
        const response = await fetch(`${API_URL}/api/travel/trip/${tripId}`);
        const trip = await response.json();

        // For now, just alert with trip details
        alert(`Trip to ${trip.destination}\nDays: ${trip.days}\nBudget: $${trip.budget}`);
    } catch (error) {
        alert('Could not load trip details');
    }
}

// Scroll to planner section
function scrollToPlanner() {
    document.getElementById('planner').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(errorDiv);

    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Initialize example chat
setTimeout(() => {
    addChatMessage("Try asking me: 'What should I pack for a beach trip?' or 'Plan a budget trip to Europe'", 'ai');
}, 2000);