#!/usr/bin/env sh
# ~5 минут. Ошибки только: (1) нет flat_id -> 422, (2) тело не dict -> 422.

start=$(date +%s)
deadline=$((start + 300))  # 5 минут
i=1

while :; do
  now=$(date +%s)
  [ "$now" -ge "$deadline" ] && break

  flat_id=$((345000 + i))

  # базовые корректные фичи
  x000=$(( (i*7)  % 500 ))
  x001=$(( (i*11) % 20 ))
  x003=$(( (i*13) % 30 ))
  x005=$(( (i*17) % 40 ))
  x007=$(( (i*19) % 100 ))
  x009=$(( (i*23) % 1000 ))
  x012=$(( (i*29) % 15 ))
  x017=$(( (i*31) % 2 ))
  x019=$(( (i*37) % 2 ))
  x023=$(( (i*41) % 3 ))

  good_payload=$(printf '{"x000": %s, "x001": %s, "x003": %s, "x005": %s, "x007": %s, "x009": %s, "x012": %s, "x017": %s, "x019": %s, "x023": %s}' \
    "$x000" "$x001" "$x003" "$x005" "$x007" "$x009" "$x012" "$x017" "$x019" "$x023")

  mode="ok"
  url="http://localhost:1702/howmuch/?flat_id=$flat_id"
  body="$good_payload"

  # Только две ошибки:
  # 1) каждый 10-й запрос — без flat_id => 422
  if [ $((i % 10)) -eq 0 ]; then
    mode="no_flat_id_422"
    url="http://localhost:1702/howmuch/"
  # 2) каждый 15-й запрос — тело не dict => 422
  elif [ $((i % 15)) -eq 0 ]; then
    mode="bad_body_type_422"
    body='"not a dict"'
  fi

  t=$((now - start))
  printf 't=%03ss req=%04d flat_id=%d [%s] ... ' "$t" "$i" "$flat_id" "$mode"
  curl -sS -o /dev/null -w 'code=%{http_code} time=%{time_total}s size=%{size_download}B\n' \
    -X POST "$url" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d "$body"

  sleep 1
  i=$((i+1))
done
