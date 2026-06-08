# Weekly Metrics Review

Question: should the team keep the current report checker threshold?

Data:

| Check | Passing examples | Failing fixtures | Notes |
| --- | ---: | ---: | --- |
| HTML static | 4 | 1 | catches layout and slop failures |
| JSON schema | 4 | 0 | catches malformed manifests |
| Cross-check | 4 | 1 | catches HTML/JSON drift |

Recommendation: keep all three checker layers because each catches a different failure mode.

