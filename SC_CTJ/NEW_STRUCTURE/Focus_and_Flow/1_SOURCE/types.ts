
export type ViewState = 'welcome' | 'warmup' | 'journal' | 'export' | 'completion';

export interface Prompt {
  id: string;
  title: string;
  part: number; // 0 for MVP exclusive, 1-3 for parts
  content: string;
}

export interface AppSettings {
  highContrast: boolean;
  dyslexiaFont: boolean;
  reducedMotion: boolean;
  textScale: number;
}

export interface JournalState {
  promptId: string;
  content: string;
  wordCount: number;
  charCount: number;
  lastSaved: string | null;
}

export interface AppState {
  currentView: ViewState;
  settings: AppSettings;
  journal: JournalState;
}

export interface AIAnalysis {
  score: number;
  tone: 'neutral' | 'emotional' | 'analytical';
  suggestions: string[];
}

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
}

export type AppAction =
  | { type: 'SET_VIEW'; payload: ViewState }
  | { type: 'TOGGLE_SETTING'; payload: keyof Omit<AppSettings, 'textScale'> }
  | { type: 'SET_TEXT_SCALE'; payload: number }
  | { type: 'UPDATE_JOURNAL'; payload: Partial<JournalState> }
  | { type: 'RESET_SESSION' };
