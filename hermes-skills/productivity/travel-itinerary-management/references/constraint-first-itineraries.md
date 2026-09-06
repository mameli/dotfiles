# Constraint-first itinerary maintenance

## Minimal fixed-details matrix

| Field | Why it is an anchor | Where it must appear |
|---|---|---|
| Flight number/times and airports | Determines realistic arrival/departure windows | Fixed-details table and the relevant first/last day |
| Rental-car pickup/drop-off | Adds time and location constraints | Arrival/departure day and checklist |
| Accommodation address and nights | Defines the daily radius and transfer route | Fixed-details table and each base transition |
| Formal event time/place | Blocks a portion of the day and often requires preparation time | Fixed-details table and event day |
| Priority (beach, food, culture, hiking) | Determines how much discretionary activity is appropriate | Every flexible-day recommendation |

## Conflict-resolution examples

### Arrival time corrects an assumed midday arrival

**Before:** airport arrival → nature reserve → coastal town → late check-in.

**After a late-afternoon arrival:** airport arrival → car pickup → accommodation → local dinner. Move the nature reserve to the later transfer day where it sits naturally on route.

### The user wants a specific town during a transfer

Do not add it alongside every other nearby attraction. Keep the day as:

1. one primary beach/nature stop;
2. the requested town for a walk, aperitivo, or early dinner;
3. destination check-in.

Demote another city to optional, rather than presenting all locations as equally feasible.

### A formal event is in a town already suggested for leisure

Remove the duplicate leisure stop on another day unless there is a distinct purpose. The event will already give the user exposure to the place and has a non-negotiable preparation window.

## Source triage for travel-operator pages

Keep only ideas that meet all three tests:

- **Route fit:** compatible with the booked bases and transfers.
- **Pace fit:** leaves enough beach/rest time for the user's priorities.
- **Evidence fit:** does not rely on the operator's unspecified or group-only logistics.

Useful output is a compact source note: URL, capture date, short summary, adopted ideas, excluded ideas, and a quality flag such as “commercial inspiration; re-check practical details locally.”

## Forwarding summary template

```md
**Trip name and dates**

**Day/date**
One or two sentences: base, anchor plan, and the one main flexible idea.

…

**In sintesi:** [trip rhythm, bases, and overall emphasis].
```

Keep it personable and decisive. Exclude internal logistics/checklists, alternatives that do not need a decision, and provenance details.