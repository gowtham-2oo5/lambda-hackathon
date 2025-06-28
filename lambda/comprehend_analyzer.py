"""
Amazon Comprehend Integration for README Content Analysis
Provides NLP analysis for professional content enhancement
"""

import boto3
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class ComprehendAnalysis:
    """Comprehensive Comprehend analysis result"""
    sentiment: Dict[str, Any]
    entities: List[Dict[str, Any]]
    key_phrases: List[Dict[str, Any]]
    syntax: List[Dict[str, Any]]
    language: Dict[str, Any]
    quality_score: float
    recommendations: List[str]

class ComprehendAnalyzer:
    """
    Amazon Comprehend integration for README content analysis
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.comprehend = boto3.client('comprehend', region_name=region)
        
        # Professional writing standards
        self.professional_keywords = {
            'positive': ['innovative', 'robust', 'scalable', 'efficient', 'secure', 'professional', 'comprehensive'],
            'technical': ['API', 'framework', 'architecture', 'implementation', 'integration', 'deployment'],
            'action': ['build', 'create', 'develop', 'implement', 'deploy', 'configure', 'optimize']
        }
        
        # Quality thresholds
        self.sentiment_threshold = 0.7  # Minimum positive sentiment
        self.confidence_threshold = 0.8  # Minimum confidence for entities
        
    def analyze_content(self, content: str, content_type: str = 'description') -> ComprehendAnalysis:
        """
        Comprehensive content analysis using all Comprehend features
        """
        logger.info(f"🔍 Analyzing {content_type} content ({len(content)} chars)")
        
        try:
            # Perform all Comprehend analyses
            sentiment_result = self._analyze_sentiment(content)
            entities_result = self._detect_entities(content)
            key_phrases_result = self._extract_key_phrases(content)
            syntax_result = self._analyze_syntax(content)
            language_result = self._detect_language(content)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(
                sentiment_result, entities_result, key_phrases_result, syntax_result
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                sentiment_result, entities_result, key_phrases_result, syntax_result, content
            )
            
            analysis = ComprehendAnalysis(
                sentiment=sentiment_result,
                entities=entities_result,
                key_phrases=key_phrases_result,
                syntax=syntax_result,
                language=language_result,
                quality_score=quality_score,
                recommendations=recommendations
            )
            
            logger.info(f"✅ Analysis complete - Quality: {quality_score:.1f}%")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Comprehend analysis failed: {e}")
            return self._create_fallback_analysis(content)
    
    def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Analyze sentiment for professional tone"""
        try:
            response = self.comprehend.detect_sentiment(
                Text=content[:5000],  # Comprehend limit
                LanguageCode='en'
            )
            
            sentiment = response['Sentiment']
            scores = response['SentimentScore']
            
            # Professional content should be neutral to positive
            is_professional = (
                sentiment in ['NEUTRAL', 'POSITIVE'] and
                scores.get('Positive', 0) + scores.get('Neutral', 0) > 0.7
            )
            
            return {
                'sentiment': sentiment,
                'scores': scores,
                'is_professional': is_professional,
                'confidence': max(scores.values())
            }
            
        except Exception as e:
            logger.error(f"❌ Sentiment analysis failed: {e}")
            return {'sentiment': 'NEUTRAL', 'scores': {}, 'is_professional': True, 'confidence': 0.5}
    
    def _detect_entities(self, content: str) -> List[Dict[str, Any]]:
        """Detect technical entities and terms"""
        try:
            response = self.comprehend.detect_entities(
                Text=content[:5000],
                LanguageCode='en'
            )
            
            entities = []
            for entity in response['Entities']:
                if entity['Score'] >= self.confidence_threshold:
                    # Categorize entity for README context
                    category = self._categorize_entity(entity['Text'], entity['Type'])
                    
                    entities.append({
                        'text': entity['Text'],
                        'type': entity['Type'],
                        'category': category,
                        'score': entity['Score'],
                        'begin_offset': entity['BeginOffset'],
                        'end_offset': entity['EndOffset']
                    })
            
            # Sort by relevance score
            entities.sort(key=lambda x: x['score'], reverse=True)
            return entities[:20]  # Top 20 entities
            
        except Exception as e:
            logger.error(f"❌ Entity detection failed: {e}")
            return []
    
    def _extract_key_phrases(self, content: str) -> List[Dict[str, Any]]:
        """Extract key phrases for highlighting"""
        try:
            response = self.comprehend.detect_key_phrases(
                Text=content[:5000],
                LanguageCode='en'
            )
            
            key_phrases = []
            for phrase in response['KeyPhrases']:
                if phrase['Score'] >= self.confidence_threshold:
                    # Analyze phrase relevance for README
                    relevance = self._assess_phrase_relevance(phrase['Text'])
                    
                    key_phrases.append({
                        'text': phrase['Text'],
                        'score': phrase['Score'],
                        'relevance': relevance,
                        'begin_offset': phrase['BeginOffset'],
                        'end_offset': phrase['EndOffset']
                    })
            
            # Sort by combined score and relevance
            key_phrases.sort(key=lambda x: x['score'] * x['relevance'], reverse=True)
            return key_phrases[:15]  # Top 15 phrases
            
        except Exception as e:
            logger.error(f"❌ Key phrase extraction failed: {e}")
            return []
    
    def _analyze_syntax(self, content: str) -> List[Dict[str, Any]]:
        """Analyze syntax for readability"""
        try:
            response = self.comprehend.detect_syntax(
                Text=content[:5000],
                LanguageCode='en'
            )
            
            syntax_analysis = []
            pos_counts = {}
            
            for token in response['SyntaxTokens']:
                pos_tag = token['PartOfSpeech']['Tag']
                pos_counts[pos_tag] = pos_counts.get(pos_tag, 0) + 1
                
                # Focus on important syntax elements
                if pos_tag in ['NOUN', 'VERB', 'ADJ', 'ADV']:
                    syntax_analysis.append({
                        'text': token['Text'],
                        'pos_tag': pos_tag,
                        'score': token['PartOfSpeech']['Score'],
                        'begin_offset': token['BeginOffset'],
                        'end_offset': token['EndOffset']
                    })
            
            # Calculate readability metrics
            total_tokens = len(response['SyntaxTokens'])
            noun_ratio = pos_counts.get('NOUN', 0) / total_tokens if total_tokens > 0 else 0
            verb_ratio = pos_counts.get('VERB', 0) / total_tokens if total_tokens > 0 else 0
            
            return {
                'tokens': syntax_analysis[:50],  # Top 50 important tokens
                'pos_distribution': pos_counts,
                'readability_metrics': {
                    'noun_ratio': noun_ratio,
                    'verb_ratio': verb_ratio,
                    'total_tokens': total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Syntax analysis failed: {e}")
            return {'tokens': [], 'pos_distribution': {}, 'readability_metrics': {}}
    
    def _detect_language(self, content: str) -> Dict[str, Any]:
        """Detect language and confidence"""
        try:
            response = self.comprehend.detect_dominant_language(
                Text=content[:5000]
            )
            
            if response['Languages']:
                dominant = response['Languages'][0]
                return {
                    'language_code': dominant['LanguageCode'],
                    'score': dominant['Score'],
                    'is_english': dominant['LanguageCode'] == 'en'
                }
            else:
                return {'language_code': 'en', 'score': 0.5, 'is_english': True}
                
        except Exception as e:
            logger.error(f"❌ Language detection failed: {e}")
            return {'language_code': 'en', 'score': 0.5, 'is_english': True}
    
    def _categorize_entity(self, text: str, entity_type: str) -> str:
        """Categorize entity for README context"""
        text_lower = text.lower()
        
        # Technical terms
        if any(tech in text_lower for tech in ['api', 'sdk', 'framework', 'library', 'database']):
            return 'technical'
        
        # Programming languages
        if any(lang in text_lower for lang in ['python', 'javascript', 'java', 'react', 'django']):
            return 'technology'
        
        # Organizations/Companies
        if entity_type == 'ORGANIZATION':
            return 'organization'
        
        # Persons (contributors, authors)
        if entity_type == 'PERSON':
            return 'contributor'
        
        # Locations (deployment regions, etc.)
        if entity_type == 'LOCATION':
            return 'location'
        
        return 'general'
    
    def _assess_phrase_relevance(self, phrase: str) -> float:
        """Assess phrase relevance for README content"""
        phrase_lower = phrase.lower()
        relevance_score = 0.5  # Base score
        
        # Technical relevance
        for keyword_list in self.professional_keywords.values():
            if any(keyword in phrase_lower for keyword in keyword_list):
                relevance_score += 0.3
                break
        
        # Length penalty for very long phrases
        if len(phrase.split()) > 6:
            relevance_score -= 0.2
        
        # Boost for action-oriented phrases
        if any(action in phrase_lower for action in ['how to', 'getting started', 'installation', 'usage']):
            relevance_score += 0.4
        
        return min(1.0, max(0.1, relevance_score))
    
    def _calculate_quality_score(self, sentiment: Dict, entities: List, key_phrases: List, syntax: Dict) -> float:
        """Calculate overall content quality score"""
        score = 0.0
        
        # Sentiment score (25%)
        if sentiment.get('is_professional', False):
            score += 25.0
        else:
            score += sentiment.get('confidence', 0) * 15.0
        
        # Entity richness (25%)
        entity_score = min(25.0, len(entities) * 2.5)  # Up to 10 entities
        score += entity_score
        
        # Key phrase quality (25%)
        if key_phrases:
            avg_phrase_score = sum(p['score'] * p['relevance'] for p in key_phrases) / len(key_phrases)
            score += avg_phrase_score * 25.0
        
        # Syntax quality (25%)
        readability = syntax.get('readability_metrics', {})
        if readability:
            # Good balance of nouns and verbs indicates clear writing
            noun_ratio = readability.get('noun_ratio', 0)
            verb_ratio = readability.get('verb_ratio', 0)
            
            if 0.2 <= noun_ratio <= 0.4 and 0.1 <= verb_ratio <= 0.3:
                score += 25.0
            else:
                score += 15.0
        
        return min(100.0, score)
    
    def _generate_recommendations(self, sentiment: Dict, entities: List, key_phrases: List, 
                                syntax: Dict, content: str) -> List[str]:
        """Generate content improvement recommendations"""
        recommendations = []
        
        # Sentiment recommendations
        if not sentiment.get('is_professional', True):
            recommendations.append("Consider using more neutral or positive language for professional tone")
        
        # Entity recommendations
        if len(entities) < 3:
            recommendations.append("Add more specific technical terms and technologies to improve clarity")
        
        # Key phrase recommendations
        if len(key_phrases) < 5:
            recommendations.append("Include more descriptive phrases about features and benefits")
        
        # Syntax recommendations
        readability = syntax.get('readability_metrics', {})
        if readability.get('noun_ratio', 0) > 0.5:
            recommendations.append("Reduce noun density for better readability")
        
        if readability.get('verb_ratio', 0) < 0.1:
            recommendations.append("Add more action words to make content more engaging")
        
        # Length recommendations
        if len(content) < 100:
            recommendations.append("Expand content with more detailed information")
        elif len(content) > 2000:
            recommendations.append("Consider breaking long content into smaller sections")
        
        return recommendations
    
    def _create_fallback_analysis(self, content: str) -> ComprehendAnalysis:
        """Create fallback analysis when Comprehend fails"""
        return ComprehendAnalysis(
            sentiment={'sentiment': 'NEUTRAL', 'is_professional': True, 'confidence': 0.5},
            entities=[],
            key_phrases=[],
            syntax={'tokens': [], 'readability_metrics': {}},
            language={'language_code': 'en', 'is_english': True, 'score': 0.5},
            quality_score=60.0,
            recommendations=["Comprehend analysis unavailable - using fallback assessment"]
        )
    
    def enhance_content_with_analysis(self, content: str, analysis: ComprehendAnalysis) -> str:
        """Enhance content based on Comprehend analysis"""
        enhanced_content = content
        
        # Apply recommendations
        for recommendation in analysis.recommendations:
            if "more neutral or positive language" in recommendation:
                enhanced_content = self._improve_tone(enhanced_content)
            elif "more specific technical terms" in recommendation:
                enhanced_content = self._add_technical_context(enhanced_content, analysis.entities)
            elif "more descriptive phrases" in recommendation:
                enhanced_content = self._enhance_descriptions(enhanced_content, analysis.key_phrases)
        
        return enhanced_content
    
    def _improve_tone(self, content: str) -> str:
        """Improve content tone for professional writing"""
        # Replace negative or weak language
        improvements = {
            r'\bcan\'t\b': 'cannot',
            r'\bwon\'t\b': 'will not',
            r'\bisn\'t\b': 'is not',
            r'\bdon\'t\b': 'do not',
            r'\bmaybe\b': 'potentially',
            r'\bprobably\b': 'likely',
            r'\bbasic\b': 'fundamental',
            r'\bsimple\b': 'streamlined'
        }
        
        for pattern, replacement in improvements.items():
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def _add_technical_context(self, content: str, entities: List[Dict]) -> str:
        """Add technical context based on detected entities"""
        # This is a simplified implementation
        # In practice, you'd use the entities to enhance technical descriptions
        return content
    
    def _enhance_descriptions(self, content: str, key_phrases: List[Dict]) -> str:
        """Enhance descriptions using key phrases"""
        # This is a simplified implementation
        # In practice, you'd use key phrases to improve content richness
        return content
