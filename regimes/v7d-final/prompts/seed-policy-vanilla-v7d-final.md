Classify the GitHub issue or pull request for OpenClaw maintainer-interest routing.

Use only the supplied GitHub context and the fixed topic taxonomy. Choose labels by central
maintainer-owned changed surface, not by keyword match, file path, PR label, test name,
package name, affected component name, or incidental implementation detail.

## Decision Procedure

Ask what behavior, contract, artifact, lifecycle, integration, operator-visible setting,
or user-facing surface would require maintainer ownership if the item lands. Select that
surface's topic only when the item changes that surface's own contract or acceptance
condition.

Use title and main problem or feature statement first. Use body, comments, labels, changed
files, and diff as supporting evidence, not as independent label triggers.

## Cardinality Rules

Return 1-3 topics in priority order, primary changed surface first. Do not pad.
Include a secondary or tertiary topic when a separate maintainer-owned surface is explicitly
changed and has its own acceptance condition. Do not collapse a clearly multi-surface item to
one broad label when multiple central owners are explicit.

Return an empty list only when no allowed topic centrally applies.

## Boundary Rules

Add a secondary label only for its own changed contract, not because that surface merely
transports, hosts, logs, tests, documents, configures, schedules, or implements another
change. Prefer the most specific central owner over a generic product or infrastructure label.

Be conservative about false positives, but do not require an easy-row confidence threshold
before adding a clearly central co-label. Preserve all central qualifying labels within the
3-label cap.

## Output

Return only the required output format. Do not include rationale or prose outside that format.
