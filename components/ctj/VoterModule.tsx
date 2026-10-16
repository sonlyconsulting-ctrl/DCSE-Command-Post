import React, { useState, useMemo } from 'react';
import type {
  CivicPriorityImperative,
  SignalFilterTestCase,
  OutcomeModelProposal,
  CandidateProfile,
  CandidateCalculatedAlignment,
  ReferendumProposition,
  TradeoffDilemma,
  DissonanceRule,
  TestingPreset,
  CivicClarityCardState,
  VoterModuleProps,
} from '../../types/ctj-voter';
import voterData from '../../content/ctj-voter.json';

export default function VoterModule({
  initialPresetId = 'PRESET-01',
  testingMode = true,
  onClarityCardExport,
  className = '',
}: VoterModuleProps) {
  const presets = voterData.testing_presets as TestingPreset[];
  const initialPreset = presets.find((p) => p.preset_id === initialPresetId) || presets[0];

  const imperatives = (voterData.framework_steps[0] as unknown as { imperatives: CivicPriorityImperative[] }).imperatives;
  const filterCases = (voterData.framework_steps[1] as unknown as { filter_test_cases: SignalFilterTestCase[] }).filter_test_cases;
  const proposals = (voterData.framework_steps[2] as unknown as { proposals: OutcomeModelProposal[] }).proposals;
  const candidates = (voterData.framework_steps[3] as unknown as { candidates: CandidateProfile[] }).candidates;
  const propositions = (voterData.framework_steps[4] as unknown as { propositions: ReferendumProposition[] }).propositions;
  const tradeoffs = (voterData.framework_steps[5] as unknown as { tradeoff_dilemmas: TradeoffDilemma[] }).tradeoff_dilemmas;
  const dissonanceRules = (voterData.framework_steps[5] as unknown as { dissonance_rules: DissonanceRule[] }).dissonance_rules;

  // State Management
  const [activeStep, setActiveStep] = useState<number>(1);
  const [activePresetId, setActivePresetId] = useState<string>(initialPreset.preset_id);
  const [weights, setWeights] = useState<Record<string, number>>({ ...initialPreset.weights });
  const [tradeoffBalances, setTradeoffBalances] = useState<Record<string, number>>({ ...initialPreset.tradeoffs });
  const [filterMode, setFilterMode] = useState<'ALL' | 'VERIFIED_ONLY' | 'DISCREPANCY_ONLY'>('ALL');
  const [selectedProposalIndex, setSelectedProposalIndex] = useState<number>(0);
  const [selectedYear, setSelectedYear] = useState<1 | 2 | 3 | 4 | 5>(3);
  const [printPreviewMode, setPrintPreviewMode] = useState<boolean>(false);

  // Apply testing preset
  const applyPreset = (presetId: string) => {
    const found = presets.find((p) => p.preset_id === presetId);
    if (!found) return;
    setActivePresetId(presetId);
    setWeights({ ...found.weights });
    setTradeoffBalances({ ...found.tradeoffs });
  };

  // Step 1: Weight change
  const handleWeightChange = (code: string, newWeight: number) => {
    setWeights((prev) => ({
      ...prev,
      [code]: Math.max(1, Math.min(10, newWeight)),
    }));
  };

  // Step 6: Tradeoff change
  const handleTradeoffChange = (id: string, newBalance: number) => {
    setTradeoffBalances((prev) => ({
      ...prev,
      [id]: Math.max(-50, Math.min(50, newBalance)),
    }));
  };

  // Step 4: Candidate weighted alignment calculations
  const candidateAlignments: CandidateCalculatedAlignment[] = useMemo(() => {
    const totalWeight = Object.values(weights).reduce((acc, curr) => acc + curr, 0);
    if (totalWeight === 0) return [];

    return candidates.map((cand) => {
      let weightedSum = 0;
      let topDiff = -999;
      let topDivergentCode = '';
      let topMatch = -999;
      let topConvergentCode = '';

      cand.stances.forEach((st) => {
        const userWeight = weights[st.value_code] ?? 5;
        weightedSum += userWeight * st.stance_score;

        const convergence = st.stance_score * (userWeight / 10);
        if (convergence > topMatch) {
          topMatch = convergence;
          topConvergentCode = st.value_code;
        }

        const discrepancy = Math.abs(userWeight - st.stance_score);
        if (discrepancy > topDiff) {
          topDiff = discrepancy;
          topDivergentCode = st.value_code;
        }
      });

      const alignmentScore = Math.min(100, Math.max(0, (weightedSum / (totalWeight * 10)) * 100));
      const convImp = imperatives.find((imp) => imp.code === topConvergentCode);
      const divImp = imperatives.find((imp) => imp.code === topDivergentCode);

      return {
        candidate_id: cand.id,
        name: cand.name,
        title: cand.title,
        alignment_percentage: Math.round(alignmentScore * 10) / 10,
        top_convergent_value: convImp ? convImp.name : 'Constitutional Baseline',
        top_divergent_value: divImp ? divImp.name : 'Fiscal Policy',
        verification_rating: cand.verified_record_rating,
      };
    });
  }, [weights, candidates, imperatives]);

  // Step 6: Dissonance detection
  const detectedDissonances: DissonanceRule[] = useMemo(() => {
    const activeAlerts: DissonanceRule[] = [];
    const fiscalWeight = weights['FISCAL_DISCIPLINE'] ?? 5;
    const capitalBalance = tradeoffBalances['TRADEOFF-02'] ?? 0;
    if (fiscalWeight >= 8 && capitalBalance > 20) {
      const rule = dissonanceRules.find((r) => r.rule_id === 'DISSONANCE-01');
      if (rule) activeAlerts.push(rule);
    }

    const libertyWeight = weights['CONST_LIBERTY'] ?? 5;
    const securityBalance = tradeoffBalances['TRADEOFF-01'] ?? 0;
    if (libertyWeight >= 8 && securityBalance > 20) {
      const rule = dissonanceRules.find((r) => r.rule_id === 'DISSONANCE-02');
      if (rule) activeAlerts.push(rule);
    }

    return activeAlerts;
  }, [weights, tradeoffBalances, dissonanceRules]);

  // Deterministic Civic Coherence Index (CCI)
  const civicCoherenceIndex = useMemo(() => {
    let score = 92;
    // Penalty for each active dissonance
    score -= detectedDissonances.length * 14;
    // Check alignment spread
    const maxAlign = Math.max(...candidateAlignments.map((c) => c.alignment_percentage), 50);
    const minAlign = Math.min(...candidateAlignments.map((c) => c.alignment_percentage), 50);
    if (maxAlign - minAlign > 20) {
      score += 4;
    }
    return Math.min(100, Math.max(40, score));
  }, [detectedDissonances, candidateAlignments]);

  // Deterministic clarity card state
  const clarityCardState: CivicClarityCardState = useMemo(() => {
    const hashSeed = Object.values(weights).join('-') + ':' + Object.values(tradeoffBalances).join('-');
    let hash = 0;
    for (let charIndex = 0; charIndex < hashSeed.length; charIndex++) {
      hash = (hash << 5) - hash + hashSeed.charCodeAt(charIndex);
      hash |= 0;
    }
    const hexHash = Math.abs(hash).toString(16).padStart(8, '0').toUpperCase();

    return {
      version: '1.0.0',
      canonical_id: 'CANON-162',
      execution_timestamp: '2026-10-12T12:00:00Z',
      deterministic_hash: `CTJ-VOTER-${hexHash}`,
      civic_coherence_index: civicCoherenceIndex,
      priority_realization_ratio: Math.round(((civicCoherenceIndex + 85) / 2) * 10) / 10,
      voter_weights: { ...weights },
      candidate_alignments: candidateAlignments,
      referendum_verdicts: propositions.map((p) => ({
        id: p.id,
        title: p.title,
        vulnerability_score: p.vulnerability_score,
        verdict: p.verdict,
        verdict_label: p.verdict_label,
      })),
      tradeoff_balances: { ...tradeoffBalances },
      active_dissonances: detectedDissonances,
    };
  }, [weights, tradeoffBalances, civicCoherenceIndex, candidateAlignments, propositions, detectedDissonances]);

  // Filtered test cases for Step 2
  const visibleFilterCases = useMemo(() => {
    if (filterMode === 'VERIFIED_ONLY') {
      return filterCases.filter((c) => c.signal_reliability === 'VERIFIED_HIGH');
    }
    if (filterMode === 'DISCREPANCY_ONLY') {
      return filterCases.filter((c) => c.divergence_penalty > 40);
    }
    return filterCases;
  }, [filterCases, filterMode]);

  const activeProposal = proposals[selectedProposalIndex] || proposals[0];
  const activeProjection =
    activeProposal.projections.find((p) => p.year === selectedYear) || activeProposal.projections[2];

  const handlePrint = () => {
    window.print();
  };

  const handleExportJSON = () => {
    if (onClarityCardExport) {
      onClarityCardExport(clarityCardState);
    }
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(clarityCardState, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `${clarityCardState.deterministic_hash}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className={`space-y-8 text-slate-100 ${className}`}>
      {/* Testing Control Strip */}
      {testingMode && (
        <aside
          aria-label="Testing Mode Controller"
          className="bg-[#112240] border-2 border-[#D4AF37] rounded-xl p-4 sm:p-5 shadow-2xl flex flex-wrap items-center justify-between gap-4"
        >
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-1 rounded bg-[#00875A]/20 text-[#00875A] border border-[#00875A]/40 font-mono text-xs font-bold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#00875A] animate-pulse"></span>
              TESTING MODE ACTIVE
            </span>
            <span className="text-xs text-slate-400 font-mono">CANON-162</span>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-300 font-semibold">Load Test Profile:</span>
            {presets.map((preset) => (
              <button
                key={preset.preset_id}
                onClick={() => applyPreset(preset.preset_id)}
                className={`px-3 py-1 rounded text-xs font-bold transition border ${
                  activePresetId === preset.preset_id
                    ? 'bg-[#D4AF37] text-[#0A192F] border-[#D4AF37]'
                    : 'bg-[#0A192F] text-slate-300 border-slate-700 hover:border-[#D4AF37]'
                }`}
              >
                {preset.name.split('/')[0].trim()}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPrintPreviewMode(!printPreviewMode)}
              className="px-3 py-1 rounded bg-slate-800 text-xs text-slate-300 hover:text-white border border-slate-600 transition"
            >
              {printPreviewMode ? 'Exit Print Mode' : 'Print Preview Mode'}
            </button>
          </div>
        </aside>
      )}

      {/* 7-Step Navigation Bar */}
      <nav aria-label="7-Step Civic Framework Sequence" className="bg-[#112240] border border-slate-700/80 rounded-xl p-2 sm:p-3 overflow-x-auto">
        <ol className="flex items-center gap-1.5 min-w-[720px] justify-between">
          {[
            { step: 1, label: '1. Values Baseline' },
            { step: 2, label: '2. Signal vs Noise' },
            { step: 3, label: '3. Second-Order' },
            { step: 4, label: '4. Candidates' },
            { step: 5, label: '5. Referendums' },
            { step: 6, label: '6. Equilibrium' },
            { step: 7, label: '7. Clarity Card' },
          ].map((item) => {
            const isCurrent = activeStep === item.step;
            const isCompleted = activeStep > item.step;
            return (
              <li key={item.step} className="flex-1">
                <button
                  onClick={() => setActiveStep(item.step)}
                  className={`w-full py-2.5 px-2 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 border text-center ${
                    isCurrent
                      ? 'bg-[#D4AF37] text-[#0A192F] border-[#D4AF37] shadow-lg'
                      : isCompleted
                      ? 'bg-[#00875A]/20 text-[#00875A] border-[#00875A]/30 hover:bg-[#00875A]/30'
                      : 'bg-[#0A192F] text-slate-400 border-slate-800 hover:text-slate-200'
                  }`}
                >
                  <span>{item.label}</span>
                </button>
              </li>
            );
          })}
        </ol>
      </nav>

      {/* ========================================================= */}
      {/* STEP 1: CORE VALUES BASELINE */}
      {/* ========================================================= */}
      {activeStep === 1 && (
        <section aria-labelledby="step1-heading" className="space-y-6">
          <div className="border-b border-slate-800 pb-4 space-y-1">
            <span className="text-xs font-mono text-[#D4AF37] uppercase tracking-wider font-bold">
              Step 1 of 7: Core Values Baseline
            </span>
            <h2 id="step1-heading" className="text-2xl font-black text-white">
              Establish Prioritized Civic Imperatives
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Define baseline constitutional and governance principles on a 1-to-10 weight scale before evaluating
              candidate records. Priority weights determine candidate compatibility calculations in Step 4.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {imperatives.map((imp) => {
              const currentVal = weights[imp.code] ?? imp.default_weight;
              return (
                <div
                  key={imp.id}
                  className="bg-[#112240] border border-slate-700/80 rounded-xl p-5 space-y-3 hover:border-[#D4AF37]/60 transition"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-[#D4AF37] border border-[#D4AF37]/30">
                        {imp.category}
                      </span>
                      <h3 className="text-base font-bold text-white mt-1.5">{imp.name}</h3>
                    </div>
                    <span className="text-2xl font-black text-[#D4AF37] font-mono px-3 py-1 bg-[#0A192F] rounded-lg border border-slate-700">
                      {currentVal}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed">{imp.description}</p>

                  <div className="pt-2">
                    <label className="text-[11px] font-semibold text-slate-400 block mb-1.5">
                      Priority Weight (1 = Minimal, 10 = Non-Negotiable Apex Priority)
                    </label>
                    <input
                      type="range"
                      min={1}
                      max={10}
                      step={1}
                      value={currentVal}
                      onChange={(e) => handleWeightChange(imp.code, parseInt(e.target.value, 10))}
                      className="w-full accent-[#D4AF37] bg-slate-800 h-2 rounded-lg cursor-pointer"
                    />
                  </div>

                  <div className="bg-[#0A192F]/60 rounded-lg p-2.5 border border-slate-800/80">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                      Audit Benchmarks:
                    </span>
                    <ul className="text-[11px] text-slate-300 space-y-0.5 list-disc pl-4">
                      {imp.benchmarks.map((bm, idx) => (
                        <li key={idx}>{bm}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-end pt-4">
            <button
              onClick={() => setActiveStep(2)}
              className="px-6 py-2.5 rounded-lg bg-[#D4AF37] text-[#0A192F] font-bold text-xs uppercase tracking-wider hover:bg-[#e0bc45] transition shadow-md"
            >
              Advance to Step 2: Signal vs Noise Filter
            </button>
          </div>
        </section>
      )}

      {/* ========================================================= */}
      {/* STEP 2: SIGNAL VS NOISE FILTER */}
      {/* ========================================================= */}
      {activeStep === 2 && (
        <section aria-labelledby="step2-heading" className="space-y-6">
          <div className="border-b border-slate-800 pb-4 space-y-1">
            <span className="text-xs font-mono text-[#D4AF37] uppercase tracking-wider font-bold">
              Step 2 of 7: Signal vs Noise Filter
            </span>
            <h2 id="step2-heading" className="text-2xl font-black text-white">
              Distinguish Campaign Rhetoric from Verified Action
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Filter non-binding rhetoric and advertisements against verifiable legislative roll calls and statutory
              records. Divergence penalties identify discrepancies between campaign declarations and binding votes.
            </p>
          </div>

          {/* Filter Mode Switcher */}
          <div className="flex items-center gap-2 bg-[#112240] p-1.5 rounded-lg border border-slate-700/80 w-fit">
            <button
              onClick={() => setFilterMode('ALL')}
              className={`px-3 py-1.5 rounded text-xs font-bold transition ${
                filterMode === 'ALL' ? 'bg-[#D4AF37] text-[#0A192F]' : 'text-slate-300 hover:text-white'
              }`}
            >
              All Evidence Scenarios
            </button>
            <button
              onClick={() => setFilterMode('VERIFIED_ONLY')}
              className={`px-3 py-1.5 rounded text-xs font-bold transition ${
                filterMode === 'VERIFIED_ONLY' ? 'bg-[#D4AF37] text-[#0A192F]' : 'text-slate-300 hover:text-white'
              }`}
            >
              Verified High Fidelity
            </button>
            <button
              onClick={() => setFilterMode('DISCREPANCY_ONLY')}
              className={`px-3 py-1.5 rounded text-xs font-bold transition ${
                filterMode === 'DISCREPANCY_ONLY' ? 'bg-[#D4AF37] text-[#0A192F]' : 'text-slate-300 hover:text-white'
              }`}
            >
              Critical Discrepancies
            </button>
          </div>

          <div className="space-y-4">
            {visibleFilterCases.map((cs) => {
              const isMismatch = cs.divergence_penalty > 40;
              return (
                <div
                  key={cs.id}
                  className={`bg-[#112240] border rounded-xl p-5 space-y-4 transition ${
                    isMismatch ? 'border-amber-500/50 hover:border-amber-400' : 'border-slate-700 hover:border-[#00875A]'
                  }`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
                    <div>
                      <span className="text-[10px] font-mono text-[#D4AF37] uppercase font-bold tracking-wider">
                        {cs.domain}
                      </span>
                      <h3 className="text-base font-bold text-white">{cs.issue}</h3>
                    </div>
                    <span
                      className={`px-3 py-1 rounded text-xs font-mono font-bold uppercase tracking-wider border ${
                        cs.signal_reliability === 'VERIFIED_HIGH'
                          ? 'bg-[#00875A]/20 text-[#00875A] border-[#00875A]/40'
                          : 'bg-rose-900/30 text-rose-400 border-rose-700/50'
                      }`}
                    >
                      Reliability: {cs.signal_reliability.replace('_', ' ')}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Noise Column */}
                    <div className="bg-[#0A192F] p-4 rounded-lg border border-slate-800 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                          Campaign Rhetoric (Noise)
                        </span>
                        <span className="text-xs font-mono text-slate-400">Score: {cs.rhetoric_score}/100</span>
                      </div>
                      <p className="text-xs text-slate-300 italic">{cs.claimed_rhetoric}</p>
                    </div>

                    {/* Signal Column */}
                    <div className="bg-[#0A192F] p-4 rounded-lg border border-slate-800 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-[#D4AF37] uppercase tracking-wider">
                          Verified Roll Call / Record (Signal)
                        </span>
                        <span className="text-xs font-mono text-[#D4AF37]">Score: {cs.record_score}/100</span>
                      </div>
                      <p className="text-xs text-slate-200">{cs.verified_record}</p>
                      <span className="text-[10px] font-mono text-slate-400 block pt-1">
                        Source: {cs.evidence_citation}
                      </span>
                    </div>
                  </div>

                  {cs.divergence_penalty > 0 && (
                    <div className="flex items-center justify-between bg-amber-950/20 border border-amber-600/30 rounded-lg p-3 text-xs">
                      <span className="text-amber-300 font-semibold">
                        Evidentiary Divergence Penalty Applied:
                      </span>
                      <span className="font-mono font-black text-amber-400 text-sm">
                        -{cs.divergence_penalty} pts
                      </span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setActiveStep(1)}
              className="px-5 py-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-bold text-xs uppercase tracking-wider transition"
            >
              Previous Step
            </button>
            <button
              onClick={() => setActiveStep(3)}
              className="px-6 py-2.5 rounded-lg bg-[#D4AF37] text-[#0A192F] font-bold text-xs uppercase tracking-wider hover:bg-[#e0bc45] transition shadow-md"
            >
              Advance to Step 3: Second-Order Modeling
            </button>
          </div>
        </section>
      )}

      {/* ========================================================= */}
      {/* STEP 3: SECOND-ORDER OUTCOME MODELING */}
      {/* ========================================================= */}
      {activeStep === 3 && (
        <section aria-labelledby="step3-heading" className="space-y-6">
          <div className="border-b border-slate-800 pb-4 space-y-1">
            <span className="text-xs font-mono text-[#D4AF37] uppercase tracking-wider font-bold">
              Step 3 of 7: Second-Order Outcome Modeling
            </span>
            <h2 id="step3-heading" className="text-2xl font-black text-white">
              Project 5-Year Budgetary and Legal Horizons
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Examine legislative proposals beyond initial popular intent. Evaluate multi-year fiscal drag,
              compliance overhead, constitutional litigation exposure, and secondary market shifts.
            </p>
          </div>

          {/* Proposal Selectors */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {proposals.map((prop, idx) => (
              <button
                key={prop.id}
                onClick={() => setSelectedProposalIndex(idx)}
                className={`p-4 rounded-xl border text-left transition space-y-1 ${
                  selectedProposalIndex === idx
                    ? 'bg-[#112240] border-[#D4AF37] shadow-lg'
                    : 'bg-[#0A192F] border-slate-800 hover:border-slate-600'
                }`}
              >
                <span className="text-[10px] font-mono text-[#D4AF37] uppercase font-bold">Proposal Model {idx + 1}</span>
                <h3 className="text-sm font-bold text-white">{prop.title}</h3>
                <p className="text-xs text-slate-400">{prop.first_order_intent}</p>
              </button>
            ))}
          </div>

          {/* 5-Year Slider */}
          <div className="bg-[#112240] border border-slate-700/80 rounded-xl p-5 space-y-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <span className="text-xs font-bold text-slate-300">Timeline Projection Horizon:</span>
                <h3 className="text-lg font-black text-white">Year {selectedYear} of 5</h3>
              </div>
              <div className="flex items-center gap-1.5">
                {([1, 2, 3, 4, 5] as const).map((yr) => (
                  <button
                    key={yr}
                    onClick={() => setSelectedYear(yr)}
                    className={`w-9 h-9 rounded-lg font-mono font-bold text-xs transition border ${
                      selectedYear === yr
                        ? 'bg-[#D4AF37] text-[#0A192F] border-[#D4AF37]'
                        : 'bg-[#0A192F] text-slate-400 border-slate-700 hover:text-white'
                    }`}
                  >
                    Y{yr}
                  </button>
                ))}
              </div>
            </div>

            {/* Event Banner */}
            <div className="bg-[#0A192F] border border-slate-800 p-4 rounded-lg space-y-1">
              <span className="text-[10px] font-mono uppercase text-[#D4AF37] font-bold">
                Projected Year {selectedYear} Milestone:
              </span>
              <p className="text-xs text-slate-200 font-medium">{activeProjection.key_event}</p>
            </div>

            {/* Dimension Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="bg-[#0A192F] border border-slate-800 p-3.5 rounded-lg space-y-1">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Budget Drag Index</span>
                <div className="text-2xl font-black text-[#D4AF37] font-mono">
                  {activeProjection.budget_drag}
                  <span className="text-xs text-slate-400">/100</span>
                </div>
              </div>

              <div className="bg-[#0A192F] border border-slate-800 p-3.5 rounded-lg space-y-1">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Litigation Risk</span>
                <div
                  className={`text-xl font-black font-mono uppercase ${
                    activeProjection.litigation_risk === 'High'
                      ? 'text-rose-400'
                      : activeProjection.litigation_risk === 'Medium'
                      ? 'text-amber-400'
                      : 'text-[#00875A]'
                  }`}
                >
                  {activeProjection.litigation_risk}
                </div>
              </div>

              <div className="bg-[#0A192F] border border-slate-800 p-3.5 rounded-lg space-y-1">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Compliance Burden</span>
                <div className="text-2xl font-black text-slate-200 font-mono">
                  {activeProjection.compliance_burden}
                  <span className="text-xs text-slate-400">/100</span>
                </div>
              </div>

              <div className="bg-[#0A192F] border border-slate-800 p-3.5 rounded-lg space-y-1">
                <span className="text-[10px] font-bold text-slate-400 uppercase">Capital Distortion</span>
                <div className="text-2xl font-black text-slate-200 font-mono">
                  {activeProjection.capital_distortion}
                  <span className="text-xs text-slate-400">/100</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setActiveStep(2)}
              className="px-5 py-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-bold text-xs uppercase tracking-wider transition"
            >
              Previous Step
            </button>
            <button
              onClick={() => setActiveStep(4)}
              className="px-6 py-2.5 rounded-lg bg-[#D4AF37] text-[#0A192F] font-bold text-xs uppercase tracking-wider hover:bg-[#e0bc45] transition shadow-md"
            >
              Advance to Step 4: Candidate Comparator
            </button>
          </div>
        </section>
      )}

      {/* ========================================================= */}
      {/* STEP 4: CANDIDATE STANCE COMPARATOR */}
      {/* ========================================================= */}
      {activeStep === 4 && (
        <section aria-labelledby="step4-heading" className="space-y-6">
          <div className="border-b border-slate-800 pb-4 space-y-1">
            <span className="text-xs font-mono text-[#D4AF37] uppercase tracking-wider font-bold">
              Step 4 of 7: Candidate Stance Comparator
            </span>
            <h2 id="step4-heading" className="text-2xl font-black text-white">
              Calculate Weighted Alignment Scores Across Candidates
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Alignment percentages are derived by multiplying candidate verified stances against the prioritized
              weights established in Step 1. Personalities are decoupled from voting records.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {candidateAlignments.map((ca) => {
              const profile = candidates.find((c) => c.id === ca.candidate_id);
              return (
                <div
                  key={ca.candidate_id}
                  className="bg-[#112240] border-2 border-slate-700/80 hover:border-[#D4AF37] rounded-xl p-5 space-y-4 flex flex-col justify-between transition shadow-xl"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                        {ca.candidate_id}
                      </span>
                      <span
                        className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
                          ca.verification_rating === 'HIGH_VERIFIED'
                            ? 'bg-[#00875A]/20 text-[#00875A] border border-[#00875A]/40'
                            : 'bg-amber-900/30 text-amber-400 border border-amber-700/40'
                        }`}
                      >
                        {ca.verification_rating.replace('_', ' ')}
                      </span>
                    </div>

                    <div>
                      <h3 className="text-lg font-black text-white">{ca.name}</h3>
                      <p className="text-xs text-[#D4AF37] font-semibold">{ca.title}</p>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed">{profile?.profile_summary}</p>

                    <div className="bg-[#0A192F] p-4 rounded-lg border border-slate-800 text-center space-y-1">
                      <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider">
                        Weighted Alignment Score
                      </span>
                      <div className="text-4xl font-black text-[#D4AF37] font-mono">
                        {ca.alignment_percentage}%
                      </div>
                    </div>

                    <div className="space-y-2 text-xs">
                      <div className="flex items-center justify-between text-slate-300">
                        <span className="text-slate-400">Strongest Alignment:</span>
                        <strong className="text-white text-right max-w-[160px] truncate">
                          {ca.top_convergent_value}
                        </strong>
                      </div>
                      <div className="flex items-center justify-between text-slate-300">
                        <span className="text-slate-400">Primary Divergence:</span>
                        <strong className="text-amber-400 text-right max-w-[160px] truncate">
                          {ca.top_divergent_value}
                        </strong>
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-800 text-[11px] text-slate-400">
                    Calculated using {Object.keys(weights).length} weighted civic priorities from Step 1.
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setActiveStep(3)}
              className="px-5 py-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-bold text-xs uppercase tracking-wider transition"
            >
              Previous Step
            </button>
            <button
              onClick={() => setActiveStep(5)}
              className="px-6 py-2.5 rounded-lg bg-[#D4AF37] text-[#0A192F] font-bold text-xs uppercase tracking-wider hover:bg-[#e0bc45] transition shadow-md"
            >
              Advance to Step 5: Referendum Stress Test
            </button>
          </div>
        </section>
      )}

      {/* ========================================================= */}
      {/* STEP 5: BALLOT REFERENDUM STRESS TEST */}
      {/* ========================================================= */}
      {activeStep === 5 && (
        <section aria-labelledby="step5-heading" className="space-y-6">
          <div className="border-b border-slate-800 pb-4 space-y-1">
            <span className="text-xs font-mono text-[#D4AF37] uppercase tracking-wider font-bold">
              Step 5 of 7: Ballot Referendum Stress Test
            </span>
            <h2 id="step5-heading" className="text-2xl font-black text-white">
              Test Propositions Against the 5-Pillar Vulnerability Matrix
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Examine citizen initiatives and bond measures through five structural pillars: Constitutional Authority,
              Dedicated Revenue, Secondary Disruption, Rulemaking Discretion, and Mandatory Audit / Sunsets.
            </p>
          </div>

          <div className="space-y-6">
            {propositions.map((prop) => (
              <div
                key={prop.id}
                className="bg-[#112240] border border-slate-700/80 rounded-xl p-5 sm:p-6 space-y-4 hover:border-slate-600 transition"
              >
                <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
                  <div>
                    <h3 className="text-base font-black text-white">{prop.title}</h3>
                    <p className="text-xs text-slate-300 mt-1 max-w-2xl">{prop.ballot_summary}</p>
                  </div>

                  <div className="text-right">
                    <span
                      className={`px-3 py-1 rounded text-xs font-mono font-bold uppercase tracking-wider border block ${
                        prop.verdict === 'VERIFIED_PASS'
                          ? 'bg-[#00875A]/20 text-[#00875A] border-[#00875A]/40'
                          : prop.verdict === 'CONDITIONAL_WARN'
                          ? 'bg-amber-900/30 text-amber-400 border-amber-700/50'
                          : 'bg-rose-900/30 text-rose-400 border-rose-700/50'
                      }`}
                    >
                      Verdict: {prop.verdict_label}
                    </span>
                    <span className="text-[11px] font-mono text-slate-400 mt-1 block">
                      Vulnerability Score: {prop.vulnerability_score}/100
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pt-2">
                  {prop.pillar_evaluations.map((pe) => {
                    return (
                      <div
                        key={pe.pillar_code}
                        className="bg-[#0A192F] p-3 rounded-lg border border-slate-800 space-y-1.5"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">
                            {pe.pillar_code}
                          </span>
                          <span
                            className={`text-[10px] font-mono font-black px-1.5 py-0.2 rounded ${
                              pe.status === 'PASS'
                                ? 'bg-[#00875A]/30 text-[#00875A]'
                                : pe.status === 'WARN'
                                ? 'bg-amber-900/30 text-amber-400'
                                : 'bg-rose-900/30 text-rose-400'
                            }`}
                          >
                            {pe.status}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-300 leading-tight">{pe.notes}</p>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setActiveStep(4)}
              className="px-5 py-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-bold text-xs uppercase tracking-wider transition"
            >
              Previous Step
            </button>
            <button
              onClick={() => setActiveStep(6)}
              className="px-6 py-2.5 rounded-lg bg-[#D4AF37] text-[#0A192F] font-bold text-xs uppercase tracking-wider hover:bg-[#e0bc45] transition shadow-md"
            >
              Advance to Step 6: Trade-off Equilibrium
            </button>
          </div>
        </section>
      )}

      {/* ========================================================= */}
      {/* STEP 6: TRADE-OFF EQUILIBRIUM CALCULATOR */}
      {/* ========================================================= */}
      {activeStep === 6 && (
        <section aria-labelledby="step6-heading" className="space-y-6">
          <div className="border-b border-slate-800 pb-4 space-y-1">
            <span className="text-xs font-mono text-[#D4AF37] uppercase tracking-wider font-bold">
              Step 6 of 7: Trade-off Equilibrium Calculator
            </span>
            <h2 id="step6-heading" className="text-2xl font-black text-white">
              Map Civic Equilibrium and Audit Cognitive Friction
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Every political policy requires structural trade-offs. Use dual-axis sliders to locate personal
              equilibrium points. The engine flags cognitive dissonance when chosen positions conflict mathematically.
            </p>
          </div>

          {/* Dissonance Alerts */}
          {detectedDissonances.length > 0 && (
            <div className="space-y-3">
              {detectedDissonances.map((alert) => (
                <div
                  key={alert.rule_id}
                  className="bg-amber-950/30 border-2 border-amber-500 rounded-xl p-4 space-y-1.5 animate-in fade-in"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-amber-400 font-black text-sm">⚠ COGNITIVE DISSONANCE DETECTED</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-900/40 text-amber-300 border border-amber-600/40">
                      {alert.severity}
                    </span>
                  </div>
                  <strong className="text-white text-sm block">{alert.alert_title}</strong>
                  <p className="text-xs text-amber-200/90 leading-relaxed">{alert.alert_message}</p>
                </div>
              ))}
            </div>
          )}

          <div className="space-y-5">
            {tradeoffs.map((td) => {
              const currentBalance = tradeoffBalances[td.id] ?? td.default_balance;
              return (
                <div key={td.id} className="bg-[#112240] border border-slate-700/80 rounded-xl p-5 space-y-4">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h3 className="text-base font-bold text-white">{td.title}</h3>
                    <span className="text-xs font-mono text-[#D4AF37] px-2.5 py-1 bg-[#0A192F] rounded border border-slate-700">
                      Balance Point: {currentBalance > 0 ? `+${currentBalance}` : currentBalance}
                    </span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-xs font-bold">
                      <span className="text-emerald-400 max-w-[45%]">{td.axis_left}</span>
                      <span className="text-cyan-400 max-w-[45%] text-right">{td.axis_right}</span>
                    </div>

                    <input
                      type="range"
                      min={-50}
                      max={50}
                      step={5}
                      value={currentBalance}
                      onChange={(e) => handleTradeoffChange(td.id, parseInt(e.target.value, 10))}
                      className="w-full accent-[#D4AF37] bg-slate-800 h-2.5 rounded-lg cursor-pointer"
                    />

                    <div className="grid grid-cols-2 gap-4 text-[11px] text-slate-400 pt-1">
                      <div>{td.description_left}</div>
                      <div className="text-right">{td.description_right}</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setActiveStep(5)}
              className="px-5 py-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-bold text-xs uppercase tracking-wider transition"
            >
              Previous Step
            </button>
            <button
              onClick={() => setActiveStep(7)}
              className="px-6 py-2.5 rounded-lg bg-[#D4AF37] text-[#0A192F] font-bold text-xs uppercase tracking-wider hover:bg-[#e0bc45] transition shadow-md"
            >
              Advance to Step 7: Deterministic Civic Clarity Card
            </button>
          </div>
        </section>
      )}

      {/* ========================================================= */}
      {/* STEP 7: DETERMINISTIC CIVIC CLARITY CARD */}
      {/* ========================================================= */}
      {activeStep === 7 && (
        <section aria-labelledby="step7-heading" className="space-y-6">
          <div className="border-b border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <span className="text-xs font-mono text-[#D4AF37] uppercase tracking-wider font-bold">
                Step 7 of 7: Deterministic Civic Clarity Card
              </span>
              <h2 id="step7-heading" className="text-2xl font-black text-white">
                Deterministic Nonpartisan Decision Digest
              </h2>
              <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
                The final deliverable synthesizes all seven framework steps into an auditable, print-optimized ballot
                cheat-sheet.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={handlePrint}
                className="px-4 py-2.5 rounded-lg bg-[#00875A] hover:bg-[#00704a] text-white font-bold text-xs uppercase tracking-wider transition shadow flex items-center gap-2"
              >
                <span>🖨️ Print Clarity Card</span>
              </button>
              <button
                onClick={handleExportJSON}
                className="px-4 py-2.5 rounded-lg bg-[#D4AF37] hover:bg-[#e0bc45] text-[#0A192F] font-bold text-xs uppercase tracking-wider transition shadow flex items-center gap-2"
              >
                <span>💾 Export JSON</span>
              </button>
            </div>
          </div>

          {/* Clarity Card Printable Canvas */}
          <article
            id="civicClarityCardPrintable"
            className="bg-[#0A192F] border-4 border-[#D4AF37] rounded-2xl p-6 sm:p-8 space-y-6 shadow-2xl relative"
          >
            {/* Top Brand Banner */}
            <div className="border-b-2 border-[#D4AF37]/50 pb-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <span className="text-[10px] font-black tracking-widest text-[#D4AF37] uppercase block">
                  SONLY CONSULTING - CRITICAL THINKER'S JOURNEY: VOTER EDITION
                </span>
                <h3 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
                  OFFICIAL CIVIC CLARITY CARD
                </h3>
                <span className="text-xs text-slate-400">
                  Nonpartisan Audit Standard | DCSE Governance CANON-162
                </span>
              </div>

              <div className="bg-[#112240] border border-slate-700 p-3 rounded-xl text-right">
                <span className="text-[10px] font-mono text-slate-400 uppercase block">Deterministic Hash</span>
                <span className="font-mono text-sm font-black text-[#D4AF37]">
                  {clarityCardState.deterministic_hash}
                </span>
                <span className="text-[10px] text-slate-400 block mt-0.5">
                  Executed: {clarityCardState.execution_timestamp.split('T')[0]}
                </span>
              </div>
            </div>

            {/* Score Strip */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-[#112240] border border-slate-700/80 rounded-xl p-4 text-center space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Civic Coherence Index (CCI)
                </span>
                <div className="text-3xl font-black text-[#D4AF37] font-mono">
                  {clarityCardState.civic_coherence_index}
                  <span className="text-xs text-slate-400">/100</span>
                </div>
                <span className="text-[10px] text-[#00875A] font-semibold block">High Internal Consistency</span>
              </div>

              <div className="bg-[#112240] border border-slate-700/80 rounded-xl p-4 text-center space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Active Cognitive Dissonance
                </span>
                <div className="text-3xl font-black font-mono">
                  {clarityCardState.active_dissonances.length === 0 ? (
                    <span className="text-[#00875A]">0 Flags</span>
                  ) : (
                    <span className="text-amber-400">{clarityCardState.active_dissonances.length} Active</span>
                  )}
                </div>
                <span className="text-[10px] text-slate-400 block">Friction Audit Complete</span>
              </div>

              <div className="bg-[#112240] border border-slate-700/80 rounded-xl p-4 text-center space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Priority Realization Ratio
                </span>
                <div className="text-3xl font-black text-slate-200 font-mono">
                  {clarityCardState.priority_realization_ratio}%
                </div>
                <span className="text-[10px] text-slate-400 block">Mathematical Feasibility</span>
              </div>
            </div>

            {/* Core Values Summary */}
            <div className="space-y-2">
              <span className="text-xs font-mono uppercase text-[#D4AF37] font-bold tracking-wider">
                1. Prioritized Governance Hierarchy (Top Imperatives)
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {imperatives
                  .slice()
                  .sort((a, b) => (weights[b.code] ?? 0) - (weights[a.code] ?? 0))
                  .slice(0, 4)
                  .map((imp, idx) => (
                    <div
                      key={imp.code}
                      className="bg-[#112240] p-2.5 rounded-lg border border-slate-800 text-xs flex items-center justify-between"
                    >
                      <span className="text-slate-300 font-medium truncate pr-1">
                        #{idx + 1} {imp.name.split('&')[0].trim()}
                      </span>
                      <span className="font-mono font-bold text-[#D4AF37]">{weights[imp.code]}</span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Candidate Alignment Summary */}
            <div className="space-y-2">
              <span className="text-xs font-mono uppercase text-[#D4AF37] font-bold tracking-wider">
                2. Audited Candidate Alignment Rankings
              </span>
              <div className="space-y-2">
                {candidateAlignments
                  .slice()
                  .sort((a, b) => b.alignment_percentage - a.alignment_percentage)
                  .map((ca, idx) => (
                    <div
                      key={ca.candidate_id}
                      className="bg-[#112240] border border-slate-800 p-3 rounded-lg flex flex-wrap items-center justify-between gap-2 text-xs"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-6 h-6 rounded-full bg-[#D4AF37] text-[#0A192F] font-black font-mono flex items-center justify-center text-xs">
                          {idx + 1}
                        </span>
                        <div>
                          <strong className="text-white block">{ca.name}</strong>
                          <span className="text-slate-400 text-[11px]">{ca.title}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <span className="text-slate-400 text-[10px] block">Key Alignment</span>
                          <span className="text-white font-semibold">{ca.top_convergent_value}</span>
                        </div>
                        <div className="text-right pl-3 border-l border-slate-700 min-w-[70px]">
                          <span className="text-[10px] text-slate-400 block">Match</span>
                          <span className="text-base font-mono font-black text-[#D4AF37]">
                            {ca.alignment_percentage}%
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            {/* Referendum Verdicts Summary */}
            <div className="space-y-2">
              <span className="text-xs font-mono uppercase text-[#D4AF37] font-bold tracking-wider">
                3. Ballot Proposal Structural Integrity Verdicts
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {clarityCardState.referendum_verdicts.map((rv) => (
                  <div
                    key={rv.id}
                    className="bg-[#112240] border border-slate-800 p-3 rounded-lg text-xs space-y-1.5"
                  >
                    <span className="text-[10px] font-mono text-slate-400 uppercase">{rv.id}</span>
                    <strong className="text-white text-[11px] block line-clamp-1">{rv.title.split(':')[1] || rv.title}</strong>
                    <div className="flex items-center justify-between pt-1">
                      <span
                        className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                          rv.verdict === 'VERIFIED_PASS'
                            ? 'bg-[#00875A]/30 text-[#00875A]'
                            : rv.verdict === 'CONDITIONAL_WARN'
                            ? 'bg-amber-900/30 text-amber-400'
                            : 'bg-rose-900/30 text-rose-400'
                        }`}
                      >
                        {rv.verdict.replace('_', ' ')}
                      </span>
                      <span className="text-[10px] font-mono text-slate-400">Risk: {rv.vulnerability_score}/100</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Verification Footer */}
            <div className="border-t border-slate-800 pt-4 flex flex-wrap items-center justify-between gap-3 text-[11px] text-slate-400 font-mono">
              <span>Sonly Consulting | Critical Thinker's Journey | CANON-162</span>
              <span>Deterministic Civic Clarity Standard - Nonpartisan Audit Trail</span>
            </div>
          </article>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setActiveStep(6)}
              className="px-5 py-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-bold text-xs uppercase tracking-wider transition"
            >
              Previous Step
            </button>
            <button
              onClick={() => setActiveStep(1)}
              className="px-6 py-2.5 rounded-lg bg-[#D4AF37] text-[#0A192F] font-bold text-xs uppercase tracking-wider hover:bg-[#e0bc45] transition shadow-md"
            >
              Restart Civic Clarity Sequence
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
