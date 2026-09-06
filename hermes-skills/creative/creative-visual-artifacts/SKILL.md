---
name: creative-visual-artifacts
description: "Class-level workflow for visual artifacts: HTML mockups, architecture diagrams, Excalidraw boards, design-token docs, style-system references, and browser-based creative demos."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, design, diagrams, html, svg, excalidraw, mockups, design-systems, p5js, pretext]
---

# Creative Visual Artifacts

Use this umbrella when the user asks for a visual artifact that can be delivered as HTML/CSS/SVG/JSON or a small browser demo: landing pages, comparison mockups, architecture/cloud diagrams, Excalidraw canvases, design-token specs, design-system-inspired UI, generative sketches, or typographic/text-layout demos.

## Default workflow

1. Identify the artifact class: static mockup, diagram, hand-drawn board, token spec, style reference, or interactive/browser sketch.
2. Choose the lightest medium that satisfies delivery:
   - static comparison or landing page → standalone HTML/CSS;
   - infrastructure/system diagram → SVG-in-HTML or Excalidraw JSON;
   - hand-drawn flow/sequence/architecture board → Excalidraw JSON;
   - reusable design language → DESIGN.md token spec;
   - brand/style inspiration → draw from named design-system patterns;
   - kinetic typography/text-as-geometry → Pretext-style browser demo;
   - generative art/interactivity → p5.js.
3. Build a real artifact, not just a description. Save it to a file when useful and verify by opening or validating the output.
4. Prefer 2–3 variants for ambiguous aesthetic requests, then summarize tradeoffs.
5. Keep assets self-contained unless the user explicitly wants external dependencies.

## Labeled playbooks

### HTML product/design mockups

For one-off landing pages, dashboards, decks, or UI prototypes, create a standalone HTML file with embedded CSS. Use strong hierarchy, realistic copy, responsive layout, and a specific visual direction. Avoid generic gradient-card sameness.

### Throwaway sketch variants

When the user wants to compare directions, produce 2–3 focused variants quickly. Each variant should make a different bet (layout density, tone, navigation, visual metaphor), not merely recolor the same page.

### Architecture and system diagrams

Use SVG/HTML for crisp dark-theme architecture diagrams, clouds, networks, data flows, and infra maps. Label boundaries, protocols, failure modes, and ownership. Prefer explicit arrows and legends over decorative complexity.

### Excalidraw-style diagrams

Use Excalidraw JSON when the user wants hand-drawn architecture, flow, or sequence diagrams. Keep element grouping and IDs coherent, use consistent colors, and verify JSON validity before delivery.

### DESIGN.md token specs

Use DESIGN.md when defining design systems or token contracts. Include colors, typography, spacing, radii, motion, components, accessibility constraints, and export/validation notes.

### Popular web design references

When asked for a style like Stripe, Linear, Vercel, Notion, Apple, Raycast, etc., translate the reference into concrete decisions: layout, spacing, type scale, color, motion, borders, shadows, copy tone, and interaction details. Do not copy logos or protected assets.

### Browser creative coding

Use p5.js for generative/interacting visuals, shaders, animation, 3D/WebGL, or exportable frames. Use Pretext-style text layout when the visual is fundamentally typography, ASCII, text flow around shapes, or text-as-geometry.

## Quality bar

- Artifact opens locally without missing dependencies.
- Visual intent is obvious from the file itself.
- The implementation includes accessibility basics where applicable.
- Diagrams are readable at the likely screenshot size.
- If generated code is delivered, include run/open instructions and verify syntax or rendering where possible.

## Archived source packages

Several former narrow skills were consolidated into this umbrella. Their full packages may remain recoverable in the skills archive for historical templates, references, and scripts, but future agents should start here and only recover archived material when a subsection needs deeper examples.
