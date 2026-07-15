# Voice State Machine Findings
**Audit ID:** Code-Review-OS-Auth-Sources-20260716
**Entity:** SC
**Classification:** Implementation Gap Analysis

---

## Current Implementation

**Location:** `index.js` lines 1305-1321

The voice implementation uses the Web Speech API (`SpeechRecognition`) with a simple toggle pattern:

```
States: OFF ←→ ON (recording)
Transitions: toggleVoice() flips voiceActive boolean
```

### Current Code Behavior

1. User clicks "Voice" button
2. `voiceActive` flips to `true`
3. `SpeechRecognition` instance created with `continuous: true`, `interimResults: false`
4. On result: transcript placed in chat input, `sendMessage()` called immediately
5. On error: voice deactivated, error message shown
6. User clicks "Stop": `recognition.stop()` called

---

## Identified Defects

### Defect 1: Premature Submission

**Severity:** HIGH

When `onresult` fires, the transcript is immediately placed in the input and `sendMessage()` is called:

```javascript
recognition.onresult = e => {
  const t = e.results[e.results.length-1][0].transcript.trim();
  if (t) {
    document.getElementById('chatInput').value = t;
    sendMessage();
  }
};
```

**Problem:** With `continuous: true`, the recognizer fires `onresult` for each recognized phrase. The user cannot review or edit the transcript before it is submitted. Partial phrases, misrecognitions, and ambient noise all trigger immediate message sends.

**Expected Behavior:** Transcript should populate the input field. User should have the option to review, edit, or confirm before sending.

### Defect 2: Missing Speech Detection States

**Severity:** MEDIUM

The implementation has only two states (OFF/ON). A proper voice state machine requires intermediate states for:

- **LISTENING:** Microphone active, waiting for speech
- **DETECTING:** Speech detected, capturing audio
- **PROCESSING:** Recognition engine processing captured audio
- **RESULT:** Transcript ready for review
- **ERROR:** Recoverable error state

**Current gap:** No `onspeechstart`, `onspeechend`, `onaudiostart`, `onaudioend`, or `onnomatch` handlers. The UI cannot distinguish between "listening for speech" and "processing speech."

### Defect 3: No Silence Detection / Auto-Stop

**Severity:** LOW

With `continuous: true` and no silence timeout, the recognizer runs indefinitely until the user manually stops it. No auto-pause after extended silence or between utterances.

### Defect 4: Single Recognition Instance Leak

**Severity:** LOW

A new `SpeechRecognition` instance is created each time voice is toggled on, but the previous instance is only stopped via `recognition.stop()`. If `stop()` fails or is delayed, multiple instances could be active simultaneously.

### Defect 5: No Visual Feedback for Recognition State

**Severity:** LOW

The voice button toggles between "Voice" and "Stop" text with a red recording indicator. There is no visual feedback for:
- Whether speech is being detected
- Confidence level of recognition
- Processing state
- Interim results (disabled by `interimResults: false`)

---

## Required State Machine

```
                    ┌─────────┐
         ┌────────▶ │  IDLE   │ ◀─────────────┐
         │          └────┬────┘               │
         │               │ toggleVoice()      │ toggleVoice() / error
         │               ▼                    │
         │          ┌─────────┐               │
         │          │LISTENING│───────────────▶│
         │          └────┬────┘ (no speech     │
         │               │      timeout)       │
         │               │ onspeechstart       │
         │               ▼                    │
         │          ┌──────────┐              │
         │          │DETECTING │              │
         │          └────┬─────┘              │
         │               │ onspeechend        │
         │               ▼                    │
         │          ┌───────────┐             │
         │          │PROCESSING │             │
         │          └────┬──────┘             │
         │               │ onresult           │
         │               ▼                    │
         │          ┌──────────┐              │
         └──────────│ RESULT   │──────────────┘
           (send    └──────────┘  (edit/discard)
            after     │
            confirm)  │ user confirms
                      ▼
                   sendMessage()
```

---

## Remediation Requirements

| Priority | Action | Effort |
|----------|--------|--------|
| P0 | Remove auto-send on result; populate input only and let user confirm | Small |
| P1 | Add `onspeechstart`/`onspeechend` handlers with visual state indicators | Medium |
| P1 | Show interim results (`interimResults: true`) for real-time feedback | Small |
| P2 | Add silence timeout to auto-stop after no speech detected | Small |
| P2 | Prevent multiple recognition instances | Small |
| P3 | Add confidence threshold filtering | Small |
| P3 | Add voice wave animation tied to actual audio levels | Medium |
