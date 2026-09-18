import React from 'react';
import { FileText, Code, Download, CheckCircle } from 'lucide-react';
import { jsPDF } from 'jspdf';
import { useAppContext } from '../context/AppContext';
import { PROMPTS } from '../constants';

export const ExportView: React.FC = () => {
  const { state, dispatch } = useAppContext();
  const prompt = PROMPTS.find(p => p.id === state.journal.promptId) || PROMPTS[0];

  const handleDownloadTXT = () => {
    const text = `CTJ: Focus & Flow™ Session\nDate: ${new Date().toLocaleString()}\n\nPrompt: ${prompt.title}\n\n${prompt.content}\n\n---\n\nReflection:\n${state.journal.content}`;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ctj-session-${new Date().toISOString().slice(0, 10)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadJSON = () => {
    const data = {
      meta: {
        app: "CTJ: Focus & Flow MVP v1.0",
        timestamp: new Date().toISOString(),
      },
      prompt: {
        id: prompt.id,
        title: prompt.title,
        body: prompt.content
      },
      journal: {
        content: state.journal.content,
        wordCount: state.journal.wordCount,
        charCount: state.journal.charCount
      }
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ctj-session-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadPDF = () => {
    const doc = new jsPDF();
    const margin = 20;
    let y = 20;

    // Header
    doc.setFontSize(10);
    doc.setTextColor(150);
    doc.text("CTJ: Focus & Flow™ MVP v1.0", margin, y);
    doc.text(new Date().toLocaleDateString(), 190 - margin, y, { align: 'right' });
    y += 15;

    // Prompt Title
    doc.setFontSize(16);
    doc.setTextColor(0);
    doc.setFont("helvetica", "bold");
    doc.text(prompt.title, margin, y);
    y += 10;

    // Prompt Body
    doc.setFontSize(11);
    doc.setFont("helvetica", "italic");
    doc.setTextColor(80);
    const promptLines = doc.splitTextToSize(prompt.content, 170);
    doc.text(promptLines, margin, y);
    y += (promptLines.length * 7) + 10;

    // Divider
    doc.setDrawColor(200);
    doc.line(margin, y, 190, y);
    y += 15;

    // Journal Entry
    doc.setFontSize(12);
    doc.setFont("times", "normal");
    doc.setTextColor(0);
    const contentLines = doc.splitTextToSize(state.journal.content, 170);
    
    // Pagination logic
    contentLines.forEach((line: string) => {
      if (y > 270) {
        doc.addPage();
        y = 20;
      }
      doc.text(line, margin, y);
      y += 7;
    });

    // Footer
    const pageCount = doc.internal.pages.length - 1; // fix jspdf page count bug
    for(let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text("Sonly Consulting - Private & Local", 105, 290, { align: "center" });
    }

    doc.save(`ctj-session-${new Date().toISOString().slice(0, 10)}.pdf`);
  };

  return (
    <div className="max-w-xl mx-auto space-y-8 text-center animate-fade-in">
      <div className="space-y-2">
        <CheckCircle size={48} className="mx-auto text-sc-gold mb-4" />
        <h2 className="text-3xl font-bold text-sc-ivory">Session Complete</h2>
        <p className="text-sc-ivory/70">
          Your thoughts are captured. Export them now to keep a permanent record.
          <br/><span className="text-xs text-sc-muted">(Data is wiped from browser upon completion)</span>
        </p>
      </div>

      <div className="grid gap-4">
        <button
          onClick={handleDownloadPDF}
          className="w-full bg-sc-ivory hover:bg-white text-sc-navy font-bold p-4 rounded-xl flex items-center justify-between group transition-all focus-ring"
        >
          <div className="flex items-center gap-4">
            <div className="bg-red-100 p-2 rounded-lg text-red-600">
              <FileText size={24} />
            </div>
            <div className="text-left">
              <div className="text-lg">Download PDF</div>
              <div className="text-xs text-sc-muted font-normal">Best for reading & printing</div>
            </div>
          </div>
          <Download size={20} className="text-sc-muted group-hover:text-sc-navy" />
        </button>

        <button
          onClick={handleDownloadJSON}
          className="w-full bg-sc-navy border border-sc-gold/30 hover:border-sc-gold text-sc-ivory font-bold p-4 rounded-xl flex items-center justify-between group transition-all focus-ring"
        >
          <div className="flex items-center gap-4">
            <div className="bg-blue-900/50 p-2 rounded-lg text-blue-300">
              <Code size={24} />
            </div>
            <div className="text-left">
              <div className="text-lg">Download JSON</div>
              <div className="text-xs text-sc-muted font-normal">Raw data for backup</div>
            </div>
          </div>
          <Download size={20} className="text-sc-muted group-hover:text-sc-gold" />
        </button>
        
        <button
          onClick={handleDownloadTXT}
          className="w-full bg-transparent border border-sc-muted/30 hover:bg-sc-ivory/5 text-sc-ivory font-semibold p-4 rounded-xl flex items-center justify-between group transition-all focus-ring"
        >
             <div className="flex items-center gap-4">
                 <div className="text-sc-muted">TXT</div>
                 <span className="text-left">Plain Text</span>
             </div>
             <Download size={20} className="text-sc-muted group-hover:text-sc-ivory" />
        </button>
      </div>

      <button
        onClick={() => dispatch({ type: 'SET_VIEW', payload: 'completion' })}
        className="text-sc-gold hover:text-white underline underline-offset-4 text-sm focus-ring rounded p-1"
      >
        Skip Export & Finish
      </button>
    </div>
  );
};