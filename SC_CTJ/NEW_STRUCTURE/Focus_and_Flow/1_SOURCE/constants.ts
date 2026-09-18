
import { Prompt, QuizQuestion } from './types';

export const APP_VERSION = '1.1';
export const STORAGE_KEY_JOURNAL = 'ctj.mvp.journal';
export const STORAGE_KEY_SETTINGS = 'ctj.mvp.settings';

export const PROMPTS: Prompt[] = [
  {
    id: 'mvp-primary',
    title: 'Focus & Flow: The One Decision',
    part: 0,
    content: `Name one decision that would meaningfully improve your day today.

1. State it clearly in one sentence.
2. Run a quick bias check: What might you be assuming that could be wrong?
3. Evidence check: What two facts support this move—and what one fact challenges it?
4. Action: What is the smallest next step you can do in 5 minutes—and when will you do it today?`
  },
  {
    id: 'minor-part1',
    title: 'Logic Ladder Lite (Clarity)',
    part: 1,
    content: `State your goal in one sentence. Convert it into an IF–THEN rule.
IF [specific condition occurs], THEN [specific action you will take].
Refine once to remove ambiguity.`
  },
  {
    id: 'minor-part2',
    title: 'Micro-Experiment (Action)',
    part: 2,
    content: `Design a 1-step test you can run today to learn whether your idea is sound.
State your hypothesis, the smallest action to test it, and what result would make you adjust.`
  },
  {
    id: 'minor-part3',
    title: 'Meaning Check (Purpose)',
    part: 3,
    content: `In one sentence, say why this matters to you.
Name one boundary that protects your energy while you pursue it, and one support you’ll use.`
  }
];

export const WELCOME_COPY = {
  title: "Welcome to the Beginning",
  subtitle: "You're Among the First",
  body: [
    "Welcome to CTJ: Focus & Flow™—the minimum viable product that validates a bold hypothesis: what if strategic thinking could be trained like a muscle, three minutes at a time?",
    "This isn't a finished product. It's a proof of concept. You're experiencing the core mechanism that will power The Critical Thinker's Journey™—a complete cognitive development system we're building with early participants like you.",
    "Local-first. Private. Entirely yours."
  ]
};

export const FRAMEWORK_CONTENT = {
  mindset: "Be skeptical. Examine evidence. Be open to change.",
  checklist: "Source reliability? Motive? Coherence with facts? Tested evidence?",
  action: "What is your smallest next step in 5 minutes?"
};

export const BIAS_QUIZ_QUESTIONS: QuizQuestion[] = [
  {
    id: 1,
    question: "You only seek news that agrees with your view. This is:",
    options: ["Critical Analysis", "Confirmation Bias", "Deductive Reasoning"],
    correctIndex: 1,
    explanation: "Confirmation bias ignores contradictory evidence."
  },
  {
    id: 2,
    question: "A colleague says: 'We've always done it this way.' They are using:",
    options: ["Appeal to Tradition", "First Principles", "Strategic Vision"],
    correctIndex: 0,
    explanation: "Past practice does not guarantee future validity."
  },
  {
    id: 3,
    question: "You assume a quiet person is angry. You are:",
    options: ["Reading Minds", "Projecting", "Inferring without Data"],
    correctIndex: 2,
    explanation: "Inference requires evidence, not just observation."
  }
];

// Heuristics for the Local AI Assist
export const AI_HEURISTICS = {
  absolutes: ['always', 'never', 'everyone', 'nobody', 'perfect', 'impossible'],
  causality: ['because', 'due to', 'since', 'therefore', 'leads to', 'results in'],
  emotion: ['feel', 'afraid', 'worried', 'excited', 'hate', 'love', 'anxious'],
  uncertainty: ['maybe', 'perhaps', 'might', 'guess', 'assume'],
  action: ['will', 'going to', 'step', 'plan', 'schedule', 'commit']
};
