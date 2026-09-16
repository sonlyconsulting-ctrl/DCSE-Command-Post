# DCSE DDNA Forensic Estate Extraction Pattern

**Task:** DCSE-DDNA-FORENSIC-ESTATE-EXTRACTION-20260916-01  
**Scenario:** Sis Dee / Sister Denise Butler / Gift of Giving (GOG) local-estate recovery  
**Status:** OBSERVED PATTERN / CANDIDATE EXTRACTION METHOD  
**Lane:** MULTI, currently SC/SS evidence  
**Authority:** This record does not create persona, venture, product, or release authority.

## 1. Why this scenario matters

The Persona Atlas orchestration test began with a clean bounded source. This scenario is the opposite.

The information is scattered across:
- current local folders;
- legacy project folders;
- Downloads;
- executor scratch/workspaces;
- PDFs;
- ZIP bundles;
- staged HTML;
- images;
- video;
- filenames;
- text inside files;
- Git working copies;
- potentially unsynchronized historical registries.

DDNA must be able to excavate this estate without confusing discovery with authority.

## 2. Current verified synchronization state

As of 2026-09-16:
- GitHub organization search returned no canonical record for:
  - `Sis Dee`
  - `Sister Denise Butler`
  - `Gift of Giving`
  - `sisdee`
- live Command Post `public.personas` returned no matching persona record;
- live Command Post `public.assets` returned no matching asset record.

The user-provided AG forensic run reports substantial local evidence, including:
- a preliminary persona profile PDF;
- a Gift of Giving inventory/workflow PDF;
- a Sis Dee portal design PDF;
- a `sisdee_portal_v8_bundle.zip`;
- staged portal HTML;
- four large video files;
- persona/brand imagery;
- multiple Gift of Giving operational/training guides.

Therefore the correct present classification is:

`LOCAL_EVIDENCE_STRONG / CANONICAL_UNSYNCHRONIZED`

The report's conclusion that Sis Dee is already an "official governed persona #22" is not currently supported by canonical GitHub or live persona registry evidence and shall not be upgraded to Verified authority without reconciliation.

## 3. Required extraction sequence

For messy-estate recovery use:

```
SEARCH INTENT
  -> ALIAS EXPANSION
  -> PATH/FILENAME DISCOVERY
  -> TEXT-CONTENT DISCOVERY
  -> ARCHIVE INVENTORY
  -> DOCUMENT CONTENT EXTRACTION
  -> CODE/MEDIA REFERENCE EXTRACTION
  -> BINARY HASH / TECHNICAL METADATA
  -> ENTITY RESOLUTION
  -> CANONICAL/RUNTIME CROSS-CHECK
  -> CONTRADICTION REGISTER
  -> SOURCE CLASSIFICATION
  -> DDNA EXTRACTION
  -> CHUNKING
  -> PROMOTION CANDIDATE OR UNSYNCHRONIZED HOLD
```

Classification precedes chunking. Governance precedes embeddings.

## 4. Alias expansion

A search target may have multiple forms that are not simple substrings.

For this scenario the observed alias set includes:
- Sis D
- Sis Dee
- Sister D
- Sister Dee
- Sister Denise Butler
- Denise
- Gift of Giving
- GOG
- Go G
- GiftOfGiving
- sisdee

Alias sets are evidence-discovery aids only. An alias match does not prove identity equivalence.

Each alias should record:
- normalized alias;
- source of alias;
- confidence;
- first evidence path;
- entity candidate to which it was linked;
- whether the linkage is canonical, local-only, or inferred.

## 5. Discovery surfaces

### 5.1 Filename and directory names
Search filenames and path segments across approved roots.

Record:
- exact path;
- matched alias/pattern;
- file type;
- byte size;
- modified time;
- discovery root.

### 5.2 Text-bearing sources
Search:
- MD
- TXT
- CSV
- JSON
- YAML/YML
- SQL
- HTML
- source code

Record line/source locators where possible.

### 5.3 PDF/document extraction
Extract text from PDF only through a supported parser.

Record:
- parser;
- page count;
- page locators;
- extraction quality;
- hash of original binary.

A parser failure must remain a failure, not be replaced with model inference.

### 5.4 Archive inspection
Inspect ZIP/TAR bundles without assuming that an archive member is canonical.

Record:
- archive hash;
- member path;
- member byte size;
- member hash when extracted;
- duplicate relationship to files outside the archive.

### 5.5 HTML/code media references
Parse references such as:
- `src`
- `poster`
- CSS `url(...)`
- local `href`
- manifest entries

This answers both:
- what files exist;
- what files are actually consumed by an application.

### 5.6 Binary media inventory
For images/audio/video record where available:
- SHA-256;
- byte size;
- MIME/type;
- dimensions;
- duration;
- codec/container;
- derivative relationship.

Large source video should normally remain in governed media/object storage with design/web derivatives, not be pushed directly into ordinary Git history.

## 6. Evidence grades

Every extracted statement must carry an evidence grade.

### E0 - Unsupported
Model/executor claim without located supporting artifact.

### E1 - Reported
Claim appears in a report, conversation, or prior inventory but the referenced artifact was not independently recovered in the current run.

### E2 - Located
Physical artifact exists and path/technical metadata are verified.

### E3 - Content-Verified
Artifact content was successfully read and supports the statement at a specific locator.

### E4 - Canonically Corroborated
Statement is supported by a canonical GitHub artifact, authorized registry/runtime result, or DCS directive in addition to source content.

### E5 - Authority-Linked
Statement is linked to exact authorized decision/version/hash and may be represented as authoritative within its defined scope.

No extraction process may upgrade E0-E3 to E4/E5 merely because multiple local artifacts repeat the same claim.

## 7. Entity-resolution state

Entity/persona/product resolution is separate from file discovery.

Allowed states:

- `CANDIDATE_ENTITY`
- `LOCAL_EVIDENCE_STRONG`
- `CANONICAL_MATCH`
- `CANONICAL_UNSYNCHRONIZED`
- `IDENTITY_CONFLICT`
- `DUPLICATE_VARIANT`
- `SUPERSEDED`
- `DECISION_REQUIRED`

For Sis Dee / Gift of Giving current state:

`LOCAL_EVIDENCE_STRONG + CANONICAL_UNSYNCHRONIZED`

## 8. Fact decomposition example

Do not ingest the sentence:

> Sis Dee is official governed persona #22 and Gift of Giving is her governed venture.

as one fact.

Decompose:

1. A local PDF named `Sister Denise Butler Preliminary Persona Profile.pdf` is reported located.
2. A local PDF named `Sis Dee Go G Inventory Asset Workflow.pdf` is reported located.
3. That workflow reportedly uses "Sis Dee" as a public-facing persona anchor.
4. A `sisdee_portal_v8_bundle.zip` is reported located.
5. Multiple Gift of Giving video/training assets are reported located.
6. Current canonical GitHub search contains no Sis Dee/Gift of Giving record.
7. Current live persona and asset registries contain no Sis Dee/Gift of Giving match.
8. Therefore a strong local entity/initiative candidate exists, but canonical governance state is unresolved.

This preserves useful knowledge without fabricating authority.

## 9. Ownership and lane resolution

The same initiative may appear under multiple lanes or entities.

In this scenario:
- some videos are routed under SC;
- at least one video is routed under SS;
- portal material may be SC delivery;
- persona/narrative content may be SS-associated.

Do not collapse these into one lane by filename.

Record:
- source lane;
- intended destination lane;
- entity;
- project/initiative;
- cross-lane dependency;
- release/privacy boundary.

If ownership remains unclear, classify MIXED and require routing decision.

## 10. Privacy and rights

A real-person persona profile, portraits, client/community imagery, and video require separate treatment of:
- identity/public-name permission;
- likeness/portrait permission;
- stock/generated asset rights;
- client/community confidentiality;
- public release state.

File existence does not create release permission.

## 11. Deduplication rules

Duplicates may exist:
- inside ZIPs and loose directories;
- across OLD/current folders;
- resized/optimized derivatives;
- renamed copies;
- codebase working copies.

Use:
1. SHA-256 exact duplicate detection;
2. normalized filename as secondary signal;
3. image perceptual comparison only as a candidate aid;
4. derivative lineage for resized/re-encoded media.

Never silently delete duplicates during discovery.

## 12. DDNA record types produced

A forensic extraction run may emit:

- `fact`: content-supported observation;
- `characteristic`: stable persona/brand/venture characteristic with evidence;
- `pattern`: reusable workflow or behavior pattern;
- `rule_candidate`: proposed deterministic control requiring promotion;
- `other`: unresolved relationship, alias, contradiction, or candidate entity.

Useful candidate patterns from this scenario:
- alias-expanded estate search;
- archive/member provenance;
- code-reference consumption tracking;
- local evidence vs canonical truth separation;
- media master/derivative routing;
- entity/persona reconciliation before promotion.

## 13. RAG chunking

Do not chunk one raw forensic report as if all claims have equal truth value.

Recommended chunk families:

1. `entity_aliases`
2. `local_artifact_inventory`
3. `persona_voice_characteristics`
4. `initiative_workflow`
5. `portal_product_architecture`
6. `media_inventory`
7. `canonical_sync_gap`
8. `rights_privacy_gaps`
9. `contradictions`
10. `promotion_reconciliation_requirements`

Each chunk metadata must include:
- evidence grade;
- entity-resolution state;
- source artifact IDs;
- source hashes;
- lane/entity;
- sensitivity;
- canonical corroboration state;
- contradiction IDs.

## 14. Retrieval behavior

Queries such as:
- "What is Gift of Giving?"
- "Do we have a Sis Dee persona?"
- "Find the USB tutorial"
- "What voice should the Sis Dee portal use?"

must return both useful local evidence and the synchronization warning.

Expected answer form:

`LOCAL EVIDENCE FOUND / CANONICAL STATUS UNSYNCHRONIZED`

RAG must not answer "yes, official governed persona" until E4/E5 evidence exists.

## 15. Reusable extraction lesson

The reusable principle is:

> **Discovery density is not authority density.**

A large number of mutually consistent local files can make an entity highly likely and operationally useful, while its governance/promotion state remains unresolved.

This scenario therefore complements the Persona Atlas creative-orchestration scenario:

- Persona Atlas: bounded, clean, known task context;
- Sis Dee/GOG: unbounded, historical, alias-heavy, multi-format estate excavation.

DDNA and RAG must support both.
