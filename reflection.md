# Reflection: What I Learned from Testing the Music Recommender

This document compares pairs of user profiles I tested and explains what changed between them — and why.

---

## Comparison 1: High-Energy Pop vs. Chill Lofi

**What changed:**
The High-Energy Pop profile returned loud, upbeat songs like Sunrise City and Gym Hero. The Chill Lofi profile returned calm, quiet songs like Midnight Coding and Library Rain. The two lists had almost no overlap.

**Why it makes sense:**
These two profiles are almost complete opposites. Pop has high energy (0.9) and a happy mood, while Lofi has low energy (0.4) and a chill mood. Because energy carries the most weight in the scoring, the system naturally separated them into two completely different clusters. This is the clearest example of the recommender working correctly — when preferences are very different, the results should be very different too.

**What this tells us:**
The system works best when user preferences are clear and sit at opposite ends of the spectrum. It confidently separates very different tastes.

---

## Comparison 2: Intense Rock vs. Conflicting Profile (high energy + dark mood + low valence)

**What changed:**
Both profiles asked for high-energy rock. But the Conflicting Profile also set mood to "dark" and valence to 0.1 (very low — meaning sad or gloomy). The results shifted noticeably. Storm Runner (rock, intense) still ranked #1 in both cases, but the Conflicting Profile surfaced Delta Blues at #2 — a slow, acoustic blues song — simply because its mood is listed as "dark."

**Why this is surprising:**
A user asking for high-energy rock with dark emotions probably expects aggressive, fast music — not a slow blues track. But the system does not understand what "dark + high energy" means as a combination. It treats each feature separately and adds up the points. Delta Blues earned a mood bonus (+1.0) and a decent valence score, which pushed it ahead of more energetic songs.

**What this tells us:**
The system cannot understand contradictions. When a user's preferences conflict with each other (very high energy but very sad valence), the system does not try to balance them. It just adds up points from each feature independently, sometimes producing results that feel wrong.

---

## Comparison 3: Intense Rock vs. Missing Genre (metal)

**What changed:**
Both profiles asked for high energy and intense music. The Intense Rock profile returned Storm Runner at #1 with a score of 6.44, earning full genre and mood points. The Missing Genre profile — which asked for "metal" — returned Storm Runner at #1 too, but with a much lower score of 3.92, earning zero genre points.

**Why it makes sense:**
There are no metal songs in the catalog. So the metal user never gets the genre bonus (+1.0) for any song, no matter what. The system still finds the closest match by energy and mood, but the scores are noticeably lower across the board. The system also printed a warning: "genre 'metal' not found in catalog."

**What this tells us:**
The system is transparent about this limitation — the warning is helpful. But there is no fallback. A real recommender might say: "we don't have metal, but here are some rock songs with similar energy." This system has no concept of related or adjacent genres. Metal and rock feel similar to a human listener, but to the algorithm they are completely different words.

---

## Why Does "Gym Hero" Keep Appearing?

"Gym Hero" is a pop song with energy 0.93 — one of the highest energy values in the entire catalog. Because energy is weighted at 4.0 (the highest of any feature), any user who asks for high energy will automatically see Gym Hero ranked near the top, even if their preferred genre is rock or EDM rather than pop.

Think of it like this: if the system were a chef scoring recipes, and you said taste counts for 4 points but cuisine type only counts for 1 point — a pasta dish that tastes exactly right would always beat a sushi dish that almost tastes right, even if you asked for sushi. "Gym Hero" is the pasta dish: it nails the energy, so it keeps winning.

This is a direct result of the energy weight being set too high relative to genre and mood. Reducing the energy weight back toward 2.0 would give genre and mood more influence and reduce how often the same high-energy songs dominate multiple different profiles.

---

## Summary of Key Lessons

| Observation | What it means |
|---|---|
| Clear profiles → clear results | The system works well when preferences are simple and consistent |
| Conflicting profiles → odd results | The system cannot balance contradictions — it just adds up points |
| Missing genre → lower scores, no fallback | The system warns you but does not suggest alternatives |
| Same songs appear across profiles | High energy weight makes a few songs universally dominant |
| Tied scores are broken by CSV order | When two songs score equally, the result is effectively random |
