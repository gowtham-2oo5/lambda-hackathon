"use client";

import { useState, useEffect, useCallback, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Activity, 
  AlertCircle, 
  CheckCircle, 
  Clock, 
  Database, 
  Zap, 
  Settings,
  Layers,
  Shield,
  RefreshCw
} from '@/lib/icons';
import { toast } from 'sonner';
import { RealTimeLogs } from './RealTimeLogs';

interface ResourceStatus {
  name: string;
  type: 'lambda' | 'stepfunctions' | 'apigateway' | 'dynamodb' | 's3' | 'cognito';
  status: 'healthy' | 'warning' | 'error';
  lastChecked: string;
  metrics?: {
    invocations?: number;
    errors?: number;
    duration?: number;
  };
}

export function ResourceMonitor() {
  const [resources, setResources] = useState<ResourceStatus[]>([]);
  const [loading, setLoading] = useState(false);

  // Mock data - replace with actual AWS API calls
  const mockResources: ResourceStatus[] = useMemo(() => [
    {
      name: 'README-Generator-Lambda',
      type: 'lambda',
      status: 'healthy',
      lastChecked: new Date().toISOString(),
      metrics: { invocations: 45, errors: 0, duration: 2500 }
    },
    {
      name: 'README-Workflow-StepFunction',
      type: 'stepfunctions',
      status: 'healthy',
      lastChecked: new Date().toISOString(),
      metrics: { invocations: 12, errors: 0 }
    },
    {
      name: 'README-API-Gateway',
      type: 'apigateway',
      status: 'warning',
      lastChecked: new Date().toISOString(),
      metrics: { invocations: 156, errors: 3 }
    },
    {
      name: 'README-History-DynamoDB',
      type: 'dynamodb',
      status: 'healthy',
      lastChecked: new Date().toISOString(),
    },
    {
      name: 'README-Storage-S3',
      type: 's3',
      status: 'healthy',
      lastChecked: new Date().toISOString(),
    },
    {
      name: 'User-Pool-Cognito',
      type: 'cognito',
      status: 'healthy',
      lastChecked: new Date().toISOString(),
    }
  ], []);

  const fetchResourceStatus = useCallback(async () => {
    setLoading(true);
    try {
      // TODO: Replace with actual AWS CloudWatch API calls
      // const response = await fetch('/api/monitoring/resources');
      // const data = await response.json();
      
      // Mock delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      setResources(mockResources);
      
      toast.success('Resource status updated');
    } catch (error) {
      toast.error('Failed to fetch resource status');
      console.error('Error fetching resources:', error);
    } finally {
      setLoading(false);
    }
  }, [mockResources]);

  useEffect(() => {
    fetchResourceStatus();
    // Set up polling every 30 seconds
    const interval = setInterval(fetchResourceStatus, 30000);
    return () => clearInterval(interval);
  }, [fetchResourceStatus]);

  const getResourceIcon = (type: ResourceStatus['type']) => {
    const iconMap = {
      lambda: Zap,
      stepfunctions: Layers,
      apigateway: Settings,
      dynamodb: Database,
      s3: Database,
      cognito: Shield
    };
    return iconMap[type] || Activity;
  };

  const getStatusColor = (status: ResourceStatus['status']) => {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: ResourceStatus['status']) => {
    switch (status) {
      case 'healthy': return CheckCircle;
      case 'warning': return AlertCircle;
      case 'error': return AlertCircle;
      default: return Clock;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Resource Monitor</h2>
          <p className="text-muted-foreground">Monitor all AWS resources for your README generator</p>
        </div>
        <Button onClick={fetchResourceStatus} disabled={loading}>
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Resource Status Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {resources.map((resource) => {
          const Icon = getResourceIcon(resource.type);
          const StatusIcon = getStatusIcon(resource.status);
          
          return (
            <Card key={resource.name}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium flex items-center">
                  <Icon className="h-4 w-4 mr-2" />
                  {resource.name}
                </CardTitle>
                <Badge className={getStatusColor(resource.status)}>
                  <StatusIcon className="h-3 w-3 mr-1" />
                  {resource.status}
                </Badge>
              </CardHeader>
              <CardContent>
                <div className="text-xs text-muted-foreground mb-2">
                  Last checked: {new Date(resource.lastChecked).toLocaleTimeString()}
                </div>
                {resource.metrics && (
                  <div className="space-y-1">
                    {resource.metrics.invocations && (
                      <div className="flex justify-between text-sm">
                        <span>Invocations:</span>
                        <span className="font-medium">{resource.metrics.invocations}</span>
                      </div>
                    )}
                    {resource.metrics.errors !== undefined && (
                      <div className="flex justify-between text-sm">
                        <span>Errors:</span>
                        <span className={`font-medium ${resource.metrics.errors > 0 ? 'text-red-600' : 'text-green-600'}`}>
                          {resource.metrics.errors}
                        </span>
                      </div>
                    )}
                    {resource.metrics.duration && (
                      <div className="flex justify-between text-sm">
                        <span>Avg Duration:</span>
                        <span className="font-medium">{resource.metrics.duration}ms</span>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Real-Time Logs */}
      <RealTimeLogs />
    </div>
  );
}
