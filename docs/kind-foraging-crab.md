# Bass Lab Research Brief

## Project Context

**Goal:** Build "Bass Lab" - a music AI tool on cbass.space to get a university biology student (and bassist) excited about AI and open source.

**The Hook:** He's skeptical of AI, sees it as a threat. We need to show him it's a tool that augments his passion (bass guitar) rather than replaces it.

**Existing Infrastructure:**
- **CBass stack** (cbass.space) - Docker Compose with n8n, Open WebUI, Ollama, Supabase, Qdrant, Neo4j, etc.
- **Karaoke pipeline** (separate project) - Demucs 6-stem separation on RunPod serverless GPU, React web player
- **Shared resources:** RunPod GPU, S3/CloudFront CDN

**Target Experience:**
1. User uploads audio or pastes YouTube link
2. Bass stem gets isolated (via existing Demucs pipeline)
3. Visual waveform + spectrogram displayed (eye candy)
4. AI analyzes the audio: key, tempo, time signature, tone description, playing technique
5. Recommendations: "To get this tone, try..."

---

## Research Topics

### 1. Qwen2-Audio Deployment (OPEN SOURCE)

**What we know:**
- 8.2B parameter model from Alibaba/Qwen
- Can identify key, tempo, time signature, genre, instruments
- Outperforms Gemini 1.5 Pro on audio understanding benchmarks
- Available on HuggingFace: `Qwen/Qwen2-Audio-7B-Instruct`

**Research needed:**
- [ ] How to containerize for RunPod serverless (Dockerfile examples?)
- [ ] GPU memory requirements - can it coexist with Demucs on same GPU?
- [ ] Input format - how to send audio (base64? file path? streaming?)
- [ ] Output format - structured JSON or just text?
- [ ] Latency for ~30 second audio clips
- [ ] Any existing RunPod templates or community deployments?
- [ ] Comparison with Qwen2-Audio-7B vs Qwen2-Audio-7B-Instruct

**Links to explore:**
- https://github.com/QwenLM/Qwen2-Audio
- https://huggingface.co/Qwen/Qwen2-Audio-7B-Instruct
- https://arxiv.org/html/2407.10759v1

---

### 2. Other Open Source Music AI Models

**Research needed:**
- [ ] **MusicGen (Meta)** - Text-to-music generation, could generate practice backing tracks
  - https://github.com/facebookresearch/audiocraft
  - Deployment options, model sizes, quality vs speed tradeoffs

- [ ] **AudioLDM2** - Text-to-audio generation
  - https://github.com/haoheliu/AudioLDM2
  - Use cases for Bass Lab?

- [ ] **CLAP (LAION)** - Audio-text embeddings (like CLIP but for audio)
  - https://github.com/LAION-AI/CLAP
  - Could power "find similar bass tones" feature

- [ ] **Essentia** - Traditional audio analysis (not deep learning)
  - https://github.com/MTG/essentia
  - Tempo, key, beat tracking - might be faster/cheaper than LLM for basics

- [ ] **Whisper** - Already in Ollama, any music transcription capabilities?

- [ ] **Any newer models from 2024-2025?** - Music understanding space is moving fast

**Key question:** What's the best combo for our use case - fast traditional analysis (Essentia) + deep understanding (Qwen2-Audio)?

---

### 3. Audio Visualization Libraries (OPEN SOURCE)

**Goal:** Eye candy. Make it look impressive in a web browser.

**Research needed:**
- [ ] **wavesurfer.js** - https://wavesurfer-js.org/
  - Waveform rendering, mature library
  - Plugin ecosystem?
  - Real-time playback sync?

- [ ] **tone.js** - https://tonejs.github.io/
  - Web Audio API wrapper
  - Better for synthesis/playback than visualization?

- [ ] **p5.js** - https://p5js.org/
  - Creative coding, great for spectrograms
  - Examples of audio visualization?

- [ ] **peaks.js** (BBC) - https://github.com/bbc/peaks.js
  - Designed for audio editing interfaces
  - Might be more practical than flashy

- [ ] **Three.js / WebGL options**
  - 3D visualizations - overkill or awesome?
  - Performance considerations

**Key questions:**
- Best library for real-time spectrogram that looks impressive?
- What do professional DAWs/audio tools use for web interfaces?
- Mobile performance - will this work on a phone?

---

### 4. Tone Analysis / Matching (OPEN SOURCE)

**Goal:** "This bass sounds like X, here's how to get that tone"

**Research needed:**
- [ ] **Open source tone matching projects** - Do any exist?
- [ ] **EQ curve analysis** - Tools that extract frequency profile
- [ ] **Effect detection** - Identifying distortion, compression, chorus, etc.
- [ ] **Timbre analysis** - Academic/open source implementations
- [ ] **Guitar/bass amp modeling projects** - NAM, ToneLib, etc. - any analysis tools?

**Specific questions:**
- Can we compare two audio clips and say "these are 85% similar in tone"?
- Any datasets of "known tones" (e.g., "Flea on Blood Sugar Sex Magik") we could reference?
- Is this a solved problem or bleeding edge?

---

### 5. RunPod Architecture

**Current setup:** Demucs worker on RunPod serverless

**Research needed:**
- [ ] Single endpoint with multiple models vs. separate endpoints
  - Pros/cons of each approach
  - How does billing work?

- [ ] Cold start times for serverless GPU
  - Can we keep it warm? Cost implications?
  - User experience if 30-60 second spin-up?

- [ ] Container optimization
  - Multi-model Docker image best practices
  - Shared dependencies between Demucs and Qwen2-Audio?

- [ ] Cost estimation
  - Current Demucs cost per song
  - Projected Qwen2-Audio cost per analysis
  - Ways to optimize (batch processing, caching, etc.)

---

### 6. Frontend Architecture

**Constraints:**
- Should feel "premium" with eye candy
- Karaoke player uses React 19 + Vite 7
- VPS has no GPU, so all heavy lifting is RunPod

**Research needed:**
- [ ] **React 19 + audio visualization** - Best practices, performance
- [ ] **Alternative frameworks** - Svelte, Vue, vanilla JS - any advantages for audio apps?
- [ ] **Web Audio API** - Direct usage vs. library wrappers
- [ ] **Progressive loading** - Show waveform while analysis runs
- [ ] **Mobile-first considerations** - Touch interactions, performance

**UI/UX inspiration:**
- [ ] What do existing audio analysis tools look like? (Splice, LANDR, etc.)
- [ ] Music production software web interfaces
- [ ] Any open source audio tool frontends to learn from?

---

### 7. n8n Integration Patterns

**Research needed:**
- [ ] Binary file handling in n8n - best practices for audio
- [ ] Long-running workflow patterns - RunPod jobs can take minutes
- [ ] Webhook callback patterns - how karaoke pipeline does it
- [ ] Open WebUI → n8n → RunPod → response flow
- [ ] Error handling and retry logic for audio processing

---

### 8. Open Source Contribution Opportunities

**Goal:** Find projects the son could contribute to

**Research needed:**
- [ ] Qwen2-Audio - are they accepting contributions? Good first issues?
- [ ] wavesurfer.js or other viz libraries - contribution guidelines?
- [ ] Essentia - community activity?
- [ ] Any music AI projects specifically looking for contributors?
- [ ] Could Bass Lab itself become an open source project others use?

**Key question:** What's a realistic "first PR" opportunity for someone new to open source but with music domain knowledge?

---

### 9. Monetization & Business Potential

**Context:** cbass.space already has authentication via Supabase. This could become a real business.

**Existing infrastructure:**
- Supabase auth (email, OAuth) - already configured
- User management - can track usage per user
- Database - can store subscription status, usage limits

**Research needed:**
- [ ] **Stripe integration with Supabase**
  - Supabase + Stripe patterns (there are templates)
  - Webhook handling for subscription events
  - n8n workflows for payment processing?

- [ ] **Pricing models for audio AI SaaS**
  - What do competitors charge? (LALAL.AI, Moises, etc.)
  - Per-song vs. subscription vs. credits model
  - Free tier limits (X songs/month?)

- [ ] **Usage metering**
  - Track processing jobs per user
  - Cost pass-through (RunPod costs → user pricing)
  - Rate limiting implementation

- [ ] **Legal/licensing considerations**
  - Terms of service for audio processing
  - Copyright considerations (users uploading music)
  - Open source license compatibility with commercial use

**Competitor analysis needed:**
| Service | Pricing | Features |
|---------|---------|----------|
| LALAL.AI | ? | Stem separation |
| Moises | ? | Stem separation + practice tools |
| Splitter.ai | ? | Free stem splitting |
| Others? | ? | ? |

**Key questions:**
- What's the minimum viable paid feature? (Stem separation alone? + AI analysis?)
- How to price to cover RunPod costs + margin?
- Free tier to attract users, paid tier for power features?

**The entrepreneurship hook:**
- Son sees real users paying for something he helped build
- Learns SaaS basics (auth, payments, usage tracking)
- Potential income stream from his own platform
- Real-world business experience for resume

---

## Deliverables Needed

1. **Model comparison matrix** - Qwen2-Audio vs alternatives for our specific use case
2. **Visualization library recommendation** - With code examples if possible
3. **RunPod deployment guide** - How to add Qwen2-Audio to existing setup
4. **Architecture diagram** - How all pieces connect
5. **Cost estimate** - Per-analysis pricing
6. **Open source contribution map** - Where could the son get involved?
7. **Competitor pricing analysis** - What do similar services charge?
8. **Stripe + Supabase integration guide** - How to add payments

---

## Success Criteria

The son should be able to:
1. Upload/link a song with a bass line he wants to learn
2. See an impressive visual representation
3. Get intelligent analysis (key, tempo, tone description)
4. Understand "this is AI helping me, not replacing me"
5. Eventually peek under the hood and see how it works
6. Maybe even contribute improvements back to the tools
7. **Potentially monetize** - turn it into a side business if there's demand

---

## The Long Game (Phases)

**Phase 1: Wow Factor**
- Launch karaoke stem splitter → "Holy shit I can isolate bass from any song"
- Launch Bass Lab → "And it tells me what key/tempo/tone it is"

**Phase 2: Curiosity**
- He asks "How does this work?"
- Show him the stack: n8n workflows, RunPod, Supabase
- Let him tinker

**Phase 3: Ownership**
- He makes his first improvement or customization
- First open source PR to an upstream project
- "I built this" feeling

**Phase 4: Entrepreneurship**
- Other musicians want to use it
- Add Stripe, set up pricing
- First paying customer → "I made money from code"

**Phase 5: Bridge to Career**
- Same patterns apply to biology (research tools, data analysis)
- Resume: "Built and monetized an AI-powered music analysis platform"
- Understands AI as a tool, not a threat

---

## Notes

- Prioritize open source solutions throughout
- Eye candy matters - this needs to look impressive on first use
- Keep the door open for biology applications later (same patterns apply)
- The karaoke stem splitter is the existing "wow factor" - Bass Lab extends it
