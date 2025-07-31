import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { DollarSign } from "lucide-react";

const Balance = () => {
  return (
    <Card className="rounded-2xl shadow-lg p-4 flex items-center gap-4">
      <DollarSign className="w-10 h-10 text-green-600" />
      <CardContent className="p-0">
        <p className="text-sm text-muted-foreground">Available Balance</p>
        <h1 className="text-3xl font-bold text-foreground">$12,420.75</h1>
      </CardContent>
    </Card>
  );
};

export default Balance;
