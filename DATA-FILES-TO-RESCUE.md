# Data files to pull off Squarespace before you cancel it

Every `.file` link on the data pages currently points at the GitHub Releases
landing page as a placeholder. The real files are still on Squarespace at the
URLs below. **These die when the Squarespace subscription ends**, so download
them now, attach them to a GitHub Release, then replace the placeholder `href`s.

Captured from chesdata.eu on 4 August 2026. Verify each one still resolves
before you rely on this list.

## CHES-Latin America 2020 — from /chesla
- https://www.chesdata.eu/s/ches_la_2020_aggregate_level_v01.dta
- https://www.chesdata.eu/s/ches_la_2020_aggregate_level_v01.rds
- https://www.chesdata.eu/s/ches_la_2020_aggregate_level_v01.csv
- https://www.chesdata.eu/s/ches_la_2020_expert_level_v01.dta
- https://www.chesdata.eu/s/ches_la_2020_expert_level_v01.rds
- https://www.chesdata.eu/s/ches_la_2020_expert_level_v01.csv
- https://www.chesdata.eu/s/2020_ches_la_codebook.pdf
- https://www.chesdata.eu/s/2020_ches_la_questionnaire_english.pdf
- https://www.chesdata.eu/s/2020_ches_la_questionnaire_spanish.pdf
- https://www.chesdata.eu/s/2020_ches_la_questionnaire_portuguese.pdf

## CHES-Israel 2021/2022 — from /chesisrael
- https://www.chesdata.eu/s/CHES_ISRAEL_means_2021_2022.dta
- https://www.chesdata.eu/s/CHES_ISRAEL_means_2021_2022.csv
- https://www.chesdata.eu/s/CHES_ISRAEL_expert_level_2021_2022.dta
- https://www.chesdata.eu/s/CHES_ISRAEL_expert_level_2021_2022.csv
- https://www.chesdata.eu/s/CHES_ISR_Codebook.pdf
- https://www.chesdata.eu/s/Qualtrics-Survey-Israel2022.pdf

## CHES-Canada 2023 — from /chescanada
- https://www.chesdata.eu/s/CHES_CA2023.dta
- https://www.chesdata.eu/s/CHES_CA2023.csv
- https://www.chesdata.eu/s/CHES_CA2023_expert-level.dta
- https://www.chesdata.eu/s/CHES_CA2023_expert-level.csv
- https://www.chesdata.eu/s/CHES_CA2023_Codebook.pdf

## Still to capture
I haven't listed the CHES-Europe or SPEED-CHES file URLs — those pages weren't
fetched in full. The same `/s/FILENAME` pattern applies, and the pages are:

- /ches-europe, /1999-2019chestrend, /2024-chapel-hill-expert-survey-ches
- /2019-chapel-hill-expert-survey, /2017-chapel-hill-expert-survey
- /2014-chapel-hill-expert-survey, /2002-chapel-hill-expert-survey
- /speedches

A quick way to grab everything at once, run from the repo root:

```
wget -r -l2 -H -D www.chesdata.eu,chesdata.eu \
     -A dta,csv,rds,pdf,sav,zip -nd -P rescued/ https://www.chesdata.eu/
```

Check what it collected before trusting it — `wget` mirroring against
Squarespace is hit and miss.
