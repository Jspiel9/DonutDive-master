const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const serverUrl = 'http://74.126.76.47:3000';

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(cookieParser());
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true,
}));

// In-memory database (for demonstration purposes)
const users = [
  { id: 1, username: 'Jspiel', password: 'Password!' },
  { id: 2, username: 'user2', password: 'password2' },
];

// Middleware to check if the user is authenticated
const isAuthenticated = (req, res, next) => {
  if (req.session && req.session.userId) {
    return next();
  }
  res.status(401).json({ message: 'Unauthorized' });
};

// Login endpoint
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);

  if (user) {
    req.session.userId = user.id;
    res.json({ message: 'Login successful' });
  } else {
    res.status(401).json({ message: 'Invalid username or password' });
  }
});

// Logout endpoint
app.post('/logout', isAuthenticated, (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ message: 'Error logging out' });
    }
    res.json({ message: 'Logout successful' });
  });
});

// Check authentication status endpoint
app.get('/checkAuth', isAuthenticated, (req, res) => {
  res.json({ message: 'User is authenticated', username: req.session.username });
});

// Claim reward endpoint
app.post('/claimReward', isAuthenticated, (req, res) => {
  // In a real-world scenario, you might perform an action to grant the reward.
  // For demonstration purposes, mark the reward as claimed.
  if (!req.session.hasClaimedReward) {
    req.session.hasClaimedReward = true;
    res.json({ message: 'Reward claimed!' });
  } else {
    res.status(400).json({ message: 'You have already claimed the reward for this week' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
