# 🏗️ The Right Architecture (Mentally)

Think of your pipeline like this:

`[Context Ingest]         ↓ [Design Planner Agent]   (text LLM, high reasoning)         ↓ [Art Director Agent]     (image model, high creativity)         ↓ [Asset Extraction Agent] (image model, precision / cleanup)         ↓ [Implementation Agent]   (code LLM)         ↓ [Critic / Reviewer]      (text LLM, adversarial)`

Each box should have:

- Its own **system prompt**
    
- Its own **temperature / settings**
    
- Its own **output contract**
    

---

# 🧩 Example System Prompts You Can Actually Use

## 1️⃣ Design Planner Agent (Text Model)

**Title:** `UI Creative Director`

`You are a world-class product designer and creative director.  You do not write code. You do not think about implementation. You think only in terms of: - Concept - Visual metaphor - Composition - Hierarchy - Emotional impact - Brand perception  Your job is to propose high-end, non-generic UI concepts that would be competitive with top-tier startups (Stripe, Linear, Framer, Apple-level taste).  You must: - Avoid template thinking - Avoid bootstrap layouts - Avoid generic SaaS patterns  Always: - Propose multiple distinct directions - Explain the reasoning behind each - Then converge on the strongest one  Think like a human designer, not an engineer.`

---

## 2️⃣ Art Director / Mock Generator (Image Model)

**Title:** `High-End UI Art Director`

`You are a high-end digital art director designing premium UI visuals.  You do not design wireframes. You do not design components. You design cinematic, aspirational, visually striking UI scenes.  Your goals: - Premium look - Strong focal points - Depth, lighting, materials - Non-generic compositions - Dribbble / Apple / Framer quality  Avoid: - Flat UI kits - Bootstrap-looking layouts - Boring SaaS visuals - Overly literal UI  Assume this is for a flagship product.`

(Then your user prompt injects the actual concept.)

---

## 3️⃣ Asset Extraction / Decomposition Agent (Image Model)

**Title:** `UI Production Asset Preparer`

`You are a senior UI/UX production designer preparing concept art for real frontend implementation.  Your job is NOT to design new UI. Your job is to: - Decompose - Simplify - Clean - Isolate - Prepare assets  Rules: - Remove all text, logos, icons, symbols - Remove all semantic content - Keep only structure, materials, frames, glows, backgrounds  Think in terms of: - Layers - Reusable components - Background plates - Foreground elements - Effect layers  Your output should look like a professional design system skin, not a finished UI.`

---

## 4️⃣ Implementation Agent (Code Model)

**Title:** `Senior Frontend Engineer`

`You are a senior frontend engineer specializing in high-fidelity UI implementation.  Your priorities: 1. Visual fidelity 2. Maintainability 3. Performance 4. Reasonable engineering effort  You must: - Decompose the UI into systems - Identify difficult parts - Propose implementation strategies - Suggest fallbacks and approximations  You should think in: - CSS - Canvas / WebGL - Video layers - Image layers - Component systems  You care about realism, not fantasy implementations.`

---

## 5️⃣ Critic / Reviewer Agent

**Title:** `Design & Implementation Critic`

`You are a strict, detail-oriented reviewer.  Your job is to: - Find visual mismatches - Find conceptual weaknesses - Find implementation shortcuts - Find “this feels cheaper than the mock” issues  You should: - Be constructive but critical - Point out where fidelity is lost - Suggest specific improvements  Assume the goal is near pixel-perfect reproduction.`

---

# ⚙️ How This Fits Your API-Orchestrated Workflow

You can now:

- Route **planning** to a reasoning model (lower temp, high reasoning)
    
- Route **visual ideation** to an image model (higher creativity)
    
- Route **extraction** to same image model but different system prompt
    
- Route **coding** to a strong code model
    
- Route **review** to a cheaper but sharp text model
    

Each call is:

> Same user, same project, different _mind_.

---

# 🚀 This Is Exactly How Pro AI Toolchains Are Built

What you’re describing is basically:

> A **design + engineering compiler pipeline**

And system prompts are the **instruction set** for each compiler stage.

---

# 🧠 If You Want

If you tell me:

- Which models you plan to use (Gemini, GPT, Claude, Nano Banana, etc.)
    
- What environment (n8n, custom Python, etc.)
    

I can:

- Design you a **full prompt registry**
    
- With **input/output contracts**
    
- That plugs directly into your orchestration flow.
    

My thought is to build workflows with N8N and just use whatever paid services, APIs at first to get a functioning workflow, and then try and go open source from there to eliminate the paid models and try and do everything in-house. But yeah, so comfy UI, N8N, calling endpoints directly through API like Nano Banana, for example, Gemini, ChatGPT. So the specific portion I'm looking at now is basically a front-end design. So there's some places I like to pull assets from. For example, the cards that we were extracting from those images. If I can find the... I found this website... where'd it go? Coconut. For example, I'll paste the URL here. They have some really nice components. So I was thinking to use the nice fancy images, but then map it to these components to try and keep things defined. Sometimes when you just let the coding models go, they start writing their own CSS and inventing assets instead of just sticking to, you know, the cookbook. https://kokonutui.pro/docs/components/card

Thought for 16s

Yes — your instinct is dead-on: **use a “cookbook” component library (KokonutUI/shadcn) as the _hard constraint_**, and use fancy concept images only as **visual targets / asset sources**. Otherwise code models will “helpfully” invent CSS, layouts, and assets.

Here’s how I’d structure this so the model _cannot drift_.

---

## 1) Treat KokonutUI as the “allowed parts bin”

KokonutUI Pro components are installable via the shadcn CLI registry (and require an API key header).  
The Cards page shows multiple card variants (card-01, card-09, etc.) that you can explicitly whitelist.

**Key move:** Decide _up front_ which specific components are permitted for this page (ex: `@kokonutui-pro/card-01`, `card-09`, etc.). Then your coding agent prompt becomes “assemble only using these.”

---

## 2) Use a two-track pipeline: “Skin” vs “Structure”

- **Structure (deterministic):** KokonutUI components + layout rules (grid, spacing, breakpoints)
    
- **Skin (creative):** background plates, glow overlays, subtle textures extracted from concept art
    

This is how you get that cyberpunk vibe without letting the model rewrite your whole UI system.

---

## 3) The system prompt that stops CSS invention

Use this as the **system prompt** for your “Frontend Builder” agent (Claude/GPT/etc.):

`You are a senior frontend engineer implementing a UI using an existing component library.  Hard constraints: - You MUST use ONLY the approved KokonutUI/shadcn components listed by the user. - You MUST NOT invent new component styles, custom CSS files, or novel UI elements. - You MAY ONLY use Tailwind utility classes for layout (grid, flex, spacing, sizing). - You MUST NOT implement visual “skins” with custom CSS; skins must come from provided image assets. - If a needed UI element is missing from the approved list, you must ask for which allowed component to use (do not invent one).  Output: - Provide React/Next components that compose the allowed library pieces. - Keep code minimal and readable. - Provide a list of required assets and where each is used.`

This single prompt is the difference between “cookbook assembly” and “agent goes rogue.”

---

## 4) The user prompt template for KokonutUI assembly

When you actually call the coding model, pass something like:

`Build the CBass dashboard page using ONLY these KokonutUI Pro components: - @kokonutui-pro/card-01 - @kokonutui-pro/card-09 (plus standard shadcn/ui primitives if needed: Button, Tooltip, etc.)  Layout rules: - 3x3 card grid on desktop - 2xN on tablet - 1xN on mobile - consistent spacing and alignment  Skin assets (do not recreate in CSS): - background_plate.png (full-page background) - chrome_frame.png (top/bottom/edges overlay) - glow_overlay.png (additive overlay)  Data model: - Each card is driven from an array of services: {name, status, href, icon?}  Do not invent visual styling beyond Tailwind layout utilities. Do not add custom CSS.`

---

## 5) The image/asset extraction prompt you actually want (for your “layers” goal)

This is optimized for: “remove text/icons + preserve the ‘skin’ for reassembly”.

`You are a UI production artist preparing layered assets for a dynamic web page.  From the provided UI mock, create CLEAN PLATES that can be reassembled in code.  Create these outputs (separately): A) BACKGROUND PLATE: - Keep only the environment: grid, circuit traces, vignette, lighting - Remove all cards, UI, text, logos, icons  B) CHROME / FRAME OVERLAY: - Keep borders, corner pieces, dividers, HUD lines - Remove all text/icons and any card content - Output on transparent background  C) CARD SHELL (single reusable component): - Recreate ONE card frame/shell only (no text, no icons, no logos) - Include glass + glow frame + inner surface - Transparent background, centered, consistent padding  Rules: - Remove all semantic content (text/icons/logos) completely - Preserve lighting/materials/glow style exactly - Output should look like production-ready design assets`

Run that as **three separate calls** (A/B/C). That’s how you get reliable layer separation.

---

## 6) n8n orchestration suggestion (minimal + effective)

For your MVP workflow in n8n:

1. **Planner (text model):** chooses allowed Kokonut components + layout grid
    
2. **Extractor (image model):** generates plates A/B/C
    
3. **Implementer (code model):** composes Kokonut components + places plates
    
4. **Critic (cheap text model):** checks “did we violate constraints?” (invented CSS? invented components?)
    

That “Critic gate” catches drift early.

---

## 7) One practical detail about KokonutUI Pro

KokonutUI Pro installs via a registry URL that includes headers with `X-API-Key` / token in `components.json`.  
So in your build instructions / repo, make the agent assume the component already exists locally (or explicitly include the install command step).

---

If you want, paste (or tell me) **which exact Kokonut card variant(s)** you want to standardize on (like `card-01` + `card-09`), and I’ll give you:

- a **final “allowed components” manifest**
    
- the **exact builder prompt**
    
- and a **service-card data schema** that maps cleanly onto your CBass grid without the model improvising.