import React, { useState, useEffect } from 'react';
import { Layout } from './components/Layout';
import { WelcomeView } from './components/WelcomeView';
import { WarmupView } from './components/WarmupView';
import { JournalView } from './components/JournalView';
import { ExportView } from './components/ExportView';
import { CompletionView } from './components/CompletionView';
import { AppProvider, useAppContext } from './context/AppContext';

const AppContent: React.FC = () => {
  const { state } = useAppContext();

  const renderView = () => {
    switch (state.currentView) {
      case 'welcome': return <WelcomeView />;
      case 'warmup': return <WarmupView />;
      case 'journal': return <JournalView />;
      case 'export': return <ExportView />;
      case 'completion': return <CompletionView />;
      default: return <WelcomeView />;
    }
  };

  return (
    <Layout>
      <div className="w-full max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        {renderView()}
      </div>
    </Layout>
  );
};

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}