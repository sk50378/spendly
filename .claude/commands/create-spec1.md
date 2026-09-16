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

## Step 1- Research the codebase
Read the files before writing the spec:
- claude