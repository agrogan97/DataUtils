Roomworld Analyses
===

- rise_year4_clean.csv : contains all year 4 rise data per-participant, restructured from the SQL version. This contains duplicate data.
- rise_year4_researchDeduplicated_rounds.csv : the round-level data from year 4 rise. Duplicates removed following the research structure - i.e. we keep only the first attempt, which may be complete or incomplete
- rise_year4_riseDeduplicated_rounds.csv : the round-level data from year 4 rise. Duplicates removed following the rise structure - i.e. keep the first complete type, regardless of if there were previous attempts. If no complete data, keep only the first attempt.
- rise_year4_clean_riseDeduplicated.csv : all year 4 rise data per-participant, with duplicates removed by the rise convention - i.e. keep the first complete type, regardless of if there were previous attempts. If no complete data, keep only the first attempt.
- rise_year4_clean_researchDeduplicated.csv : all year 4 rise data per-participant, with duplicates removed by the research convention - i.e. keep the first attempt, which may be complete or incomplete
- rise_year4_duplicateLabelled_rounds.csv : the round-level data from year 4 rise, with duplicate attempts labelled by the attempt number as duplicateNumber. Attempt numbers are defined in the order the first round was attempted.

rise_year4_clean
---

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| pk        | int  | Database primary key. Unique per game. |
| userId    | str  | Hashed user ID received from RISE. Long alphanumeric string. One participant may have duplicate userIds |
| rawData | dict | All raw data from the gameplay. Used for down the pipeline for extracting rounds and responses |
| sdata | dict | Data specifically related to gameplay. See round-level data. |
| edata | Obj | Not regularly required |
| parameters | Obj | Not regularly required |
| totalAttempts | int | How many overall attempt the user had, on this server id. This means restarts by closing and reopening the browser, and differs from duplicates |
| completed | boolean | Whether or not the user completed the game |
| lastCompletedRound| int | The round index the player reached before ending the game |
| lastTrialGame | int | How many trial_games they've seen |
| finalRooms | ?? | The final room each participant reached |
| urlParameters | Obj  | Not regularly required |
| timestamps | list, ints | The timestamps (epoch times) of the start times of specific attempts made with this server ID. Doesn't include RISE-side duplicates |
| timeCreated | str | Datetime of when the object was created in the database, in UCT. |
| lastModified | str | Datetime of when the object was last modified in the database, in ICT. |

rise_year4_*_rounds.csv
---

| Parameter |
| --------- |
| pk |
| id |
| iv |
| tag |
| expt_index |
| expt_trial |
| trial_layout |
| trial_level |
| trial_solved |
| trial_attempts |
| trial_game |
| trial_transfer |
| trial_test |
| round_start_time |
| round_end_time |
| last_room |
| roundAttempted |
| gameComplete |
| *duplicateLabelled only* duplicateNumber |