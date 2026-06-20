# v7k Clean Reflection ASI

v7k keeps the established data split, row-soft-exact scoring, and editable
component layout, but removes historical run vocabulary from the task prompt and static reflection
ASI.

Key changes:

- self-contained local copies of all prompt assets and schema;
- merged topic list and definitions, avoiding a duplicate bare topic list;
- neutral task-facing headings;
- cleaned routing policy with no generation/adjudication, easy-row, or vanilla wording;
- cleaned static ASI that states the scoring and edit contract without regime history;
- one combined 20000 character budget across editable components.

Default run shape: row-wise, compact feedback, minibatch 30, hybrid frontier, strict improvement,
2400 max metric calls, parallel 8.
