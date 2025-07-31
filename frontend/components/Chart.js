import React from "react";
import { Card, CardContent } from "@/components/ui/card";

const Chart = () => {
  return (
    <Card className="rounded-2xl shadow-lg p-4">
      <CardContent>
        <h2 className="text-xl font-semibold mb-4">Performance Chart</h2>
        <div className="w-full h-64 bg-muted rounded-lg flex items-center justify-center">
          <span className="text-muted-foreground">[Chart goes here]</span>
        </div>
      </CardContent>
    </Card>
  );
};

export default Chart;
