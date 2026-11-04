# Dataset and Knowledge Governance

## Principles

Use data with a documented lawful basis and license. Record where it came from, when it was acquired, what transformations were applied, and which model or index versions consumed it. Publicly accessible data is not automatically licensed for training or redistribution.

## Dataset manifest fields

Recommended fields: `source_id`, `source_uri`, `title`, `publisher`, `license`, `license_uri`, `acquired_at`, `allowed_uses`, `language`, `content_hash`, `dedup_group`, `quality_score`, `personal_data_review`, `processing_version`, `split`, and `exclusion_reason`.

## Processing pipeline

1. Acquire only approved sources.
2. Preserve source and license metadata.
3. Normalize encodings and remove malformed records.
4. Detect exact and near duplicates.
5. Filter spam, boilerplate, and low-quality content.
6. Review personal data and sensitive content.
7. Split datasets without leakage.
8. Generate immutable manifests and hashes.
9. Track each dataset version in training experiments.
10. Support takedown/exclusion and rebuild procedures.

## Knowledge uploads

Uploaded content is treated as user-provided untrusted data. The starter stores extracted text chunks and filename metadata, not the original binary. Implement owner/tenant checks, secure object storage, upload scanning, retention rules, and complete deletion verification before multi-user use.
