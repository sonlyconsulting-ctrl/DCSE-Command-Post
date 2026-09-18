import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AppState, AppAction, AppSettings, JournalState } from '../types';
import { STORAGE_KEY_JOURNAL, STORAGE_KEY_SETTINGS, PROMPTS } from '../constants';

const defaultSettings: AppSettings = {
  highContrast: false,
  dyslexiaFont: false,
  reducedMotion: false,
  textScale: 1,
};

const defaultJournal: JournalState = {
  promptId: PROMPTS[0].id,
  content: '',
  wordCount: 0,
  charCount: 0,
  lastSaved: null,
};

const initialState: AppState = {
  currentView: 'welcome',
  settings: defaultSettings,
  journal: defaultJournal,
};

const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
}>({ state: initialState, dispatch: () => null });

const reducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'SET_VIEW':
      return { ...state, currentView: action.payload };
    case 'TOGGLE_SETTING':
      const newSettings = {
        ...state.settings,
        [action.payload]: !state.settings[action.payload],
      };
      localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify(newSettings));
      return { ...state, settings: newSettings };
    case 'SET_TEXT_SCALE':
      return { ...state, settings: { ...state.settings, textScale: action.payload } };
    case 'UPDATE_JOURNAL':
      const newJournal = { ...state.journal, ...action.payload };
      // Calculate counts if content changed
      if (action.payload.content !== undefined) {
        newJournal.charCount = action.payload.content.length;
        newJournal.wordCount = action.payload.content.trim().split(/\s+/).filter(w => w.length > 0).length;
        newJournal.lastSaved = new Date().toISOString();
      }
      localStorage.setItem(STORAGE_KEY_JOURNAL, JSON.stringify(newJournal));
      return { ...state, journal: newJournal };
    case 'RESET_SESSION':
      localStorage.removeItem(STORAGE_KEY_JOURNAL);
      return { ...state, journal: defaultJournal, currentView: 'welcome' };
    default:
      return state;
  }
};

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  // Initialize from LocalStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem(STORAGE_KEY_SETTINGS);
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        Object.keys(parsed).forEach((key) => {
          if (state.settings[key as keyof AppSettings] !== parsed[key]) {
             dispatch({ type: 'TOGGLE_SETTING', payload: key as keyof Omit<AppSettings, 'textScale'> });
          }
        });
      } catch (e) { console.error("Failed to load settings", e); }
    }

    const savedJournal = localStorage.getItem(STORAGE_KEY_JOURNAL);
    if (savedJournal) {
      try {
        dispatch({ type: 'UPDATE_JOURNAL', payload: JSON.parse(savedJournal) });
      } catch (e) { console.error("Failed to load journal", e); }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Apply visual settings to body
  useEffect(() => {
    const body = document.body;
    if (state.settings.highContrast) body.classList.add('high-contrast');
    else body.classList.remove('high-contrast');

    if (state.settings.dyslexiaFont) body.classList.add('font-dyslexic');
    else body.classList.remove('font-dyslexic');

    if (state.settings.reducedMotion) body.classList.add('reduce-motion');
    else body.classList.remove('reduce-motion');
    
  }, [state.settings]);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);