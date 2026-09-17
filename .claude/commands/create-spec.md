---
description: Create a spec file for the next Spendly feature
argument-hint: "Step number and feature name e.g. 2 registration"
allowed-tools: Read,Write,Glob
---

You are a senior developer planning a new feature for spendly expense tracker. Always follows the rules in CLAUDE.md

User input: $ARGUMENTS

## Step 1- Parse the arguments
From $ARGUMENTS extract:

1. `step_number` - zero padded to 2 digits: 2->02, 11->11
2. `feature_title` - human readable title in Title Case 
                   -Example: "Registration" or "Login and Logout"
3. `feature-slug` - file safe slug
                  - Lowercase, kebab-case
                  - Only a-z, 0-9 and -
                  - Maximum 40 characters
                  - Example: registration, login-logout

If you cannot infer these from $ARGUMENTS, ask the user to clarify before proceeding. 

## Step 2- Research the codebase
Read the files before writing the spec:
- CLAUDE.md - roadmap,conventions,, schema
- app.py - existing routes and structure
- database/db.py -existing schemas and functions
- All files in .claude/specs/ -avoid duplicate existing specs

 
## Step 3- Write the spec
Generate a spec document with this existing structure

# Spec: <feature_title>

## Overview
One paragraph describing what this feature does and why it exists at this stage of Spendly roadmap.

## Depends on
Which previous steps this feature requires to be completed. 

## Routes
Every new route needed:
- METHOD /path -description  -access level (public/logged-in)

## Database changes
Any new table,column or constraint is needed.
Always veify against the database/db.py before writing this. 
If none, state "No Database changes".

## Templates
- Create: list new templates with their path
- Modify: list existing templates and what changes

## Files to change
Every file that  will be modified.

## Files to create
Every new file that will be created

## New Dependencies
Any new pip package. If none: state "No new dependencies".

## Rules to implementation
Specific constraints Claude must follow.
Always include:
- No SQLAlchemy or ORMs
- Parameterised queris only
- Password hashed with werkzeug
- Use CSS variables -never hard code hex values
- All templates extends base.html

## Defination of done
A specific testable checklist. Each item must be something that can be verified by running the app.

## Step 4. -Save the spec
Save to: .claude/specs/<step_number>-<feature_slug>.md

## Step 5. -Report to the user.
Print a short summary in this exact format:

Spec file: .claude/specs/<step_number>-<feature_slug>.md
Title: <feature_title>

Then tell the user:
"Review the spec at .claude/specs/<step_number>-<feature_slug>.md, then enter the plan mode with Shift+Tab twice to begin implementation.

Do not print the full spec in chat unless explicitly asked.