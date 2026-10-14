#!/usr/bin/env bash
# Load test script for TaskBoard HPA demonstration
# Usage: ./scripts/load-test.sh [BASE_URL] [DURATION_SECONDS]
#
# Example:
#   ./scripts/load-test.sh http://localhost:8000 60

BASE_URL="${1:-http://localhost:8000}"
DURATION="${2:-60}"
CONCURRENCY=10

echo "=== TaskBoard Load Test ==="
echo "Target: $BASE_URL"
echo "Duration: ${DURATION}s"
echo "Concurrency: $CONCURRENCY"
echo ""

if command -v hey &>/dev/null; then
  echo "[+] Using hey for load test..."
  hey -z "${DURATION}s" -c "$CONCURRENCY" "${BASE_URL}/api/tasks"
elif command -v ab &>/dev/null; then
  echo "[+] Using Apache Bench..."
  REQUESTS=$((CONCURRENCY * DURATION * 5))
  ab -n "$REQUESTS" -c "$CONCURRENCY" "${BASE_URL}/api/tasks"
else
  echo "[+] Using curl loop (install 'hey' for better results)..."
  END=$((SECONDS + DURATION))
  COUNT=0
  while [ $SECONDS -lt $END ]; do
    curl -s "${BASE_URL}/api/tasks" > /dev/null &
    curl -s "${BASE_URL}/health" > /dev/null &
    COUNT=$((COUNT + 2))
    sleep 0.1
  done
  wait
  echo "Sent approximately $COUNT requests"
fi

echo ""
echo "=== Load test complete ==="
echo "Check HPA: kubectl get hpa -n taskboard"
