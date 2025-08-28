#!/bin/bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GH_TOKEN" \
  https://api.github.com/repos/mathpferreira/ranking-gta/actions/workflows/update_ranking.yml/dispatches \
  -d '{"ref":"main"}'
