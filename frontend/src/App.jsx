import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HeroPage from './pages/HeroPage';
import TradingDashboard from './pages/TradingDashboard';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HeroPage />} />
        <Route path="/dashboard" element={<TradingDashboard />} />
      </Routes>
    </Router>
  );
};

export default App;
