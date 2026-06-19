# Copilot Instructions — Mergington High School Activities App

## Project context
This is a Flask REST API for managing extracurricular activities at Mergington High School.
Students use it to sign up and remove themselves from activities.

## NEVER_MODIFY — UAT-locked code
The following have passed UAT and must NOT be modified by any Copilot suggestion:

### Routes (src/app.py)
- `get_activities()` — the GET /activities route
- `signup()` — the POST /activities/{name}/signup route
- `remove_signup()` — the DELETE /activities/{name}/signup route

### Tests (src/tests/test_app.py)
- ALL existing test functions — never delete, rename, or modify
- Never reduce assertion count in any existing test

## What Copilot MAY help with
- New route functions added BELOW the existing routes
- New test functions added at the BOTTOM of test_app.py
- README and documentation updates
- requirements.txt updates

## Constraints
- Always use Flask's `jsonify()` for responses — never return raw dicts
- Always return appropriate HTTP status codes (200, 201, 404, 400)
- Never use string-formatted SQL or shell commands
- New routes must have a corresponding test before the PR is opened