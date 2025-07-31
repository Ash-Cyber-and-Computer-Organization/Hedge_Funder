import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

const tradeHistory = [
  { id: 1, asset: "EUR/USD", type: "Buy", profit: "+$220", time: "2 hours ago" },
  { id: 2, asset: "BTC/USD", type: "Sell", profit: "-$85", time: "5 hours ago" },
  { id: 3, asset: "AAPL", type: "Buy", profit: "+$170", time: "1 day ago" },
];

const History = () => {
  return (
    <Card className="rounded-2xl shadow-md p-4">
      <CardContent>
        <h2 className="text-xl font-semibold mb-4">Trade History</h2>
        <ScrollArea className="h-64 pr-2">
          <ul className="space-y-3">
            {tradeHistory.map((trade) => (
              <li
                key={trade.id}
                className="flex justify-between items-center p-3 rounded-xl bg-muted hover:bg-accent transition"
              >
                <div>
                  <p className="font-medium">{trade.asset}</p>
                  <p className="text-sm text-muted-foreground">
                    {trade.type} • {trade.time}
                  </p>
                </div>
                <span
                  className={`font-bold ${
                    trade.profit.startsWith("+") ? "text-green-600" : "text-red-600"
                  }`}
                >
                  {trade.profit}
                </span>
              </li>
            ))}
          </ul>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default History;
