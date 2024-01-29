Pointer Analyses
===

- pointerPilotRounds.csv : The pilot data from lab participants Oxford 2024

pointerPilot.csv
---

| Parameter | Description |
| --------- | ----------- |
| UserId | Unique participant ID |
| RawData | The raw game data. See round-level data CSV |
| Source | The source of the data, for filtering out pilot participants |
| platformData | Contains lists of the debrief questions |
| Metadata | Not used in study data, but contains a copy of the UID |
| timeCreated | Datetime of when the object was created in the database, in UCT. |
| lastModified | Datetime of when the object was last modified in the database, in ICT. |

pointerPilotRounds.csv
---

| Parameter | Description |
| --------- | ----------- |
| userId    | Unique Participant ID |
| source    | The source of the data, for filtering out pilot participants |
| resp      | Dictionary of response values per round |
| level     | Can ignore, only relevant for a 1D curriculum |
| score     | Player starting score |
| layout    | The layout configuration for this round, containing information on node positions, difficulty levels, etc. |
| target    | The target score |
| endTime   | Epoch time for the end of the round |
| layoutId  | The ID of the layout in the database |
| playerIx  | Variable that tracks the player index during gameplay |
| completed | If the round was completed successfully |
| roundType | The type of round this is, out of train, test, transfer |
| startTime | Epoch time for start of the round |
| attemptNum | Indicates whether the player has restart the round, if restarts are enabled |
| numCorrect | Indicates how many rounds the player has gotten correct so far |
| roundIndex | The pure index of this round in terms of absolute levels, doesn't factor in restarts. |
| scoreTally | A list of how the player's score changes over the course of the round |
| trainingNum | Deprecated |
| globalRoundNum | A counter of round index that does take into account restarts |
| numCorrectPerLevel | For certain curriculum types, tracks how many rounds in a row have been successfully completed |
| gameNum | The index of the overall attempt number (the player can return to Pointer, which attempt is this) |