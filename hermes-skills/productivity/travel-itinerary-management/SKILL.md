---
name: travel-itinerary-management
description: "Use when planning and maintaining a multi-day personal trip."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [travel, itinerary, planning, obsidian, logistics]
---

# Travel Itinerary Management

Use when a user wants an actionable multi-day trip plan, especially when it evolves through voice notes, maps lists, shared links, booking details, or an Obsidian trip note.

## Principles

- Treat the itinerary as a **living draft**, not a fixed schedule, until the user confirms bookings and event timing.
- Prioritize immutable constraints first: flight times, accommodation bases and addresses, car pickup/drop-off, ceremonies/events, and booked activities.
- Build every flexible day around the user's stated priority (for example beach time, food, museums, hiking), then add at most one optional complement.
- Never retain a conflicting earlier suggestion after the user clarifies a time or location. Update both the summary table and the affected day section.
- Keep transfer days intentionally lighter. Do not combine multiple major stops simply because they are geographically nearby; recommend a primary stop and make the rest optional.

## Workflow

1. **Orient in the existing trip folder before planning.** Resolve and validate `OBSIDIAN_VAULT_PATH` through `local-knowledge-workbench`, then discover the existing travel/trip directory; `Viaggi/<TripName>/` is an example, not a required layout. Inventory the main itinerary, integrated guides/comparisons, dedicated notes, and `raw/` sources before creating anything. Preserve established filenames and update existing notes instead of creating parallel versions.
2. **Collect and normalize fixed details.** Capture dates, flights, transportation, overnight bases, hotel choice/address, bookings, event times/locations, explicit exclusions, and hard priorities. Correct transcription errors before designing around them. Evaluate a hotel against the actual itinerary, transfers, evening returns, and nearby food—not as a generic neighborhood.
3. **Map bases and transfer legs.** Assign each overnight to a base and put on-route stops only on the relevant transfer day.
4. **Draft a constraint-first itinerary.** Give each day one primary activity, one optional complement, and a calm fallback. Protect mornings before formal events and departure days.
5. **Ingest sources selectively.** Inspect the original source directly; save concise provenance under the trip's `raw/` folder when building a durable vault; for videos default to a structured operational summary rather than a transcript; extract only ideas compatible with dates, bases, pace, and priorities; label commercial sources as inspiration; explain useful exclusions.
6. **Maintain single sources of truth.** Use dedicated notes for restaurants, packing, bookings, or source summaries; keep only a synopsis and wikilink in the general guide. When a fact changes, update every active occurrence and remove superseded values. Verify every write by reading it back.
7. **Build packing lists from the real trip.** Read dates, baggage allowance, activities, laundry access, willingness to rewear, trekking/city/evening mix, weather, and owned equipment before assigning quantities; never assume one outfit per calendar day.
8. **Replan live travel days.** Re-read the latest itinerary and confirmed constraints, use current opening/transport/weather facts when relevant, preserve booked anchors, and clearly label what changed versus the stored plan.
9. **Offer a forwarding-ready summary on request.** Include dates, bases, anchor plans, and only logistics the recipient needs; omit internal checklists unless they affect a decision.

## Obsidian trip-note pattern

The following Italian folder names and headings illustrate one vault convention; follow the destination vault's existing layout and language rather than creating these paths unconditionally.

- Place the main plan at `Viaggi/<TripName>/<TripName>.md` (or match the vault's established convention).
- Keep source captures in `Viaggi/<TripName>/raw/` and link them from a compact `## Fonti di ispirazione` section.
- Preserve a `## Logistica da confermare` checklist, but remove an item as soon as the user supplies the fact.
- Record a source's ideas in your own words; do not mirror marketing copy or long source text.

## Common pitfalls

- **Arrival-day overload:** flights, baggage, car collection, and a long drive often eliminate the value of a distant scenic detour.
- **Transfer-day overload:** beach, town visit, lunch, check-in, and another city can sound compact but feel rushed. Make one stop the commitment.
- **Event duplication:** if a place is already covered by a wedding or other fixed event, do not schedule it again as a casual sightseeing evening without the user asking.
- **Stale logistics:** flight-time corrections must update both the top-level table and the departure/arrival day, including the recommended airport buffer.
- **Source gravity:** do not let a polished group-tour page pull the user into geographically incoherent extras; assess each stop against the actual trip.

## Verification

- Re-read the entire modified itinerary note or all changed sections after updates.
- Check that every fixed fact appears consistently in the summary table and daily plan.
- When a source was saved, confirm both the source-note path and the wikilink/reference from the main itinerary.
- Before sharing a summary, make sure it reflects the latest user correction and contains no superseded timing or duplicate stop.
- When the user specifies a count or geographic subdivision—such as “top 5 per city”—preserve the unit and verify the resulting count independently for every area.

## Reference

See [references/constraint-first-itineraries.md](references/constraint-first-itineraries.md) for a compact example of conflict resolution and source triage.