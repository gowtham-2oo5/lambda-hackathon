import dynamic from 'next/dynamic';
import { Loader2 } from '@/lib/icons';

// Loading component
const LoadingSpinner = () => (
  <div className="flex items-center justify-center p-4">
    <Loader2 className="h-6 w-6 animate-spin mr-2" />
    <span>Loading...</span>
  </div>
);

// Dynamically imported components - these will be code-split automatically
export const DynamicHistoryDashboard = dynamic(
  () => import('@/components/HistoryDashboard'),
  {
    loading: LoadingSpinner,
    ssr: false, // Disable SSR for this component to reduce initial bundle
  }
);

export const DynamicDebugInfo = dynamic(
  () => import('@/components/DebugInfo').then(mod => ({ default: mod.DebugInfo })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
);

export const DynamicMultiStepLoader = dynamic(
  () => import('@/components/ui/multi-step-loader').then(mod => ({ default: mod.MultiStepLoader })),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
);

// Heavy diagram components - only load when needed
export const DynamicServiceFlowDiagram = dynamic(
  () => import('@/components/ServiceFlowDiagram'),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
);

export const DynamicArchitectureDiagram = dynamic(
  () => import('@/components/ArchitectureDiagram'),
  {
    loading: LoadingSpinner,
    ssr: false,
  }
);
