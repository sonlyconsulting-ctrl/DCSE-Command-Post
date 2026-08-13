#!/usr/bin/env bash
set -euo pipefail

# Containment rule for Git-triggered Vercel deployments from the shared
# DCSE-Command-Post repository. Five Vercel projects are currently connected
# to the repository root, so ordinary governance/Tribunal commits cause
# unrelated deployments. Until each project is mapped to its proper source
# root, freeze Git-triggered builds for those known project IDs.
#
# Manual/non-Git deployments are allowed to proceed.

if [[ -z "${VERCEL_GIT_COMMIT_SHA:-}" ]]; then
  echo "No Git commit context detected. Proceeding with build."
  exit 1
fi

case "${VERCEL_PROJECT_ID:-}" in
  prj_xVHcFD74DWyVD0QtizARSGIRSP2T|\
  prj_WJLnWl2RrdUcELBZHwPI6Qw8ZIZ9|\
  prj_3t9SKxOUuW0peitSq97OHWDWCQy9|\
  prj_z6GCdh8IzcPnQ4PwgFmZ8V5YhNKM|\
  prj_a9pbcrfvQczbmH2Cr1S2Q08p2975)
    echo "Skipping Git-triggered deployment for ${VERCEL_PROJECT_ID}; source-root reconciliation is pending."
    exit 0
    ;;
  *)
    echo "Project ${VERCEL_PROJECT_ID:-unknown} is not in the containment set. Proceeding with build."
    exit 1
    ;;
esac
