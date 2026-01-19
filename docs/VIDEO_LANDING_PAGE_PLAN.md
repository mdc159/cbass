# Plan: Video Landing Page for CBass.space

> **Created:** 2026-01-12
> **Status:** Planning

## Current State

**Video inventory** (in `X:\GitHub\CBass\media`):

| File | Duration | Resolution | Size | Notes |
|------|----------|------------|------|-------|
| `cbass-logo-lowfreq-pulse.mp4` | 5s | 1924x1076 | **3MB** | Smallest, good candidate |
| `cbass-logo-animation-01.mp4` | 5s | 1440x1920 | 5MB | Portrait orientation |
| `cbass-logo-slow-zoom-01.mp4` | 5s | 1924x1076 | 5MB | |
| `cbass-logo-slow-zoom-02.mp4` | 5s | 1924x1076 | 5MB | |
| `cbass-logo-animation-02.mp4` | 10s | 1924x1076 | 7MB | |
| `cbass-intro-with-audio-01.mp4` | 5s | 1924x1076 | 8MB | Has audio |
| `cbass-intro-with-audio-02.mp4` | 5s | 1924x1076 | 10MB | Has audio |
| `cbass-logo-hexagon-01.mp4` | 10s | 1924x1076 | 18MB | High quality |
| `cbass-logo-hexagon-02.mp4` | 10s | 1924x1076 | 17MB | High quality |
| `cbass-logo-hexagon-03.mp4` | 10s | 1924x1076 | 19MB | High quality |

**Current landing page**: Login form at `cbass.space` (`/opt/cbass/dashboard/app/page.tsx`)

---

## Options Considered

### Option 1: Optimized Video Background (Recommended)

**Approach**: Re-encode video to web-optimized format, serve from S3+CloudFront CDN, use as full-screen background behind login form.

**Pros**:
- Professional "wow factor" landing page
- CDN ensures fast global delivery
- Poster image shows instantly while video loads
- Video loops seamlessly

**Cons**:
- Requires video re-encoding
- S3/CloudFront setup needed
- ~1-2MB final size still adds some load time

**Implementation**:
1. Re-encode best video to web-optimized MP4 + WebM:
   - Resolution: 1280x720 (720p) - good for backgrounds
   - Bitrate: 1-2 Mbps (down from 5-15 Mbps)
   - Format: H.264 MP4 + VP9 WebM for browser compatibility
   - Target size: ~1-2MB for 5-10 second loop
2. Extract first frame as poster image (JPEG, ~50KB)
3. Upload to S3 bucket with CloudFront distribution
4. Update landing page with video background

**Code pattern**:
```tsx
<div className="fixed inset-0 -z-10">
  <video
    autoPlay
    loop
    muted
    playsInline
    poster="/poster.jpg"
    className="w-full h-full object-cover"
  >
    <source src="https://cdn.cbass.space/bg.webm" type="video/webm" />
    <source src="https://cdn.cbass.space/bg.mp4" type="video/mp4" />
  </video>
  <div className="absolute inset-0 bg-black/50" /> {/* Overlay for readability */}
</div>
```

---

### Option 2: Animated WebP/AVIF (Lightweight Alternative)

**Approach**: Convert video to animated WebP or AVIF image format. Much smaller than video, auto-plays everywhere, no audio needed.

**Pros**:
- Tiny file size (~200-500KB for 5s loop)
- No video player needed - just an `<img>` tag
- Works everywhere, even where autoplay is blocked
- Can be served from any static host

**Cons**:
- Lower quality than video
- No audio option
- Conversion can be lossy

**Implementation**:
1. Convert video to animated WebP:
   ```bash
   ffmpeg -i input.mp4 -vf "fps=15,scale=1280:-1" -loop 0 -q 80 output.webp
   ```
2. Use as background image with CSS animation fallback

---

### Option 3: Video Splash + Login Transition

**Approach**: Full-screen video plays on first visit, then transitions to login form. Like a movie intro.

**Pros**:
- Maximum visual impact
- Can use audio (with user interaction)
- Full attention on branding

**Cons**:
- Extra click/wait before login
- May annoy repeat visitors
- Needs "skip" button

**Implementation**:
1. Show full-screen video on load
2. After video ends (or skip clicked), fade to login form
3. Store cookie to skip on repeat visits

---

### Option 4: Hero Section with Inline Video

**Approach**: Redesign landing page with hero section containing video, login form below or to the side.

**Pros**:
- Video is prominent but doesn't block login
- Works well on mobile
- Can show more content

**Cons**:
- More complex layout
- Video competes with login form for attention

---

### Option 5: Cloudflare Stream / Mux (Managed Video)

**Approach**: Use a managed video streaming service that handles encoding, CDN, and adaptive bitrate.

**Pros**:
- Automatic quality adaptation
- Global CDN included
- No encoding needed on your end

**Cons**:
- Monthly cost ($5-20/month for light usage)
- Another service to manage
- Overkill for a single background video

---

## Final Approach: Video Landing + Hidden Login Easter Egg

### Concept
- **Full-screen looping video** as the entire landing page
- **No visible login form** initially - just the video
- **Click the C8 logo** (or designated hotspot) to reveal login form
- Creates an "exclusive access" feel - only those who know can log in

### User Decisions
- **CDN**: Already have S3 + CloudFront set up ✓
- **Videos loop seamlessly**: Front/last frames match ✓
- **Video choice**: Will pick later (infrastructure supports easy swap)
- **Easter egg type**: Hidden trigger (click logo to reveal)

### Technical Implementation

#### 1. Video Optimization
Re-encode selected video for web delivery:
```bash
# MP4 (H.264) - wide compatibility
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow \
  -vf "scale=1280:-2" -an -movflags +faststart output.mp4

# WebM (VP9) - better compression
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 \
  -vf "scale=1280:-2" -an output.webm

# Poster image (first frame)
ffmpeg -i input.mp4 -vframes 1 -q:v 2 poster.jpg
```

Target specs:
- Resolution: 1280x720 (720p)
- Bitrate: ~1.5 Mbps
- Final size: ~1-2MB per format
- No audio (muted autoplay)

#### 2. S3 + CloudFront Setup
Upload to existing S3 bucket:
```
s3://your-bucket/cbass/
├── bg.mp4        # H.264 version
├── bg.webm       # VP9 version
└── poster.jpg    # First frame
```

CloudFront URL pattern: `https://cdn.cbass.space/cbass/bg.mp4`

#### 3. Landing Page Code (`app/page.tsx`)

```tsx
"use client"

import { useState } from "react"
import { LoginForm } from "./login-form"

export default function LandingPage() {
  const [showLogin, setShowLogin] = useState(false)

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Full-screen video background */}
      <video
        autoPlay
        loop
        muted
        playsInline
        poster="https://cdn.cbass.space/cbass/poster.jpg"
        className="absolute inset-0 w-full h-full object-cover"
      >
        <source src="https://cdn.cbass.space/cbass/bg.webm" type="video/webm" />
        <source src="https://cdn.cbass.space/cbass/bg.mp4" type="video/mp4" />
      </video>

      {/* Clickable logo area (easter egg trigger) */}
      <div className="absolute inset-0 flex items-center justify-center">
        <button
          onClick={() => setShowLogin(true)}
          className="p-8 cursor-pointer hover:scale-105 transition-transform"
          aria-label="Access login"
        >
          {/* Invisible hotspot over logo in video, or overlay a subtle logo */}
          <div className="w-48 h-48 rounded-full" />
        </button>
      </div>

      {/* Hidden login form - revealed on click */}
      {showLogin && (
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center animate-fadeIn">
          <div className="relative">
            <button
              onClick={() => setShowLogin(false)}
              className="absolute -top-4 -right-4 text-white/70 hover:text-white"
            >
              ✕
            </button>
            <LoginForm />
          </div>
        </div>
      )}
    </div>
  )
}
```

#### 4. Subtle Hint (Optional)
Add a very subtle hint for users who don't know:
- Faint "Click to enter" text that appears after 5 seconds
- Cursor changes to pointer over the logo area
- Small pulsing glow on the hotspot

---

## Implementation Steps

1. [ ] Choose video(s) to optimize (can do multiple for A/B testing)
2. [ ] Re-encode to web-optimized MP4 + WebM (720p, ~1-2MB)
3. [ ] Extract poster frame from first frame
4. [ ] Upload to S3 bucket
5. [ ] Configure CloudFront cache headers
6. [ ] Refactor `app/page.tsx` to split login into component
7. [ ] Implement video background with hidden login trigger
8. [ ] Add fade-in animation for login reveal
9. [ ] Test on mobile (ensure hotspot works with touch)
10. [ ] Deploy to VPS

---

## Verification

- [ ] Video loads and plays on desktop (Chrome, Firefox, Safari)
- [ ] Video loads and plays on mobile (iOS Safari, Android Chrome)
- [ ] Video loops seamlessly without visible jump
- [ ] Clicking logo/hotspot reveals login form
- [ ] Login form animates in smoothly with backdrop blur
- [ ] Close button hides login form
- [ ] Login authentication still works (Supabase)
- [ ] Test on slow connection (3G throttling in DevTools)
- [ ] Poster image shows while video loads
- [ ] Touch works on mobile for easter egg trigger

## Files to Modify

| File | Change |
|------|--------|
| `/opt/cbass/dashboard/app/page.tsx` | Replace with video landing + hidden login |
| `/opt/cbass/dashboard/app/login-form.tsx` | Extract login form to separate component (new) |
| `/opt/cbass/dashboard/app/globals.css` | Add fadeIn animation |
| S3 bucket | Upload optimized video files |

## CDN URLs (Example)

```
https://cdn.cbass.space/cbass/bg.mp4
https://cdn.cbass.space/cbass/bg.webm
https://cdn.cbass.space/cbass/poster.jpg
```

(Adjust based on your actual CloudFront distribution domain)
