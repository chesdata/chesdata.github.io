#!/bin/bash
# Checks every GitHub Release download URL referenced across the CHES site's
# .md files. Run this from your repo root, or point URLFILE at any list of
# URLs, one per line.
#
# Usage:  bash check-links.sh
#
URLFILE="urls.txt"
FAIL=0
TOTAL=0

while IFS= read -r url; do
  [ -z "$url" ] && continue
  TOTAL=$((TOTAL+1))
  # -L follows the redirect GitHub issues from /releases/download/... to the
  # actual asset; -o /dev/null discards the body; -w prints just the final
  # HTTP status; -s silences the progress bar; -I would be faster (HEAD-only)
  # but GitHub's release CDN doesn't reliably support HEAD, so this uses GET
  # with a byte-range trick to avoid downloading the whole file.
  status=$(curl -sL -o /dev/null -w "%{http_code}" -r 0-0 "$url")
  if [ "$status" = "200" ] || [ "$status" = "206" ]; then
    echo "OK   $status  $url"
  else
    echo "FAIL $status  $url"
    FAIL=$((FAIL+1))
  fi
done < "$URLFILE"

echo
echo "$((TOTAL-FAIL)) / $TOTAL links OK"
if [ "$FAIL" -gt 0 ]; then
  echo "$FAIL link(s) failed -- see FAIL lines above"
fi
