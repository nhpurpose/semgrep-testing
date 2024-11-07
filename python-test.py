name: Semgrep Python Scan

on:
  # Scan changed files in PRs
  pull_request:
    paths:
      - '**.py'
  # Allow manual triggering
  workflow_dispatch: {}
  # Scan mainline branches
  push:
    branches: ["master", "main"]
    paths:
      - '**.py'
  # Regular scheduled scans (at a randomized time)
  schedule:
    - cron: '42 15 * * *'  # 15:42 UTC every day - randomized as recommended

jobs:
  semgrep:
    name: semgrep/python-scan
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep
    
    # Skip dependabot PRs
    if: (github.actor != 'dependabot[bot]')

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v42
        with:
          files: |
            **.py

      - name: Run Semgrep scan
        if: steps.changed-files.outputs.any_changed == 'true' || github.event_name != 'pull_request'
        run: |
          semgrep scan \
            --config "auto" \
            --config "p/python" \
            --config "p/security-audit" \
            --config "p/owasp-top-ten" \
            --severity ERROR \
            --max-target-bytes 10000000