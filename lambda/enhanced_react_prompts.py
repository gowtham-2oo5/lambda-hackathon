"""
Enhanced ReAct Prompting System for Better Content Generation
"""

def create_enhanced_reasoning_prompt(cycle: int, context: dict, previous_results: list, quality_history: list) -> str:
    """Create enhanced reasoning prompt for more engaging content"""
    
    project_type = context.get('project_type', 'Software Application')
    primary_language = context.get('primary_language', 'Unknown')
    frameworks = context.get('frameworks', [])
    complexity = context.get('complexity_level', 'simple')
    target_audience = context.get('target_audience', 'developers')
    
    return f"""
You are an expert technical writer and ReAct agent specializing in creating ENGAGING, COMPELLING README documentation. This is cycle {cycle} of 4.

PROJECT CONTEXT:
- Type: {project_type}
- Language: {primary_language}
- Frameworks: {frameworks}
- Complexity: {complexity}
- Target Audience: {target_audience}

QUALITY HISTORY: {quality_history}
PREVIOUS ACTIONS: {len(previous_results)} completed

CONTENT QUALITY GOALS:
1. ENGAGING: Use power words, active voice, compelling descriptions
2. PROFESSIONAL: Maintain technical accuracy while being approachable
3. VISUAL: Include emojis, badges, proper formatting for visual appeal
4. ACTIONABLE: Clear, specific instructions that developers can follow
5. COMPREHENSIVE: Cover all essential aspects without being overwhelming

WRITING STYLE REQUIREMENTS:
- Use active voice ("Build amazing apps" not "Apps can be built")
- Include power words: "powerful", "streamlined", "cutting-edge", "robust"
- Add context and benefits ("Why should developers care?")
- Make it scannable with bullet points, headers, code blocks
- Include specific examples and use cases

REASONING TASK:
Analyze the current README content quality and create an action plan to make it MORE ENGAGING and COMPELLING while maintaining technical accuracy.

Focus areas for improvement:
- Content engagement and readability
- Technical depth with accessibility
- Visual appeal and formatting
- Clear value proposition
- Actionable instructions

Respond with JSON:
{{
  "analysis": "Your detailed reasoning about current content quality and engagement level",
  "action_plan": [
    {{
      "type": "enhance_content|optimize_language|generate_section|validate_quality",
      "priority": 1-5,
      "data": {{
        "section": "target_section",
        "focus": "engagement|clarity|technical_depth|visual_appeal",
        "enhancement_type": "power_words|active_voice|examples|formatting"
      }}
    }}
  ],
  "confidence": 0.0-1.0,
  "engagement_score": 0-100,
  "improvement_areas": ["specific areas needing enhancement"]
}}
"""

def create_content_enhancement_prompt(section: str, content: str, project_context: dict) -> str:
    """Create prompt for content enhancement with engaging language"""
    
    return f"""
You are a master technical writer specializing in creating COMPELLING, ENGAGING developer documentation.

TASK: Transform the following {section} content to be MORE ENGAGING and COMPELLING while maintaining technical accuracy.

CURRENT CONTENT:
{content}

PROJECT CONTEXT:
- Type: {project_context.get('project_type', 'Software Application')}
- Language: {project_context.get('primary_language', 'Unknown')}
- Frameworks: {project_context.get('frameworks', [])}

ENHANCEMENT REQUIREMENTS:
1. USE POWER WORDS: Replace weak words with strong ones
   - "simple" → "streamlined" or "intuitive"
   - "basic" → "essential" or "fundamental"
   - "good" → "exceptional" or "robust"

2. ACTIVE VOICE: Make it action-oriented
   - "Can be used" → "Empowers you to"
   - "Is built with" → "Leverages cutting-edge"

3. ADD VALUE CONTEXT: Explain WHY it matters
   - Don't just say "JWT authentication"
   - Say "Enterprise-grade JWT authentication for bulletproof security"

4. INCLUDE BENEFITS: What does the user gain?
   - "Fast setup" → "Get up and running in under 5 minutes"
   - "Easy to use" → "Intuitive API that developers love"

5. VISUAL LANGUAGE: Paint a picture
   - "Comprehensive documentation" → "Crystal-clear documentation that guides you every step"

6. SPECIFIC EXAMPLES: Replace generic with specific
   - "Good performance" → "Handles 10,000+ requests per second"

ENHANCED CONTENT GUIDELINES:
- Start with impact/benefit
- Use specific, measurable claims when possible
- Include emotional triggers (excitement, confidence, ease)
- Make it scannable with formatting
- End with clear next steps

Transform the content to be 2x more engaging while keeping it professional and accurate.
"""

def create_quality_validation_prompt(content: str, criteria: dict) -> str:
    """Create prompt for quality validation with engagement focus"""
    
    return f"""
You are a senior technical writing reviewer evaluating README content for ENGAGEMENT and QUALITY.

CONTENT TO REVIEW:
{content}

EVALUATION CRITERIA:
1. ENGAGEMENT SCORE (0-100):
   - Does it grab attention immediately?
   - Uses compelling language and power words?
   - Includes clear value propositions?
   - Makes developers excited to try it?

2. CLARITY SCORE (0-100):
   - Easy to scan and understand?
   - Clear structure and flow?
   - Actionable instructions?
   - No jargon without explanation?

3. COMPLETENESS SCORE (0-100):
   - Covers all essential information?
   - Includes examples and use cases?
   - Has clear next steps?
   - Addresses common questions?

4. PROFESSIONALISM SCORE (0-100):
   - Maintains technical accuracy?
   - Appropriate tone for developers?
   - Consistent formatting?
   - Error-free content?

SPECIFIC ISSUES TO CHECK:
- Weak or passive language
- Missing value propositions
- Unclear instructions
- Poor visual formatting
- Generic descriptions
- Missing context or benefits

Provide detailed feedback with specific improvement suggestions.

Respond with JSON:
{{
  "engagement_score": 0-100,
  "clarity_score": 0-100,
  "completeness_score": 0-100,
  "professionalism_score": 0-100,
  "overall_score": 0-100,
  "strengths": ["what works well"],
  "weaknesses": ["specific issues found"],
  "improvement_suggestions": ["actionable recommendations"],
  "engagement_improvements": ["specific ways to make it more compelling"]
}}
"""

def create_language_optimization_prompt(text: str, focus: str, audience: str) -> str:
    """Create prompt for language optimization"""
    
    return f"""
You are a copywriting expert specializing in technical documentation that CONVERTS and ENGAGES.

TASK: Optimize the following text for {focus} targeting {audience}.

TEXT TO OPTIMIZE:
{text}

OPTIMIZATION FOCUS: {focus}

LANGUAGE TRANSFORMATION RULES:

1. POWER WORDS REPLACEMENT:
   - Weak → Strong
   - "use" → "leverage", "harness", "utilize"
   - "make" → "create", "build", "craft"
   - "help" → "empower", "enable", "accelerate"
   - "good" → "exceptional", "outstanding", "superior"

2. ACTIVE VOICE CONVERSION:
   - "X can be done" → "You can do X"
   - "It is built" → "We built it"
   - "Features are provided" → "You get features"

3. BENEFIT-DRIVEN LANGUAGE:
   - Feature → Benefit
   - "Has authentication" → "Keeps your data secure"
   - "Includes API" → "Integrates seamlessly with your apps"

4. EMOTIONAL TRIGGERS:
   - Add excitement: "Discover", "Unlock", "Transform"
   - Build confidence: "Proven", "Reliable", "Battle-tested"
   - Create urgency: "Get started now", "Join thousands"

5. SPECIFIC OVER GENERIC:
   - "Fast" → "Lightning-fast (< 100ms response)"
   - "Easy" → "Set up in 3 simple steps"
   - "Powerful" → "Handles 50,000+ concurrent users"

Return the optimized text that is 50% more engaging while maintaining accuracy.
"""
