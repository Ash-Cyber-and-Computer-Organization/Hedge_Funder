import React from "react";

const Footer = () => {
  return (
    <footer className="w-full py-4 mt-8 text-center text-sm text-muted-foreground border-t border-border">
      <p>
        &copy; {new Date().getFullYear()} Hedge Funder • Built for performance
      </p>
    </footer>
  );
};

export default Footer;
