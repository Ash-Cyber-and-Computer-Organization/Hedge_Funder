import HeroPage from './pages/HeroPage'
import AboutPage from './pages/AboutPage'
import PricingPage from './pages/PricingPage'
import ContactPage from './pages/ContactPage'
import Error404Page from './pages/Error404Page'
import SignUpPage from './pages/auth/SignUp'
import { Routes, Route } from "react-router-dom"
import { Toaster } from 'react-hot-toast'

const App = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<HeroPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/signin" element={<SignUpPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="*" element={<Error404Page />} />
      </Routes>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            theme: 'colored',
          },
          error: {
            duration: 4000,
            theme: 'colored',
          },
        }}
      />
    </>
   );
}

export default App;
