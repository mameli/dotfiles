---
name: productivity-integrations
description: "Class-level workflow for productivity SaaS and document integrations: Google Workspace, Notion, Airtable, PowerPoint, maps/geocoding, and Teams meeting pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, google-workspace, notion, airtable, powerpoint, maps, teams, documents, api]
---

# Productivity Integrations

Use this umbrella when operating external productivity systems or local document workflows: Google Workspace, Notion, Airtable, PowerPoint decks, geocoding/routes/timezones, and Teams meeting summary pipelines.

## Default workflow

1. Identify the system of record and operation: read, search, create, update, export, summarize, or automate.
2. Check authentication/environment before making API calls.
3. Prefer API/CLI calls over browser automation when available.
4. Fetch current state before modifying anything.
5. After writes, read back or verify by ID/path/URL.
6. Report exact object IDs/URLs/paths and any partial failures.

## Labeled playbooks

### Google Workspace

Use gws/Python/API workflows for Gmail, Calendar, Drive, Docs, and Sheets. Be precise with search syntax, scopes, file IDs, and date ranges. For writes, verify the resulting doc/sheet/event.

### Notion

Use Notion API or CLI for pages, databases, markdown conversion, block operations, and Worker-backed automations. Respect database schemas and preserve page hierarchy.

### Airtable

Use REST API operations for bases, tables, records, filtering, pagination, upserts, and attachments. Handle formula escaping and verify returned record IDs.

### PowerPoint and Office files

Use local scripts/libraries for creating, reading, editing, cleaning, and validating `.pptx` decks. Preserve slide masters/layouts when possible; verify the deck opens or passes structural checks.

### Maps and geodata

Use OSM/Nominatim/OSRM-style tooling for geocoding, points of interest, routes, distances, and timezones. Include coordinates and source caveats; do not overclaim precision.

### Teams meeting pipeline

Use pipeline commands to summarize meetings, inspect status, replay jobs, and manage Microsoft Graph subscriptions. Verify generated summaries/reports and subscription state.

## Safety and verification

- Never assume a cloud write succeeded; read back the object.
- For destructive operations, confirm target scope unless the user explicitly asked.
- Keep credentials out of outputs.
- For documents/decks, provide file path or share URL and summarize changes.

## Archived source packages

Former app-specific productivity skills were consolidated here. Archived packages retain deep API references and scripts for recovery when a task requires exact historical implementation details.
