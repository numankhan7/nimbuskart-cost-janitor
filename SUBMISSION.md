# Submission — DevOps Engineer Assignment 
  
**Candidate name:** Numan Khan
**Email:** numaankhan286@gmail.com
**Date submitted:** May 24, 2026
**Hours spent (approximate):** 7 Hours
  
## Deliverables checklist
- [x] Part A: Terraform code under /terraform applies cleanly on LocalStack
- [x] Part A: `terraform validate` and `terraform fmt -check` both pass
- [x] Part B: Janitor script runs in --dry-run mode and produces report.json
- [x] Part B: GitHub Actions workflow runs green on a fresh PR
- [x] Part B: --delete mode respects Protected=true tag
- [x] Part C: DESIGN.md is present and within 2 pages
- [x] Walkthrough video link below is accessible (unlisted is fine) 
  
## Walkthrough video 
Link (Loom / YouTube unlisted / Google Drive):https://www.loom.com/share/eea6e4205e1d42e99aacf596145a6038
Length: max 5 minutes 
  
## Sample report 
Path to a sample report.json produced by your script: cost_leaks_report.json
  
## Known limitations 
* LocalStack community core engine S3 lifecycle hook deadlock limits (Bypassed S3 creation natively to maintain execution stability for core assignment criteria).
* Script currently parses timezone context via local native machine time offsets rather than centralized NTP system logs.
  
## AI usage disclosure 
* **Which tools you used and roughly for what:** Utilized ChatGPT/Gemini to clean Python 3.14 datetime deprecation warnings and debug Docker network container endpoints for LocalStack mapping.
* **One specific thing the AI got wrong or suggested badly, and how you noticed:** The AI initially suggested using raw `datetime.utcnow()` which threw a critical deprecation trace warning in the modern Python environment. Noticed via local terminal stack traces and manually resolved using explicit `timezone.utc` objects.
* **One section of the code you wrote without AI help — and why you chose to do that part manually:** Wrote the custom validation loops and assertion checks inside `test_cost_janitor.py` manually to precisely isolate client endpoints based on custom environment variable overrides (`TEST_MODE`) without relying on generalized AI-generated testing templates.