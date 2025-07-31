// frontend/pages/_app.js
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return (
    <div className="flex flex-col min-h-screen bg-gray-900">
      <Navbar />
      <main className="flex-grow">
        <Component {...pageProps} />
      </main>
      <Footer />
    </div>
  );
}

export default MyApp;