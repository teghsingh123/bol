# Bol - ਬੋਲ

> *Preserving the lost words of the late 90s and 2000s underground Punjabi music scene.*

---

## What is Bol?

Bol (ਬੋਲ) means *words* or *to speak* in Punjabi. It is an open archive dedicated to recovering and preserving lyrics from the underground Punjabi music scene of the late 90s and early 2000s — a period of extraordinary creative output that has been largely undocumented.

This era produced a distinct sound rooted not in Punjab itself, but in the British cities where Punjabi communities had put down new roots. Birmingham, Bradford, and London were the centers of gravity. The children and grandchildren of Punjabi immigrants — raised between two cultures, speaking Punjabi at home and English outside — found their voice through music that blended traditional folk music with reggae, hip-hop, and electronic production.

Daytime discos in Bradford, where teenagers would skips school to catch their favorite acts, became legendary underground spaces. The music circulated on casettes, passed hand to hand within South Asian communities, largely invisible to the main stream. Much of it was never formally released or documented. Tracks exist today only as low-quality rips with no metadata, no credits, and no lyrics.

Streaming platforms have brought some of this music to new audiences — but the lyrics, the actual *Bol* remeains missing. They are not on Genius or any old lyrics forums. In many cases, they only exist in the memory of listeners who grew up with them.

Bol is an attempt to change that. Using AI-Assisted audio transcription, we extract lyrics from audio tracks, validate them by hand, and build a searchable, permanent record of this music — in Gurmukhi, Shahmukhi, and Romanized script.

This is not just a tech project. It is an act of cultural preservation.

--- 

# How It Works

Bol uses a four-phase pipeline to go from raw audio to verified, searchable lyrics.

---

### Phase 1 — Audio Preparation

Before any audio transcription can happen, the audio needs to be cleaned and isolated.

- Collect source tracks in any format (MP3, WAV, FLAC)
- Normalize audio levels and reduce noise where possible — many old recordings have tape hiss, clipping, or heavy reverb
- Run tracks through **Demucs** (Meta's open-source audio separator) to isolate the vocal layer from instruments — dhol, tumbi, harmonium, bass, and any other accompaniment get stripped away
- The result is a clean vocal-only audio file, ready for transcription
This step alone significantly improves accuracy. Feeding a full music mix into a speech model produces poor results; feeding isolated vocals produces good ones.
 
---

### Phase 2 — Transcription
 
The vocal audio is passed through **OpenAI Whisper (large-v3)**, the most accurate open-source speech recognition model available.
 
- Language is set to Punjabi, with output in Gurmukhi script by default
- For tracks from the Pakistani side of the scene, Shahmukhi (Urdu script) output is also supported
- Whisper produces not just text but **timestamps** — every line of lyrics is tied to a specific moment in the track, enabling synced (karaoke-style) display
- The raw transcript is saved alongside confidence scores, flagging sections where the model was uncertain
Expected accuracy out of the box: 70–85%, depending on recording quality and dialect. The pipeline does the heavy lifting, but human correction is always required.
 
---

### Phase 3 — Correction and Validation
 
Raw AI transcripts are never published directly. Every track goes through a human correction pass.
 
- A simple editing interface lets contributors play a section of audio and edit the transcript side by side
- Slang, regional dialect, proper nouns, and fast-phrased lines are the most common failure points
- Corrections are tracked so the same mistakes can inform future improvements
- Community contributors who know this music and its language are the most important part of this phase — the AI starts the work, humans finish it
---

### Phase 4 — Storage and Display
 
Verified lyrics are stored in a structured database alongside track metadata.
 
- Artist name, year, album or cassette title, region, language/script
- Lyrics in Gurmukhi, Shahmukhi, and/or Romanized form
- Timestamps for synced playback where available
- Source notes (which digitization, any known credits)
A frontend lets users search by artist, keyword, or browse the full archive. Lyrics can be read alongside the track, with synced highlighting where timestamps exist.
 
---

## Tools
 
| Tool | Purpose |
|---|---|
| Demucs | Vocal isolation from music |
| Whisper large-v3 | Speech-to-text transcription |
| Python | Pipeline glue |
| Google Colab | Optional free GPU environment |
| SQLite | Lyrics and metadata storage |
| React | Frontend archive and editor |
 
---

## Status
 
Early development. The pipeline is being built and tested. Contributions welcome — especially from anyone with knowledge of this music, its artists, or its language.
 
---

## Name
 
**Bol** — ਬੋਲ — *words. speak. say it.*