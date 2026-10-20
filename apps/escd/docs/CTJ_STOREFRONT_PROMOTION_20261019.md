# CTJ approved storefront: ESCD synchronization

Task SC-CTJ-PROMOTION-20261019-01. DCS authorized the approved storefront deployment and subsequent ESCD update.

Source artifact: SC-CTJ PR #22, commit ec50ba0569546b1acc22ebc4eaf97698f8c7c9d7, deployment/approved-ctj/ctj/index.html. SHA-256 4f2eedc1bd206712ac8e589d34a8e71bff02dc3518893e13f897c81550c41a1a. Target https://sonlyconsulting.com/ctj/.

Current status: source synchronized as pending; deployment is not verified. No live URL/version has been relabeled as the approved release.

After the actual Netlify deployment is verified:
1. Update only the CTJ entry in both catalog copies. Set actions.live_url and actions.external_preview to the verified branded route, store the actual deployment ID/artifact hash, and close pending_release with deployed/readback status.
2. Reconcile the CTJ card description and capabilities to the approved family; do not present the separate Voter Edition as the total CTJ family. Do not alter unrelated products or teaching.
3. Append or update the bounded canonical promotion record with the actual receipt. Retain prior evidence and distinguish storefront promotion from open commerce work in issue #21.
4. Publish the catalog/registry changes through the existing ESCD production deployment process, preserving its current verified chat repair and other production files. Do not rebuild production from an older or unverified snapshot.
5. Verify the production ESCD Products response and UI return the actual new URL/version, and the canonical Knowledge entry includes the artifact identity. A Git commit alone is not live ingestion.

The current ESCD source reads its products catalog and canonical registry from packaged files, so there is no verified automatic GitHub-to-live-catalog refresh. The asset path in the inspected source uses public schema; do not use it for this operation. Follow operative D15 dcse_cp isolation and do not create a substitute registration table.
