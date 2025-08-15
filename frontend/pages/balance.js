import React from "react";
import ModernLayout from "../components/ModernLayout";

const Balance = () => {
  return (
    <ModernLayout>
      <div className="bg-dark-800/50 backdrop-blur-sm rounded-xl p-6 border border-dark-700 flex items-center gap-4">
        <div className="w-10 h-10 flex items-center justify-center rounded-full bg-primary-500 text-white text-2xl font-bold">
          $
        </div>
        <div>
          <p className="text-sm text-gray-400">Available Balance</p>
          <h1 className="text-3xl font-bold text-white">$12,420.75</h1>
        </div>
      </div>
    </ModernLayout>
  );
};

export default Balance;
