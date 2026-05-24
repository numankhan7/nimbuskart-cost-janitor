# Cost Janitor - Sample Audit Report Summary

* **Scan Date:** 2026-05-24
* **Environment:** Staging (LocalStack Mock)

### Infrastructure Waste Found:
1. **Active EC2 Instances:** 2 Servers (`t3.micro`) running without cost-containment schedule.
2. **Orphaned EBS Volumes:** 1 Block Storage Volume (`gp3`, 10GB) unattached to any virtual instance.

**Action Taken:** All detected leak resources were automatically terminated/deleted via the Remediation engine loop. Total wasted burn rate reduced to $0.00.