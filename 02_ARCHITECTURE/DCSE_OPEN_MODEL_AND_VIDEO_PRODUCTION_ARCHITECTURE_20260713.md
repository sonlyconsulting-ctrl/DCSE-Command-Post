# DCSE Open Model and Video Production Architecture

Date: 2026-07-13
Status: ACTIVE BUILD DIRECTION
Authority: DCS
Lane: DCSE / Command Post / DDNA / Media

## Decision

DCSE will use a hybrid production architecture.

Local and open-source systems provide privacy, control, reusable workflows, low-cost iteration, DDNA development, and provider independence.

Commercial APIs provide premium generation quality, speed, difficult motion, native audio, higher resolution, and production fallback when local hardware is insufficient.

No single model or provider becomes the operating system. The DCSE Agent OS routes each job to the most appropriate approved engine.

## Ollama Role

Ollama is the primary local language-model runtime and model gateway for approved open-weight models.

Ollama is responsible for:

1. Interactive local chat
2. Script and treatment generation
3. Story structure and scene decomposition
4. Shot lists and camera-direction drafts
5. Prompt generation for image and video engines
6. Product and campaign metadata
7. Source excavation and classification
8. DDNA comparison and drift detection
9. Caption, title, description, and variant generation
10. Private preliminary reasoning before frontier-model escalation

Ollama is not the video renderer. It directs and supports the visual production engines through the Agent OS.

## Open-Source and Minimally Filtered Reasoning

The Agent OS will register at least one local Raw Reasoning and Divergence model. This model may be selected for broad internal ideation, critique, alternative concepts, and less conformity-biased DDNA analysis.

The model may be minimally provider-filtered, but it remains governed by DCSE permissions.

It may not autonomously:

1. Publish or deploy
2. Delete or overwrite protected assets
3. Expose credentials
4. Modify production databases
5. Cross protected lane boundaries
6. Generate or distribute unlawful content
7. Use a real person's identity or likeness without authorization

Unfiltered generation behavior does not create unfiltered system authority.

## Local Visual Production Layer

ComfyUI is the preferred local visual workflow engine because it can expose node-based image, video, audio, and related workflows through APIs and simplified application interfaces.

Initial local video model candidates:

1. Wan family for text-to-video, image-to-video, editing, and efficient local variants
2. LTX-Video for rapid iteration, lower-resource variants, image-to-video, keyframes, extension, and commercial-production candidates
3. HunyuanVideo for higher-compute cinematic experimentation
4. Additional approved open models after license, hardware, quality, and provenance review

Every local model must have a registry record containing:

- model and checkpoint name
- source and version
- license
- commercial-use status
- hardware requirement
- supported workflows
- content and identity limitations
- benchmark results
- approved lanes
- installation status
- provenance and checksum

## Commercial API Layer

The Agent OS will support interchangeable video APIs rather than binding the company to one provider.

Initial provider candidates include:

1. OpenAI Sora video API for rapid concepts and higher-quality production variants
2. Google Veo API for video generation with native audio and advanced direction capabilities
3. Runway API for text-to-video and image-to-video production
4. Luma Ray API for text-to-video, image-to-video, keyframes, and higher-resolution delivery
5. Additional providers after quality, price, data-use, rights, and reliability review

API credentials must remain server-side. Each provider adapter must support job creation, status polling, failure handling, output retrieval, cost capture, and artifact registration.

## Production Routing Rules

### Route to local open source when

- the material is private or commercially sensitive
- the work is exploratory, repetitive, or high volume
- many variants are required
- the workflow needs exact node-level control
- the company is developing reusable house styles, LoRAs, templates, or DDNA
- API restrictions block an otherwise lawful internal concept
- cost discipline is more important than immediate top-tier fidelity
- the output is a storyboard, animatic, concept test, background, transition, or draft

### Route to a commercial API when

- a final client-facing hero shot is required
- complex movement, cinematic stability, or prompt adherence exceeds local capability
- native synchronized audio is important
- the delivery deadline is more important than local render cost
- local hardware cannot complete the render efficiently
- a specific API consistently wins the approved benchmark for the requested shot type

### Route to both when

- the job is commercially important
- comparative candidates improve final selection
- a local rough cut can reduce paid iterations
- the API output requires local cleanup, extension, upscaling, compositing, or versioning

## Standard Video Production Workflow

Creative request
> source and rights check
> DDNA retrieval
> script and treatment
> storyboard and shot list
> local concept generation
> candidate scoring
> API escalation where justified
> edit, composite, voice, music, and captions
> identity and rights review
> DCS approval
> master export
> aspect-ratio and duration variants
> durable URL assignment
> product and campaign registration
> Tribunal and GitHub receipt
> quality and cost feedback to DDNA

## Media Registry Requirements

Every generated or imported production asset must preserve:

- project, entity, lane, and campaign
- source prompt and approved prompt revision
- model, provider, checkpoint, and version
- workflow identifier and parameters
- seed where available
- source images, reference frames, and consent record
- license and commercial-use basis
- generation and editing cost
- duration, dimensions, frame rate, codec, and audio state
- content hash
- raw, working, candidate, approved, and published versions
- internal storage reference
- public durable URL or restricted signed URL
- approval status and approver
- related product, website, and campaign placements

## Initial Implementation Order

1. Add Ollama health discovery and model listing to the existing Command Post.
2. Register local reasoning, coding, and Raw Divergence model roles.
3. Add ComfyUI as the local visual workflow adapter.
4. Create provider-neutral video job and output interfaces.
5. Build one local storyboard and animatic workflow.
6. Build one API-based premium video workflow.
7. Add comparative scoring for quality, speed, cost, DDNA fit, and rights risk.
8. Register outputs in the media and durable URL system.
9. Apply the workflow first to approved SC, SJL, Bee Beauty, CTJ, TSL, and website media requirements.

## Company Position

DCSE video production will not be only an API reseller and will not be constrained to local open-source quality.

The company will own the workflow, DDNA, prompts, source intelligence, production logic, model routing, asset history, approvals, and client experience. Models and providers remain replaceable production resources.