# Design Note: Enterprise Cost Janitor Architecture & Safety Net

## 1. Multi-Cloud Reality & Extensibility Architecture

To prevent core rewrites when adding Google Cloud Platform (GCP) or Azure next quarter, the Janitor is structured using the **Provider Factory Pattern** and clean interface isolation. The core orchestration framework interacts strictly with abstract interfaces, decoupling business logic (cost thresholding, tag scanning) from underlying cloud SDK components (`boto3`, `google-cloud-storage`, etc.).

               ┌──────────────────────────────┐
               │   janitor_orchestrator.py    │
               └──────────────┬───────────────┘
                              │ Uses Abstract Interface
                              ▼
               ┌──────────────────────────────┐
               │    BaseCloudProvider (Interface)  │
               └──────────────┬───────────────┘
      ┌───────────────────────┼───────────────────────┐
      ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ AWSProvider      │    │ GCPProvider      │    │ AzureProvider    │
│ (Boto3 Engine)   │    │ (Google SDK)     │    │ (Azure SDK)      │
└──────────────────┘    └──────────────────┘    └──────────────────┘


### Module Boundaries & Directory Layout Blueprint
```text
janitor/
├── janitor_orchestrator.py  # Core Engine: Controls scan loops and report logic
├── providers/
│   ├── __init__.py          # Factory class exporter
│   ├── base_provider.py     # Defines Abstract Base Classes (ABC)
│   ├── aws_provider.py      # AWS Specific discovery and teardown (Current Boto3 code)
│   └── gcp_provider.py      # GCP Specific discovery (Compute Engine & GCS buckets)