import React, { useState, useEffect } from 'react';

const ServiceFlowDiagram = ({ currentStep = 0, isProcessing = false }) => {
  const [animatedStep, setAnimatedStep] = useState(0);

  const services = [
    {
      id: 1,
      name: "Frontend Input",
      icon: "🌐",
      description: "User enters GitHub URL",
      color: "bg-blue-100 border-blue-300",
      activeColor: "bg-blue-500 text-white"
    },
    {
      id: 2,
      name: "API Gateway",
      icon: "🚪",
      description: "REST API endpoint /generate",
      color: "bg-purple-100 border-purple-300",
      activeColor: "bg-purple-500 text-white"
    },
    {
      id: 3,
      name: "Step Functions",
      icon: "⚡",
      description: "Workflow orchestration",
      color: "bg-green-100 border-green-300",
      activeColor: "bg-green-500 text-white"
    },
    {
      id: 4,
      name: "Lambda Analysis",
      icon: "🔍",
      description: "Repository analysis phase",
      color: "bg-orange-100 border-orange-300",
      activeColor: "bg-orange-500 text-white"
    },
    {
      id: 5,
      name: "AI Services",
      icon: "🤖",
      description: "Bedrock + Comprehend + A2I",
      color: "bg-yellow-100 border-yellow-300",
      activeColor: "bg-yellow-500 text-white"
    },
    {
      id: 6,
      name: "S3 Storage",
      icon: "💾",
      description: "Analysis results storage",
      color: "bg-pink-100 border-pink-300",
      activeColor: "bg-pink-500 text-white"
    },
    {
      id: 7,
      name: "Lambda Generation",
      icon: "📄",
      description: "README generation phase",
      color: "bg-indigo-100 border-indigo-300",
      activeColor: "bg-indigo-500 text-white"
    },
    {
      id: 8,
      name: "Final Output",
      icon: "✅",
      description: "Generated README ready",
      color: "bg-emerald-100 border-emerald-300",
      activeColor: "bg-emerald-500 text-white"
    }
  ];

  useEffect(() => {
    if (isProcessing && currentStep > animatedStep) {
      const timer = setTimeout(() => {
        setAnimatedStep(currentStep);
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [currentStep, isProcessing, animatedStep]);

  const getStepStatus = (stepId) => {
    if (stepId < animatedStep) return 'completed';
    if (stepId === animatedStep && isProcessing) return 'active';
    return 'pending';
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6">
      {/* Title */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          🏗️ Serverless Architecture Flow
        </h2>
        <p className="text-gray-600">
          Multi-AI Service Integration with Step Functions Orchestration
        </p>
      </div>

      {/* Flow Diagram */}
      <div className="relative">
        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {services.map((service, index) => {
            const status = getStepStatus(service.id);
            const isActive = status === 'active';
            const isCompleted = status === 'completed';
            
            return (
              <div
                key={service.id}
                className={`relative p-4 rounded-lg border-2 transition-all duration-500 transform ${
                  isActive 
                    ? `${service.activeColor} scale-105 shadow-lg` 
                    : isCompleted
                    ? 'bg-gray-100 border-gray-300 opacity-75'
                    : service.color
                }`}
              >
                {/* Service Icon */}
                <div className="text-center mb-3">
                  <span className="text-3xl">{service.icon}</span>
                  {isActive && (
                    <div className="absolute -top-2 -right-2">
                      <div className="animate-ping absolute inline-flex h-4 w-4 rounded-full bg-blue-400 opacity-75"></div>
                      <div className="relative inline-flex rounded-full h-4 w-4 bg-blue-500"></div>
                    </div>
                  )}
                  {isCompleted && (
                    <div className="absolute -top-2 -right-2">
                      <div className="inline-flex rounded-full h-4 w-4 bg-green-500 text-white text-xs items-center justify-center">
                        ✓
                      </div>
                    </div>
                  )}
                </div>

                {/* Service Info */}
                <div className="text-center">
                  <h3 className={`font-semibold mb-1 ${isActive ? 'text-white' : 'text-gray-800'}`}>
                    {service.name}
                  </h3>
                  <p className={`text-sm ${isActive ? 'text-white opacity-90' : 'text-gray-600'}`}>
                    {service.description}
                  </p>
                </div>

                {/* Progress Indicator */}
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-1 bg-white bg-opacity-30 rounded-b-lg">
                    <div className="h-full bg-white rounded-b-lg animate-pulse"></div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Connection Lines */}
        <div className="hidden lg:block absolute inset-0 pointer-events-none">
          <svg className="w-full h-full" viewBox="0 0 800 400">
            {/* Horizontal connections */}
            <path
              d="M 200 100 L 400 100"
              stroke="#e5e7eb"
              strokeWidth="2"
              fill="none"
              className={animatedStep >= 2 ? "stroke-blue-500" : ""}
            />
            <path
              d="M 600 100 L 800 100"
              stroke="#e5e7eb"
              strokeWidth="2"
              fill="none"
              className={animatedStep >= 4 ? "stroke-blue-500" : ""}
            />
            <path
              d="M 200 300 L 400 300"
              stroke="#e5e7eb"
              strokeWidth="2"
              fill="none"
              className={animatedStep >= 6 ? "stroke-blue-500" : ""}
            />
            <path
              d="M 600 300 L 800 300"
              stroke="#e5e7eb"
              strokeWidth="2"
              fill="none"
              className={animatedStep >= 8 ? "stroke-blue-500" : ""}
            />
            
            {/* Vertical connections */}
            <path
              d="M 800 100 L 800 300"
              stroke="#e5e7eb"
              strokeWidth="2"
              fill="none"
              className={animatedStep >= 5 ? "stroke-blue-500" : ""}
            />
          </svg>
        </div>
      </div>

      {/* Technical Details */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="font-semibold text-blue-800 mb-2">🔄 Processing Flow</h4>
          <ul className="text-blue-700 space-y-1">
            <li>• Event-driven architecture</li>
            <li>• Automatic retry logic</li>
            <li>• State persistence</li>
          </ul>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg">
          <h4 className="font-semibold text-green-800 mb-2">🤖 AI Integration</h4>
          <ul className="text-green-700 space-y-1">
            <li>• Multi-model processing</li>
            <li>• Quality validation</li>
            <li>• ReAct reasoning</li>
          </ul>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-lg">
          <h4 className="font-semibold text-purple-800 mb-2">⚡ Performance</h4>
          <ul className="text-purple-700 space-y-1">
            <li>• 45-60 second processing</li>
            <li>• 99%+ accuracy rate</li>
            <li>• Auto-scaling compute</li>
          </ul>
        </div>
      </div>

      {/* Current Status */}
      {isProcessing && (
        <div className="mt-6 text-center">
          <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
            Processing step {animatedStep} of {services.length}
          </div>
        </div>
      )}
    </div>
  );
};

export default ServiceFlowDiagram;
