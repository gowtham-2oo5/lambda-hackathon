"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Play, Pause, Download, Trash2 } from "@/lib/icons";
import { toast } from "sonner";

interface LogEntry {
  timestamp: string;
  level: "INFO" | "WARN" | "ERROR" | "DEBUG";
  service: string;
  message: string;
  requestId?: string;
  raw?: string;
}

interface RealTimeLogsProps {
  logGroups?: string[];
  autoRefresh?: boolean;
  maxLogs?: number;
}

export function RealTimeLogs({
  logGroups = [
    "/aws/lambda/README-Generator",
    "/aws/apigateway/README-API",
    "/aws/stepfunctions/README-Workflow",
  ],
  autoRefresh = true,
  maxLogs = 100,
}: RealTimeLogsProps) {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isStreaming, setIsStreaming] = useState(autoRefresh);
  const [selectedLogGroup, setSelectedLogGroup] = useState<string>("all");
  const [loading, setLoading] = useState(false);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchLogs = useCallback(async () => {
    if (loading) return;

    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (selectedLogGroup !== "all") {
        params.append("logGroup", selectedLogGroup);
      }

      const response = await fetch(`/api/monitoring/logs?${params}`);
      if (!response.ok) throw new Error("Failed to fetch logs");

      const newLogs = await response.json();

      setLogs((prevLogs) => {
        const combined = [...prevLogs, ...newLogs];
        // Keep only the most recent logs
        return combined.slice(-maxLogs);
      });

      // Auto-scroll to bottom if new logs arrived
      if (newLogs.length > 0) {
        setTimeout(scrollToBottom, 100);
      }
    } catch (error) {
      console.error("Error fetching logs:", error);
      toast.error("Failed to fetch logs");
    } finally {
      setLoading(false);
    }
  }, [loading, selectedLogGroup, maxLogs]);

  const startStreaming = useCallback(() => {
    setIsStreaming(true);
    intervalRef.current = setInterval(fetchLogs, 5000); // Fetch every 5 seconds
  }, [fetchLogs]);

  const stopStreaming = () => {
    setIsStreaming(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  const clearLogs = () => {
    setLogs([]);
    toast.success("Logs cleared");
  };

  const exportLogs = () => {
    const logText = logs
      .map(
        (log) =>
          `[${log.timestamp}] ${log.level} ${log.service}: ${log.message}${
            log.requestId ? ` (${log.requestId})` : ""
          }`
      )
      .join("\n");

    const blob = new Blob([logText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aws-logs-${new Date().toISOString().split("T")[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast.success("Logs exported");
  };

  useEffect(() => {
    // Initial fetch
    fetchLogs();

    if (isStreaming) {
      startStreaming();
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [selectedLogGroup, isStreaming, fetchLogs, startStreaming]);

  const getLogLevelColor = (level: LogEntry["level"]) => {
    switch (level) {
      case "ERROR":
        return "bg-red-100 text-red-800 border-red-200";
      case "WARN":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "INFO":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "DEBUG":
        return "bg-gray-100 text-gray-800 border-gray-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const filteredLogs =
    selectedLogGroup === "all"
      ? logs
      : logs.filter((log) =>
          log.service.toLowerCase().includes(selectedLogGroup.toLowerCase())
        );

  return (
    <Card className="h-full">
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle className="flex items-center gap-2">
              Real-Time Logs
              {isStreaming && (
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-green-600">Live</span>
                </div>
              )}
            </CardTitle>
          </div>

          <div className="flex items-center gap-2">
            <select
              value={selectedLogGroup}
              onChange={(e) => setSelectedLogGroup(e.target.value)}
              className="px-3 py-1 border rounded-md text-sm"
            >
              <option value="all">All Services</option>
              {logGroups.map((group) => (
                <option key={group} value={group}>
                  {group.split("/").pop()}
                </option>
              ))}
            </select>

            <Button
              size="sm"
              variant={isStreaming ? "destructive" : "default"}
              onClick={isStreaming ? stopStreaming : startStreaming}
            >
              {isStreaming ? (
                <Pause className="h-4 w-4" />
              ) : (
                <Play className="h-4 w-4" />
              )}
            </Button>

            <Button size="sm" variant="outline" onClick={exportLogs}>
              <Download className="h-4 w-4" />
            </Button>

            <Button size="sm" variant="outline" onClick={clearLogs}>
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className="bg-black text-green-400 font-mono text-sm p-4 rounded-lg h-96 overflow-y-auto">
          {filteredLogs.length === 0 ? (
            <div className="text-gray-500 text-center py-8">
              {loading ? "Loading logs..." : "No logs available"}
            </div>
          ) : (
            <div className="space-y-1">
              {filteredLogs.map((log, index) => (
                <div
                  key={index}
                  className="flex items-start gap-2 hover:bg-gray-900 p-1 rounded"
                >
                  <span className="text-gray-400 text-xs whitespace-nowrap">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <Badge className={`text-xs ${getLogLevelColor(log.level)}`}>
                    {log.level}
                  </Badge>
                  <span className="text-blue-400 text-xs">{log.service}:</span>
                  <span className="flex-1 break-words">{log.message}</span>
                  {log.requestId && (
                    <code className="text-xs text-white bg-gray-800 px-1 rounded">
                      {log.requestId}
                    </code>
                  )}
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          )}
        </div>

        <div className="mt-2 text-xs text-gray-500 flex justify-between">
          <span>
            Showing {filteredLogs.length} of {logs.length} logs
          </span>
          <span>
            {isStreaming ? "Auto-refreshing every 5s" : "Streaming paused"}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
