# Data

Do not commit manuscript scans or third-party transcriptions without checking their license and attribution requirements.

For each imported dataset record:

- source URL
- author/maintainer
- version/date
- transcription system (EVA, STA, etc.)
- license/usage terms
- checksum
- preprocessing performed

Suggested layout:

```
data/
  raw/
  derived/
  metadata/
```

Raw third-party data should remain unmodified. Derived data should be reproducible from scripts.
