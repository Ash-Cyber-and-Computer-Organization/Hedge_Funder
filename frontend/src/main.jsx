import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { ClerkProvider } from "@clerk/clerk-react";
import { BrowserRouter } from "react-router-dom";

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

const AppWithClerk = () => {
  if (!PUBLISHABLE_KEY) {
    console.warn(
      "Clerk publishable key not found. Running without authentication."
    );
    return (
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
  }

  return (
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ClerkProvider>
  );
};

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <AppWithClerk />
  </StrictMode>
);
