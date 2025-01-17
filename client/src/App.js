import React from 'react';
import { CssBaseline, Container, Typography, Box, AppBar, Toolbar, Button } from '@mui/material';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

// Example Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import UserDashboard from './pages/user/UserDashboard';

// Main App layout component
const App = () => {
  return (
    <Router>
      <div style={{ display: 'flex' }}>
        {/* Sidebar */}
        <Box
          sx={{
            width: 250,
            height: '100vh',
            backgroundColor: 'primary.main',
            color: 'white',
            padding: 2,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Typography variant="h5" gutterBottom>
            Admin Panel
          </Typography>
          <Button component={Link} to="/admin-dashboard" color="inherit">Admin Dashboard</Button>
          <Button component={Link} to="/user-dashboard" color="inherit">User Dashboard</Button>
        </Box>

        {/* Main content area */}
        <Box
          sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                My Application
              </Typography>
            </Toolbar>
          </AppBar>

          <Container sx={{ marginTop: 2 }}>
            <Routes>
              <Route path="/admin-dashboard" element={<AdminDashboard />} />
              <Route path="/user-dashboard" element={<UserDashboard />} />
            </Routes>
          </Container>
        </Box>
      </div>
    </Router>
  );
};

export default App;
