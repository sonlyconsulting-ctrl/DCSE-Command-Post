/**
 * Strict TypeScript types for CTJ: Voter Edition (CANON-162)
 * Governed by DCSE Master Profile v7.3:
 * Third-person solo-brand, nonpartisan civic clarity framework.
 */

export type EvidentiaryReliability = 'POOR' | 'CRITICAL_MISMATCH' | 'VERIFIED_HIGH' | 'MEDIUM_MIXED';
export type PillarVerdictStatus = 'PASS' | 'WARN' | 'FAIL';
export type ProposalVerdict = 'VERIFIED_PASS' | 'CONDITIONAL_WARN' | 'CRITICAL_FAIL';
export type DissonanceSeverity = 'CRITICAL_DISSONANCE' | 'EVIDENTIARY_FRICTION' | 'BALANCED';

export interface CivicPriorityImperative {
  id: string;
  code: string;
  name: string;
  category: 'Governance' | 'Economy' | 'Security' | 'Legal' | 'Integrity' | 'Infrastructure';
  description: string;
  default_weight: number;
  benchmarks: string[];
}

export interface SignalFilterCategory {
  type: 'SIGNAL' | 'NOISE';
  tier: string;
  weight_multiplier: number;
  sources: string[];
}

export interface SignalFilterTestCase {
  id: string;
  domain: string;
  issue: string;
  claimed_rhetoric: string;
  verified_record: string;
  rhetoric_score: number;
  record_score: number;
  divergence_penalty: number;
  signal_reliability: EvidentiaryReliability;
  evidence_citation: string;
}

export interface OutcomeModelProjection {
  year: 1 | 2 | 3 | 4 | 5;
  budget_drag: number;
  litigation_risk: 'Low' | 'Medium' | 'High';
  compliance_burden: number;
  capital_distortion: number;
  key_event: string;
}

export interface OutcomeModelDimension {
  dimension: 'BUDGET_IMPACT' | 'LEGAL_EXPOSURE' | 'COMPLIANCE_BURDEN' | 'CAPITAL_DISTORTION';
  label: string;
  unit: string;
  description: string;
}

export interface OutcomeModelProposal {
  id: string;
  title: string;
  first_order_intent: string;
  projections: OutcomeModelProjection[];
}

export interface CandidateStance {
  value_code: string;
  stance_score: number;
  rationale: string;
  verification_source: string;
}

export interface CandidateProfile {
  id: string;
  name: string;
  title: string;
  profile_summary: string;
  verified_record_rating: 'HIGH_VERIFIED' | 'MEDIUM_MIXED' | 'LOW_UNVERIFIED';
  stances: CandidateStance[];
}

export interface CandidateCalculatedAlignment {
  candidate_id: string;
  name: string;
  title: string;
  alignment_percentage: number;
  top_convergent_value: string;
  top_divergent_value: string;
  verification_rating: string;
}

export interface ReferendumStressPillar {
  code: string;
  name: string;
  fail_condition: string;
}

export interface ReferendumPillarEval {
  pillar_code: string;
  status: PillarVerdictStatus;
  notes: string;
}

export interface ReferendumProposition {
  id: string;
  title: string;
  ballot_summary: string;
  pillar_evaluations: ReferendumPillarEval[];
  vulnerability_score: number;
  verdict: ProposalVerdict;
  verdict_label: string;
}

export interface TradeoffDilemma {
  id: string;
  title: string;
  axis_left: string;
  axis_right: string;
  description_left: string;
  description_right: string;
  default_balance: number; // -50 to +50
}

export interface DissonanceRule {
  rule_id: string;
  trigger_condition: string;
  severity: DissonanceSeverity;
  alert_title: string;
  alert_message: string;
}

export interface TestingPreset {
  preset_id: string;
  name: string;
  description: string;
  weights: Record<string, number>;
  tradeoffs: Record<string, number>;
}

export interface CivicClarityCardState {
  version: string;
  canonical_id: string;
  execution_timestamp: string;
  deterministic_hash: string;
  civic_coherence_index: number;
  priority_realization_ratio: number;
  voter_weights: Record<string, number>;
  candidate_alignments: CandidateCalculatedAlignment[];
  referendum_verdicts: {
    id: string;
    title: string;
    vulnerability_score: number;
    verdict: ProposalVerdict;
    verdict_label: string;
  }[];
  tradeoff_balances: Record<string, number>;
  active_dissonances: DissonanceRule[];
}

export interface VoterModuleState {
  activeStep: number;
  isTestingMode: boolean;
  activePresetId: string | null;
  weights: Record<string, number>;
  tradeoffs: Record<string, number>;
  selectedProposalId: string;
  selectedProjectionYear: number;
  filterMode: 'ALL' | 'VERIFIED_ONLY' | 'DISCREPANCY_ONLY';
  printPreviewMode: boolean;
}

export interface VoterModuleProps {
  initialPresetId?: string;
  testingMode?: boolean;
  onClarityCardExport?: (card: CivicClarityCardState) => void;
  className?: string;
}
