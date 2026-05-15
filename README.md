APP PURPOSE:

✔ core
Authentication, roles, permissions, home page, demo data.

✔ meets
Teams, entries, meet setup, meet editing, meet dashboards.

✔ judging
Judge score sheets, judge dashboards, judge entry UI.

✔ kct
Kick count, timing, jazz skill confirmations, dangerous moves.

✔ superior
Superior judge issue resolution, DQ workflow, review screens.

✔ tabulation
Scoring engine, ranking, meet results, public results, announcer results.

✔ mshsl_dance
Project settings, root URLs, WSGI/ASGI.



APP STRUCTURE:

judging/
├── admin.py
├── forms.py
├── helpers.py
├── models/
│   └── judge_score_sheet.py
├── scoring.py
├── signals.py
├── templates/judging/
│   ├── compare_judges.html
│   ├── dashboard.html
│   ├── judge_score_entry.html
│   └── view_score_sheets.html
├── urls.py
└── views/
    ├── dashboard.py
    └── view_score_sheets.py

kct/
├── admin.py
├── forms.py
├── models.py
├── templates/kct/
│   ├── dangerous_move.html
│   ├── dashboard.html
│   ├── entry.html
│   └── kct_entry.html
├── urls.py
└── views/
    ├── dangerous_move.py
    ├── dashboard.py
    ├── entry.py
    └── save_kct.py

tabulation/
├── models.py
├── services/
│   ├── apply_kct_to_scores.py
│   ├── kct_deductions.py
│   ├── ranking.py
│   └── tiebreakers.py
├── templates/tabulation/
│   ├── announcer_results.html
│   ├── dashboard.html
│   ├── judge_recap.html
│   ├── meet_overview.html
│   ├── meet_results.html
│   ├── public_results.html
│   ├── public_results_pdf.html
│   └── tabulator_verify.html
└── views/
    ├── announcer.py
    ├── dashboard.py
    ├── judge_recap.py
    ├── lock_meet.py
    ├── meet_overview.py
    ├── public_results.py
    ├── reorder_entries.py
    ├── results.py
    ├── results_pdf.py
    └── verify.py

superior/
├── issue_factory.py
├── models.py
├── templates/superior/
│   ├── create_dq.html
│   ├── dashboard.html
│   ├── resolve_issue.html
│   └── review.html
└── views/
    ├── dashboard.py
    ├── dq_actions.py
    ├── issue_actions.py
    └── review.py

meets/
├── models/
│   ├── entry.py
│   ├── meet.py
│   ├── ruleset.py
│   └── team.py
├── ranking.py
├── templates/meets/
│   ├── add_entry.html
│   ├── add_team.html
│   ├── edit_entry.html
│   ├── entry_inline_form.html
│   ├── meet_setup.html
│   ├── summary.html
│   └── tabulator_dashboard.html
└── views/
    ├── add_team_inline.py
    ├── delete_entry.py
    ├── edit_entry.py
    ├── entry.py
    ├── setup.py
    └── team.py
