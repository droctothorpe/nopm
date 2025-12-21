---
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh pr comment:*), Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr list:*), Bash(mkdir:*)
description: Command for automating performance management based on GitHub activity; supports --user, --name, and --start-date arguments.
model: claude-haiku-4-5
---

The arguments to this command will be a set of keyword arguments including:

- user: The GitHub user to generate a report for.
- start_date: The start date to filter PRs by.
- name: The name of the person to generate a report for.

For example:

```
--user=foo --name="John Smith" --start-date="01/01/2025"
```

Generate a report that positively summarizes the impact of the specified GitHub user. If --start-date is passed, filter to only include PRs after and including the specified date. The outputs should be saved to `nopm-output/` and should include the following:

1. A markdown file.
2. A docx file based on the markdown file.

The markdown file should adhere to the following format:

# <name> Performance Report
#### <start-date (MM/DD/YYYY)> - <current-date (MM/DD/YYYY)>

## Summary

<!-- A high level summary of the work done by the specified GitHub user. It should be positive and effusive. Highlight the scope, breadth, range, complexity, and impact of the user's contributions.-->

## PRs

Total: <exact total merged PR count>

<!-- A COMPLETE list of the PRs that the specified GitHub user has made from the specified start-date to the present, including the title, URL, and a short description of the PR. This can be an html table. Only include merged PRs.-->

## Commits

Total: <exact total commit count>>

<!-- A COMPLETE list of the commits that the specified GitHub user has made from the specified start-date to the present. This should just include links to the commits. -->

## Involved

Total: <total_involved_in>

<!-- A COMPLETE list of the PRs and issues that the specified GitHub user has been involved in from the specified start date to the present. This should just include links to the specified issues or PR. -->



