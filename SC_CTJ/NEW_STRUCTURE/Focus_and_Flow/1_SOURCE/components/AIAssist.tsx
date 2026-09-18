
import React, { useEffect, useState } from 'react';
import { Sparkles, AlertCircle, Lightbulb, ArrowRight } from 'lucide-react';
import { AIAnalysis } from '../types';
import { AI_HEURISTICS } from '../constants';

interface AIAssistProps {
  content: string;
}

export const AIAssist: React.FC<AIAssistProps> = ({ content }) => {
  const [analysis, setAnalysis] = useState<AIAnalysis | null>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Debounce the analysis to avoid flickering
    const timer = setTimeout(() => {
      analyzeText(content);
    }, 800);

    return () => clearTimeout(timer);
  }, [content]);

  const analyzeText = (text: string) => {
    if (!text || text.length < 10) {
      setAnalysis(null);
      setIsVisible(false);
      return;
    }

    const lowerText = text.toLowerCase();
    const suggestions: string[] = [];
    let score = 0;

    // 1. Check for Absolutes (Bias Check)
    const foundAbsolutes = AI_HEURISTICS.absolutes.filter(w => lowerText.includes(w));
    if (foundAbsolutes.length > 0) {
      suggestions.push(`Watch out for absolutes like "${foundAbsolutes[0]}". Is this true in every single case?`);
    } else {
      score += 1;
    }

    // 2. Check for Causality (Logic Check)
    const hasCausality = AI_HEURISTICS.causality.some(w => lowerText.includes(w));
    if (!hasCausality && text.length > 50) {
      suggestions.push("Connect your thoughts with reasoning. Try using 'because' or 'therefore' to deepen the logic.");
    } else {
      score += 1;
    }

    // 3. Action Orientation (Action Check)
    const hasAction = AI_HEURISTICS.action.some(w => lowerText.includes(w));
    if (!hasAction && text.length > 100) {
      suggestions.push("Move to action. usage verbs like 'I will' or 'I plan to' to solidify your intent.");
    }

    // 4. Length/Depth Check
    if (text.length < 50) {
      suggestions.push("Go deeper. What is the evidence for this?");
    }

    setAnalysis({
      score,
      tone: 'neutral', // simplified for MVP
      suggestions
    });
    
    if (suggestions.length > 0) setIsVisible(true);
  };

  if (!analysis || !isVisible || analysis.suggestions.length === 0) return null;

  return (
    <div className="mt-4 animate-fade-in">
      <div className="bg-sc-navy border border-sc-gold/30 rounded-xl overflow-hidden shadow-lg">
        <div className="bg-sc-gold/10 px-4 py-2 flex items-center justify-between border-b border-sc-gold/20">
          <div className="flex items-center gap-2">
            <Sparkles size={16} className="text-sc-gold animate-pulse" />
            <span className="text-xs font-bold text-sc-gold uppercase tracking-wider">AI Thinking Partner</span>
          </div>
          <span className="text-[10px] text-sc-muted">Local Intelligence • Private</span>
        </div>
        
        <div className="p-4 space-y-3">
          {analysis.suggestions.slice(0, 2).map((suggestion, idx) => (
            <div key={idx} className="flex gap-3 items-start">
              {idx === 0 ? <AlertCircle size={16} className="text-sc-gold mt-0.5 shrink-0" /> : <Lightbulb size={16} className="text-sc-gold mt-0.5 shrink-0" />}
              <p className="text-sm text-sc-ivory/90 leading-relaxed">{suggestion}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
