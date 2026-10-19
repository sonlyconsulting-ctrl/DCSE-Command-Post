# ESCD production release authorization and media replacement

Task: `SC-ESCD-CHAT-PERSISTENCE-20261019-01`  
Lane: SC / ESCD  
Handoff: `HO-SC-ESCD-CHAT-20261019-01`  
Activity: production release of PR #196 plus requested ambiance soundtrack replacement.

## Authority and acceptance

On 2026-10-19, DCS explicitly instructed: “TESTED, CONFIRM AND DEPLOY PRODUCTION AND UPDATE GITHUB WITH ACTIVITY.” DCS also instructed replacement of the ambiance music with the attached file. This is direct production authorization for the scoped repair and media replacement, superseding the earlier production HOLD. It does not authorize any schema, RLS, or unrelated application changes.

DCS reports successful preview testing. The attached screenshot shows `sc-escd-aqipx959q-sonlyconsulting-ctrls-projects.vercel.app/escd/app` and Saved Chats listing `SAVE` at 2026-10-19 2:58:27 PM local. The screenshot establishes listing; restore/update acceptance remains DCS-reported. No independent AG review is claimed.

Tested repair commit: `f7288f3f09ea15435bc7bdc8ea0a25d125451c96`. The new commit adds only this authorization record and the ambiance files.

## Ambiance replacement

Source supplied by DCS: `The_Quiet_Study.mp4`.

- Source SHA-256: `d91478f7a9520fb7ab3a1c33d2997f380163fbb7653e93f8cbf06a1b6d9b5516`.
- Audio extracted from stream 0:a:0 with FFmpeg; video excluded.
- Output: MP3, stereo, 44.1 kHz, 128 kbps, 156.682449 seconds, 2,507,570 bytes.
- Output SHA-256: `3ee2714f766ea5d10f0340d12cf2175b5abbb8d289388fb020120ab5451e204a`.
- Git blob: `0fda7e1c20d777c82a16c009485046eda3941182`.

Identical audio replaces these existing files so both static-file resolution and rewrite fallbacks serve the requested soundtrack:

- `ambiance.mp3`
- `audio/scripture_ambiance.mp3`
- `apps/escd/web/ambiance.mp3`
- `apps/escd/web/audio/scripture_ambiance.mp3`

Existing manual play/pause control, loop behavior, and volume remain unchanged. The source video and screenshot are not published as application assets. Other entity-specific ambiance files are untouched.

## Pre-release verification

- Full ESCD regression suite: **108 passed** on the combined worktree.
- FFmpeg full audio decode: pass.
- Git whitespace check: pass.
- Source and audio blob checksums recorded above.
- Prior production alias reverified before release: `sc-escd.vercel.app` → `dpl_4octnuCf1RnfVoTzw3hBnbELeGLS`, source `fe308859cb694a1ea44eccfcdc81c9b3cbdd3fd0`.
- No database migration, policy, grant, user, or conversation deletion performed.

## Release and closeout

Merge through PR #196 with its exact reviewed head. Deploy only the `sc-escd` Vercel project (`prj_TfGqYXFwkLfaZth644kXLn48CMVR`) for team `team_g4aI8rT2IsL2OCR3pYA65141`. Verify READY and production-alias assignment at the resulting commit. Record final deployment ID, commit SHA, CI outcome, HTTP/media readback, and verification limits in PR #196 activity comments after execution. This pre-release record does not assert deployment success.

The existing operator-wide RLS SELECT behavior is unchanged. API owner filtering is tested; no strict direct-PostgREST two-operator isolation certification is claimed.

Rollback, if needed and authorized, restores the recorded prior production deployment and verifies alias readback. No database rollback is required; preserve all saved records. A source revert must use a new controlled branch and PR, including the audio replacements. Older runtime code cannot fully use version-2 snapshots; retaining data does not make the old reader compatible.
