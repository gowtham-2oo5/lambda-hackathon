"use client";

import type React from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ArrowRight,
  Github,
  Zap,
  FileText,
  Download,
  Users,
  Clock,
  Code,
  Brain,
  Sparkles,
} from "@/lib/icons";
import Link from "next/link";
import { useRef, forwardRef, useEffect, useState } from "react";
import { AnimatedBeam } from "@/components/magicui/animated-beam";
import { AnimatedGradientText } from "@/components/magicui/animated-gradient-text";
import { cn } from "@/lib/utils";
// import PreviewNavigation from "@/components/PreviewNavigation";
// import PreviewTest from "@/components/PreviewTest";

const Circle = forwardRef<
  HTMLDivElement,
  { className?: string; children?: React.ReactNode }
>(({ className, children }, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        "z-10 flex size-16 items-center justify-center rounded-full border border-neutral-200/50 bg-white/80 backdrop-blur-sm p-4 shadow-[0_8px_32px_-12px_rgba(0,0,0,0.25)] transition-all duration-300 hover:shadow-[0_20px_40px_-12px_rgba(0,0,0,0.35)]",
        className
      )}
    >
      {children}
    </div>
  );
});
Circle.displayName = "Circle";

export default function LandingPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const div1Ref = useRef<HTMLDivElement>(null);
  const div2Ref = useRef<HTMLDivElement>(null);
  const div3Ref = useRef<HTMLDivElement>(null);
  const div4Ref = useRef<HTMLDivElement>(null);
  const div5Ref = useRef<HTMLDivElement>(null);

  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50/50">
      {/* Header */}
      <header className="border-b border-neutral-200/50 bg-white/70 backdrop-blur-xl sticky top-0 z-50 transition-all duration-300">
        <div className="container mx-auto px-6 py-5 flex items-center justify-between max-w-7xl">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 bg-gradient-to-br from-neutral-900 to-neutral-700 rounded-xl flex items-center justify-center shadow-lg">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-semibold text-neutral-900 tracking-tight">
              SmartReadmeGen
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/auth/login">
              <Button
                variant="ghost"
                className="text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100/50 transition-all duration-200"
              >
                Sign In
              </Button>
            </Link>
            <Link href="/auth/signup">
              <Button className="bg-neutral-900 hover:bg-neutral-800 text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-24 pb-32 px-6 relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-r from-neutral-50/50 via-transparent to-neutral-50/50" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-blue-100/30 to-purple-100/30 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-br from-amber-100/30 to-rose-100/30 rounded-full blur-3xl" />

        <div className="container mx-auto text-center max-w-5xl relative z-10">
          <div
            className={`mb-8 transition-all duration-1000 ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-8"
            }`}
          >
            <div className="inline-flex items-center justify-center rounded-full px-4 py-2 bg-white/60 backdrop-blur-sm border border-neutral-200/50 shadow-lg hover:shadow-xl transition-all duration-300 group">
              <Sparkles className="w-4 h-4 mr-2 text-amber-500" />
              <div className="h-4 w-px bg-neutral-300 mx-2" />
              <AnimatedGradientText
                className="text-sm font-medium inline-block"
                colorFrom="#6366f1"
                colorTo="#8b5cf6"
              >
                Enterprise Edition v3.0 • 95% AI Accuracy
              </AnimatedGradientText>
              <ArrowRight className="ml-2 size-4 text-neutral-500 transition-transform duration-300 group-hover:translate-x-1" />
            </div>
          </div>

          <h1
            className={`text-6xl md:text-7xl lg:text-8xl font-bold mb-8 text-neutral-900 leading-[0.9] tracking-tight transition-all duration-1000 delay-200 ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-8"
            }`}
          >
            Enterprise-Grade
            <br />
            <span className="bg-gradient-to-r from-neutral-900 via-neutral-700 to-neutral-900 bg-clip-text text-transparent">
              README
            </span>
            <br />
            Generation Platform
          </h1>

          <p
            className={`text-xl md:text-2xl text-neutral-600 mb-8 leading-relaxed max-w-4xl mx-auto font-light transition-all duration-1000 delay-400 ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-8"
            }`}
          >
            The world's most sophisticated README generator powered by{" "}
            <strong>Claude Sonnet 4 AI</strong>,
            <strong> multi-model consensus validation</strong>, and
            enterprise-grade AWS serverless architecture. Delivering{" "}
            <strong>95% accuracy</strong> with{" "}
            <strong>16-second processing</strong> times.
          </p>

          {/* Performance Stats */}
          <div
            className={`grid grid-cols-2 md:grid-cols-4 gap-6 mb-12 max-w-4xl mx-auto transition-all duration-1000 delay-500 ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-8"
            }`}
          >
            <div className="text-center">
              <div className="text-3xl font-bold text-neutral-900 mb-1">
                &lt;30s
              </div>
              <div className="text-sm text-neutral-600">Processing Time</div>
              <div className="text-xs text-neutral-500">Sub-30 second analysis</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-neutral-900 mb-1">
                95%
              </div>
              <div className="text-sm text-neutral-600">AI Accuracy</div>
              <div className="text-xs text-neutral-500">
                Multi-model consensus
              </div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-neutral-900 mb-1">
                $0.07
              </div>
              <div className="text-sm text-neutral-600">Cost per README</div>
              <div className="text-xs text-neutral-500">70% cheaper than alternatives</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-neutral-900 mb-1">
                20+
              </div>
              <div className="text-sm text-neutral-600">READMEs Generated</div>
              <div className="text-xs text-neutral-500">Real production usage</div>
            </div>
          </div>

          <div
            className={`flex flex-col sm:flex-row gap-6 justify-center mb-16 transition-all duration-1000 delay-600 ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-8"
            }`}
          >
            <Link href="/dashboard">
              <Button
                size="lg"
                className="bg-neutral-900 hover:bg-neutral-800 text-white text-lg px-10 py-4 h-auto shadow-xl hover:shadow-2xl transition-all duration-300 group"
              >
                Launch Platform
                <ArrowRight className="ml-3 w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" />
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              className="text-lg px-10 py-4 h-auto border-neutral-300 text-neutral-700 hover:bg-neutral-50 bg-white/50 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300 group"
            >
              <Github className="mr-3 w-5 h-5" />
              View Architecture
            </Button>
          </div>
        </div>
      </section>

      {/* How it Works with Animated Flow */}
      <section className="py-32 px-6 bg-white relative">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-bold mb-6 text-neutral-900 tracking-tight">
              How It Works
            </h2>
            <p className="text-xl md:text-2xl text-neutral-600 font-light max-w-2xl mx-auto">
              Simple process, powerful results
            </p>
          </div>

          {/* Animated Flow */}
          <div
            className="relative flex h-[500px] w-full items-center justify-center overflow-hidden rounded-3xl bg-gradient-to-br from-neutral-50/50 to-white border border-neutral-200/50 shadow-2xl"
            ref={containerRef}
          >
            <div className="flex size-full max-h-[400px] max-w-6xl flex-row items-center justify-between px-12">
              {/* Step 1: GitHub Repo */}
              <div className="flex flex-col items-center text-center max-w-xs">
                <Circle
                  ref={div1Ref}
                  className="size-20 border-neutral-200/50 bg-white/90 shadow-xl"
                >
                  <Github className="w-8 h-8 text-neutral-700" />
                </Circle>
                <h3 className="text-lg font-semibold mb-2 text-neutral-900 mt-6">
                  GitHub Repository
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  Paste your repository URL
                </p>
              </div>

              {/* Step 2: Code Scraping */}
              <div className="flex flex-col items-center text-center max-w-xs">
                <Circle
                  ref={div2Ref}
                  className="size-20 border-blue-200/50 bg-blue-50/90 shadow-xl"
                >
                  <Code className="w-8 h-8 text-blue-600" />
                </Circle>
                <h3 className="text-lg font-semibold mb-2 text-neutral-900 mt-6">
                  Code Analysis
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  Intelligent code scraping and parsing
                </p>
              </div>

              {/* Step 3: AI Agent */}
              <div className="flex flex-col items-center text-center max-w-xs">
                <Circle
                  ref={div3Ref}
                  className="size-24 border-purple-200/50 bg-purple-50/90 shadow-2xl"
                >
                  <Brain className="w-10 h-10 text-purple-600" />
                </Circle>
                <h3 className="text-lg font-semibold mb-2 text-neutral-900 mt-6">
                  AI Analysis
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  Advanced reasoning and code analysis
                </p>
              </div>

              {/* Step 4: README Generation */}
              <div className="flex flex-col items-center text-center max-w-xs">
                <Circle
                  ref={div4Ref}
                  className="size-20 border-emerald-200/50 bg-emerald-50/90 shadow-xl"
                >
                  <FileText className="w-8 h-8 text-emerald-600" />
                </Circle>
                <h3 className="text-lg font-semibold mb-2 text-neutral-900 mt-6">
                  README Creation
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  Professional documentation generated
                </p>
              </div>

              {/* Step 5: Dashboard */}
              <div className="flex flex-col items-center text-center max-w-xs">
                <Circle
                  ref={div5Ref}
                  className="size-20 border-amber-200/50 bg-amber-50/90 shadow-xl"
                >
                  <Download className="w-8 h-8 text-amber-600" />
                </Circle>
                <h3 className="text-lg font-semibold mb-2 text-neutral-900 mt-6">
                  Download & Use
                </h3>
                <p className="text-sm text-neutral-600 leading-relaxed">
                  Copy or download your README
                </p>
              </div>
            </div>

            {/* Animated Beams - Fixed positioning and flow */}
            <AnimatedBeam
              containerRef={containerRef}
              fromRef={div1Ref}
              toRef={div3Ref}
              curvature={-50}
              pathColor="#e5e7eb"
              pathWidth={2}
              gradientStartColor="#6366f1"
              gradientStopColor="#8b5cf6"
              duration={4}
            />
            <AnimatedBeam
              containerRef={containerRef}
              fromRef={div2Ref}
              toRef={div3Ref}
              curvature={50}
              pathColor="#e5e7eb"
              pathWidth={2}
              gradientStartColor="#3b82f6"
              gradientStopColor="#6366f1"
              duration={4}
              delay={0.5}
            />
            <AnimatedBeam
              containerRef={containerRef}
              fromRef={div3Ref}
              toRef={div4Ref}
              curvature={-50}
              pathColor="#e5e7eb"
              pathWidth={2}
              gradientStartColor="#8b5cf6"
              gradientStopColor="#10b981"
              duration={4}
              delay={1}
              reverse
            />
            <AnimatedBeam
              containerRef={containerRef}
              fromRef={div3Ref}
              toRef={div5Ref}
              curvature={50}
              pathColor="#e5e7eb"
              pathWidth={2}
              gradientStartColor="#8b5cf6"
              gradientStopColor="#f59e0b"
              duration={4}
              delay={1.5}
              reverse
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-32 px-6 bg-gradient-to-br from-neutral-50/50 via-white to-neutral-50/50 relative">
        {/* Background decoration */}
        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-px h-32 bg-gradient-to-b from-transparent via-neutral-200 to-transparent" />

        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-bold mb-6 text-neutral-900 tracking-tight">
              Technical Achievements
            </h2>
            <p className="text-xl md:text-2xl text-neutral-600 font-light max-w-3xl mx-auto">
              Enterprise serverless architecture built by AWS Certified Developer in 2 weeks
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-neutral-200/50 hover:shadow-2xl transition-all duration-500 bg-white/70 backdrop-blur-sm group hover:border-neutral-300/50 hover:-translate-y-2">
              <CardHeader className="p-8">
                <div className="w-14 h-14 bg-gradient-to-br from-indigo-100 to-indigo-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Zap className="w-7 h-7 text-indigo-600" />
                </div>
                <CardTitle className="text-neutral-900 text-xl mb-3 font-semibold">
                  6 AWS Lambda Functions
                </CardTitle>
                <CardDescription className="text-neutral-600 leading-relaxed text-base">
                  Enterprise serverless architecture with Claude Sonnet 4 integration,
                  multi-phase development evolved through 3 iterations for peak accuracy
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-neutral-200/50 hover:shadow-2xl transition-all duration-500 bg-white/70 backdrop-blur-sm group hover:border-neutral-300/50 hover:-translate-y-2">
              <CardHeader className="p-8">
                <div className="w-14 h-14 bg-gradient-to-br from-emerald-100 to-emerald-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <FileText className="w-7 h-7 text-emerald-600" />
                </div>
                <CardTitle className="text-neutral-900 text-xl mb-3 font-semibold">
                  Microsoft Projects Proven
                </CardTitle>
                <CardDescription className="text-neutral-600 leading-relaxed text-base">
                  Generated READMEs for TypeScript, Calculator, VS Code projects.
                  Live production system with real usage, not just a demo
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-neutral-200/50 hover:shadow-2xl transition-all duration-500 bg-white/70 backdrop-blur-sm group hover:border-neutral-300/50 hover:-translate-y-2">
              <CardHeader className="p-8">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-100 to-blue-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Download className="w-7 h-7 text-blue-600" />
                </div>
                <CardTitle className="text-neutral-900 text-xl mb-3 font-semibold">
                  70% Cost Reduction
                </CardTitle>
                <CardDescription className="text-neutral-600 leading-relaxed text-base">
                  Automated solution eliminates hours of manual README writing.
                  $0.07 per generation - significantly cheaper than industry alternatives
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-neutral-200/50 hover:shadow-2xl transition-all duration-500 bg-white/70 backdrop-blur-sm group hover:border-neutral-300/50 hover:-translate-y-2">
              <CardHeader className="p-8">
                <div className="w-14 h-14 bg-gradient-to-br from-amber-100 to-amber-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Clock className="w-7 h-7 text-amber-600" />
                </div>
                <CardTitle className="text-neutral-900 text-xl mb-3 font-semibold">
                  Sub-30 Second Processing
                </CardTitle>
                <CardDescription className="text-neutral-600 leading-relaxed text-base">
                  Fast repository analysis with enterprise Step Functions orchestration.
                  Quality consistency and professional documentation every time
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-neutral-200/50 hover:shadow-2xl transition-all duration-500 bg-white/70 backdrop-blur-sm group hover:border-neutral-300/50 hover:-translate-y-2">
              <CardHeader className="p-8">
                <div className="w-14 h-14 bg-gradient-to-br from-purple-100 to-purple-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Github className="w-7 h-7 text-purple-600" />
                </div>
                <CardTitle className="text-neutral-900 text-xl mb-3 font-semibold">
                  Production-Ready System
                </CardTitle>
                <CardDescription className="text-neutral-600 leading-relaxed text-base">
                  Live system with proper monitoring, already helping developers with actual projects.
                  Built on AWS with enterprise-grade reliability
                </CardDescription>
              </CardHeader>
            </Card>
                  Supports 10+ languages and 15+ frameworks including React,
                  Vue, Angular, Django, Spring Boot, and more
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-neutral-200/50 hover:shadow-2xl transition-all duration-500 bg-white/70 backdrop-blur-sm group hover:border-neutral-300/50 hover:-translate-y-2">
              <CardHeader className="p-8">
                <div className="w-14 h-14 bg-gradient-to-br from-rose-100 to-rose-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Users className="w-7 h-7 text-rose-600" />
                </div>
                <CardTitle className="text-neutral-900 text-xl mb-3 font-semibold">
                  DynamoDB History Tracking
                </CardTitle>
                <CardDescription className="text-neutral-600 leading-relaxed text-base">
                  Complete generation history with AWS Cognito authentication,
                  comprehensive monitoring, and enterprise-grade security
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-6 bg-white relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-r from-neutral-50/30 via-transparent to-neutral-50/30" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-indigo-100/20 to-purple-100/20 rounded-full blur-3xl" />

        <div className="container mx-auto text-center max-w-4xl relative z-10">
          <h2 className="text-5xl md:text-6xl font-bold mb-6 text-neutral-900 tracking-tight">
            Experience Enterprise-Grade Documentation
          </h2>
          <p className="text-xl md:text-2xl text-neutral-600 mb-12 font-light leading-relaxed max-w-3xl mx-auto">
            Join the next generation of developers using AI-powered
            documentation with 95% accuracy, 16-second processing, and
            enterprise reliability
          </p>
          <Link href="/dashboard">
            <Button
              size="lg"
              className="bg-neutral-900 hover:bg-neutral-800 text-white text-xl px-12 py-6 h-auto shadow-2xl hover:shadow-3xl transition-all duration-300 group"
            >
              Launch SmartReadmeGen Platform
              <ArrowRight className="ml-3 w-6 h-6 transition-transform duration-300 group-hover:translate-x-1" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-neutral-900 text-white py-16 px-6 relative">
        <div className="container mx-auto text-center max-w-4xl">
          <div className="flex items-center justify-center space-x-3 mb-8">
            <div className="w-10 h-10 bg-gradient-to-br from-neutral-700 to-neutral-600 rounded-xl flex items-center justify-center shadow-lg">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-semibold tracking-tight">
              SmartReadmeGen
            </span>
          </div>
          <p className="text-neutral-400 text-lg font-light">
            &copy; 2024 SmartReadmeGen. All rights reserved.
          </p>
        </div>
      </footer>

      {/* Preview Navigation - Development Helper */}
      {/* <PreviewNavigation /> */}

      {/* Preview Test - Quick Test */}
      {/* <PreviewTest /> */}
    </div>
  );
}
