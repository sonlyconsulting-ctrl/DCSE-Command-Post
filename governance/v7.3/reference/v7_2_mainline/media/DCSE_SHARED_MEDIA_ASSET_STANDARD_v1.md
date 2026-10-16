# DCSE Shared Media Asset Standard v1

**Status:** OPERATIVE upon Level 0 promotion  
**Authority:** DCS Level 0  
**Parents:** D06, D09, D10, D12, D18, D19, D20, D22  
**Purpose:** Establish one governed media asset model for product, campaign, website, image, video, and audio workflows.

## 1. Canonical model

GitHub is the canonical **control/index** surface. Governed object storage is the default canonical binary surface for large/high-resolution/frequently changing media.

`PROJECT MANIFEST -> MEDIA ASSET MANIFEST -> AUTHORIZED BINARY STORAGE -> WORKFLOW -> DERIVED ASSET -> HASH/PROVENANCE UPDATE -> QA -> RELEASE`

## 2. Asset classes

- PRODUCT_PERSONA_IMAGE
- PRODUCT_HERO
- LOGO_WORDMARK
- BACKGROUND_TEXTURE
- SOURCE_REFERENCE_IMAGE
- BROLL_VIDEO
- SOURCE_VIDEO
- VOICE_AUDIO
- MUSIC_AUDIO
- SFX_AUDIO
- THUMBNAIL
- GENERATED_DERIVATIVE
- EDIT_PROJECT
- FINAL_DELIVERABLE

## 3. Required start inventory

For every product/media task, inventory current:

- product/persona images;
- current images in use;
- approved backgrounds/textures;
- source/reference files;
- logos/wordmarks;
- fonts/typography references;
- audio/voice/music source files where applicable;
- video/B-roll/source footage where applicable.

Missing required visual/media assets invoke the Product Start Gate and DCS-E escalation.

## 4. Storage routing

### GitHub
Stores:
- project and media manifests;
- hashes/metadata;
- prompts/scripts/storyboards/transcripts/captions/shot lists;
- rights/release records;
- small assets where appropriate;
- LFS pointers when explicitly selected.

### Object storage
Stores:
- high-resolution images;
- video/audio masters;
- source recordings;
- B-roll;
- intermediate renders;
- image sequences;
- large design exports;
- generated binary variants;
- packaged binary deliverables.

### Local working files
May hold temporary editing cache/source copies but are not canonical absent D22 designation.

## 5. Access

"Accessible to all" means accessible to all **authorized task participants** whose lane/classification permits the asset.

Private media SHALL use authenticated/RLS/scoped server access or time-limited signed retrieval. Service-role credentials SHALL never be given to models or browsers.

## 6. Manifest identity

Every canonical asset SHALL have:
- stable asset ID;
- project/task identity;
- canonical URI/path;
- SHA-256;
- byte size/MIME type;
- dimensions/duration as applicable;
- entity/lane/classification;
- provenance/source;
- creator/provider/model;
- rights/license/release;
- public-release state;
- access class;
- version;
- derivation links;
- validation state.

## 7. Rights and public release

No asset becomes public because it exists in storage or GitHub. Public release requires the applicable product/campaign/media gate.

## 8. Shared storage implementation

The physical shared media store SHALL use a private-by-default bucket/container with explicit upload/read/update/delete policy, object naming, size/MIME restrictions, lifecycle/retention, and negative access tests.

Until that storage surface passes its access tests, manifests may register `STORAGE_PENDING` and current governed source locations without claiming shared binary availability.
