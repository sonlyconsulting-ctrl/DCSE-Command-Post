# DCSE Consolidated Acceptance Checklist

**Document ID:** DCSE_CONSOLIDATED_ACCEPTANCE_CHECKLIST_TEMPLATE
**Version:** 1.0
**Purpose:** Pre-implementation and post-implementation validation matrix enforcing semantic consistency and DART methodology across all agents.

## Section 1: Pre-Implementation Baseline
*   [ ] Task scope and existing authorization clearly established via Shared Action Contract.
*   [ ] Target repository, branch, and working directory verified.
*   [ ] Pre-existing unrelated modifications on the branch identified for preservation.

## Section 2: Authority and Lifecycle State
*   [ ] Document headers and introductory prose precisely match the declared lifecycle state (e.g., CANDIDATE).
*   [ ] No premature claims of "canonical," "mandatory," or "production" status for candidate artifacts.
*   [ ] Artifact state is separated from action authority (i.e., a commit does not confer publication approval).

## Section 3: Semantic Content Validation (Whole-Artifact)
*   [ ] **Zero Absolute Outcome Promises:** Absolute outcome claims must be replaced with concrete mechanisms (such as requires targeted state checkpoints).
*   [ ] **Prohibited Punctuation:** Zero em dashes (Unicode U+2014) or en dashes (Unicode U+2013) anywhere in the document. Use standard periods, colons, or parentheses.
*   [ ] **Voice Calibration:** Third-person solo-brand posture strictly maintained; no performative buzzwords (synergy, delve, unlock potential).

## Section 4: DART Routing and Legal Frameworks
*   [ ] Command Post / SC Route explicitly defines: Discovery, Assess, Refine, Transfer.
*   [ ] Protected PS Route explicitly defines: Discovery, Attack, Rebuttal, Trial.
*   [ ] Specialized legal frameworks (such as McDonnell Douglas) are restricted entirely to the Protected PS adapter and do not bleed into universal documentation.

## Section 5: Provenance and Evidence
*   [ ] Timeline assertions include specific reference links or system IDs.
*   [ ] If direct files are inaccessible in the current environment, assertions are explicitly qualified as requiring external validation.

## Section 6: Commit and Readback
*   [ ] Changes strictly bounded to the authorized task scope.
*   [ ] Vercel suppression applied via [skip ci] or [skip vercel] for non-deployment commits.
*   [ ] Push successfully verified on the remote repository.
*   [ ] Final action log/receipt generated in the designated shared repository location.
