"use client";

import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Github, Upload, Brain, FileText, Download, ArrowRight } from 'lucide-react';

const steps = [
  {
    id: 1,
    icon: Github,
    title: "Connect Repository",
    description: "Paste your GitHub URL or upload project files directly",
    details: "Supports public/private repos, multiple file formats, and drag-and-drop uploads",
    color: "blue",
    time: "5 seconds"
  },
  {
    id: 2,
    icon: Upload,
    title: "Smart Analysis", 
    description: "AI scans your codebase, dependencies, and project structure",
    details: "Analyzes package.json, requirements.txt, file structure, and code patterns",
    color: "purple",
    time: "10 seconds"
  },
  {
    id: 3,
    icon: Brain,
    title: "AI Processing",
    description: "Claude Sonnet 4 generates comprehensive documentation",
    details: "Advanced reasoning creates contextual, accurate, and professional content",
    color: "indigo", 
    time: "15 seconds"
  },
  {
    id: 4,
    icon: FileText,
    title: "README Creation",
    description: "Professional README with badges, sections, and formatting",
    details: "Includes installation, usage, features, and contribution guidelines",
    color: "emerald",
    time: "3 seconds"
  },
  {
    id: 5,
    icon: Download,
    title: "Download & Use",
    description: "Copy, download, or integrate directly into your project",
    details: "Multiple export formats, direct GitHub integration, and version history",
    color: "amber",
    time: "Instant"
  }
];

const colorClasses = {
  blue: {
    bg: "bg-blue-50",
    border: "border-blue-200",
    gradient: "from-blue-500 to-blue-600",
    text: "text-blue-600",
    ring: "ring-blue-200"
  },
  purple: {
    bg: "bg-purple-50", 
    border: "border-purple-200",
    gradient: "from-purple-500 to-purple-600",
    text: "text-purple-600",
    ring: "ring-purple-200"
  },
  indigo: {
    bg: "bg-indigo-50",
    border: "border-indigo-200", 
    gradient: "from-indigo-500 to-indigo-600",
    text: "text-indigo-600",
    ring: "ring-indigo-200"
  },
  emerald: {
    bg: "bg-emerald-50",
    border: "border-emerald-200",
    gradient: "from-emerald-500 to-emerald-600", 
    text: "text-emerald-600",
    ring: "ring-emerald-200"
  },
  amber: {
    bg: "bg-amber-50",
    border: "border-amber-200",
    gradient: "from-amber-500 to-amber-600",
    text: "text-amber-600", 
    ring: "ring-amber-200"
  }
};

export default function HowItWorksTimeline() {
  const [activeStep, setActiveStep] = useState(1);

  return (
    <section className="py-24 px-6 bg-gradient-to-br from-neutral-50 via-white to-neutral-100/50">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 text-neutral-900 tracking-tight">
            How It Works
          </h2>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto mb-4">
            From code to professional documentation in under 30 seconds
          </p>
          <div className="flex items-center justify-center space-x-2 text-sm text-neutral-500">
            <span>Total time:</span>
            <span className="font-semibold text-neutral-700">~30 seconds</span>
          </div>
        </div>

        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-blue-200 via-purple-200 via-indigo-200 via-emerald-200 to-amber-200 rounded-full hidden md:block" />

          <div className="space-y-12">
            {steps.map((step, index) => {
              const colors = colorClasses[step.color];
              const isActive = activeStep === step.id;
              const isLeft = index % 2 === 0;

              return (
                <div 
                  key={step.id}
                  className={`relative flex items-center ${isLeft ? 'md:flex-row' : 'md:flex-row-reverse'} flex-col`}
                  onMouseEnter={() => setActiveStep(step.id)}
                >
                  {/* Timeline Node */}
                  <div className={`absolute left-1/2 transform -translate-x-1/2 w-4 h-4 rounded-full bg-gradient-to-r ${colors.gradient} ring-4 ${colors.ring} z-10 hidden md:block transition-all duration-300 ${isActive ? 'scale-125' : ''}`} />

                  {/* Content Card */}
                  <div className={`w-full md:w-5/12 ${isLeft ? 'md:pr-12' : 'md:pl-12'}`}>
                    <Card className={`${colors.border} ${colors.bg} hover:shadow-xl transition-all duration-300 ${isActive ? 'scale-105 shadow-2xl' : ''} cursor-pointer`}>
                      <CardContent className="p-6">
                        <div className="flex items-start space-x-4">
                          <div className={`w-12 h-12 rounded-full bg-gradient-to-r ${colors.gradient} flex items-center justify-center flex-shrink-0`}>
                            <step.icon className="w-6 h-6 text-white" />
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h3 className="text-xl font-semibold text-neutral-900">
                                {step.title}
                              </h3>
                              <span className={`text-xs font-medium px-2 py-1 rounded-full ${colors.bg} ${colors.text}`}>
                                {step.time}
                              </span>
                            </div>
                            <p className="text-neutral-600 mb-3">
                              {step.description}
                            </p>
                            {isActive && (
                              <div className="text-sm text-neutral-500 border-t pt-3 animate-in slide-in-from-top-2 duration-300">
                                {step.details}
                              </div>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Step Number */}
                  <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${colors.gradient} flex items-center justify-center text-white font-bold text-sm mb-4 md:mb-0 md:absolute md:left-1/2 md:transform md:-translate-x-1/2 z-20`}>
                    {step.id}
                  </div>

                  {/* Arrow for mobile */}
                  {index < steps.length - 1 && (
                    <ArrowRight className="w-6 h-6 text-neutral-300 mb-4 md:hidden" />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
