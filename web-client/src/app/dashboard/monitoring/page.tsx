"use client";

import { ResourceMonitor } from '@/components/monitoring/ResourceMonitor';

export default function MonitoringPage() {
  return (
    <div className="container mx-auto p-6">
      <ResourceMonitor />
    </div>
  );
}
