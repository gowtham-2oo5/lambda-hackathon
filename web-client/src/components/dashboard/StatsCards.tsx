"use client";

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  FileText, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  TrendingUp,
  Zap
} from "lucide-react";
import { ReadmeHistoryItem } from "@/types/dashboard";

interface StatsCardsProps {
  history: ReadmeHistoryItem[];
}

const StatsCards: React.FC<StatsCardsProps> = ({ history }) => {
  const totalGenerated = history.length;
  const completedCount = history.filter(item => item.status === 'completed').length;
  const processingCount = history.filter(item => item.status === 'processing').length;
  const failedCount = history.filter(item => item.status === 'failed').length;
  
  const completedItems = history.filter(item => item.status === 'completed' && item.processingTime);
  const avgProcessingTime = completedItems.length > 0 
    ? completedItems.reduce((sum, item) => sum + (item.processingTime || 0), 0) / completedItems.length
    : 0;
  
  const successRate = totalGenerated > 0 ? (completedCount / totalGenerated) * 100 : 0;
  
  const formatTime = (seconds: number) => {
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    return `${Math.floor(seconds / 60)}m ${(seconds % 60).toFixed(0)}s`;
  };

  const stats = [
    {
      title: "Total Generated",
      value: totalGenerated.toString(),
      icon: FileText,
      color: "bg-blue-500",
      bgColor: "bg-blue-50",
      textColor: "text-blue-700"
    },
    {
      title: "Completed",
      value: completedCount.toString(),
      icon: CheckCircle,
      color: "bg-green-500",
      bgColor: "bg-green-50",
      textColor: "text-green-700"
    },
    {
      title: "Processing",
      value: processingCount.toString(),
      icon: Clock,
      color: "bg-yellow-500",
      bgColor: "bg-yellow-50",
      textColor: "text-yellow-700"
    },
    {
      title: "Success Rate",
      value: `${successRate.toFixed(1)}%`,
      icon: TrendingUp,
      color: "bg-purple-500",
      bgColor: "bg-purple-50",
      textColor: "text-purple-700"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => {
        const IconComponent = stat.icon;
        return (
          <Card key={index} className={`${stat.bgColor} border-l-4 border-l-current ${stat.textColor}`}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium opacity-70">
                    {stat.title}
                  </p>
                  <p className="text-3xl font-bold">
                    {stat.value}
                  </p>
                </div>
                <div className={`p-3 rounded-full ${stat.color}`}>
                  <IconComponent className="w-6 h-6 text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
      
      {/* Additional Performance Stats */}
      {avgProcessingTime > 0 && (
        <Card className="bg-gradient-to-br from-indigo-50 to-purple-50 border-l-4 border-l-indigo-500 md:col-span-2 lg:col-span-2">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-indigo-700 opacity-70">
                  Average Processing Time
                </p>
                <p className="text-3xl font-bold text-indigo-700">
                  {formatTime(avgProcessingTime)}
                </p>
                <div className="flex items-center space-x-2 mt-2">
                  <Badge className="bg-indigo-100 text-indigo-800 border-indigo-200">
                    <Zap className="w-3 h-3 mr-1" />
                    74% Faster than Original
                  </Badge>
                </div>
              </div>
              <div className="p-3 rounded-full bg-indigo-500">
                <Clock className="w-6 h-6 text-white" />
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      
      {failedCount > 0 && (
        <Card className="bg-red-50 border-l-4 border-l-red-500">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-red-700 opacity-70">
                  Failed
                </p>
                <p className="text-3xl font-bold text-red-700">
                  {failedCount}
                </p>
              </div>
              <div className="p-3 rounded-full bg-red-500">
                <AlertCircle className="w-6 h-6 text-white" />
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default StatsCards;
