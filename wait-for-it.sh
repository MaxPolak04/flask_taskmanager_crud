#!/bin/bash

HOST=$1
PORT=$2
shift 2
CMD="$@"

echo "⏱️ Checking availability $HOST:$PORT..."

for i in {1..30}; do
    nc -z "$HOST" "$PORT" && break
    echo "⏳ $HOST:$PORT is not available, waiting..."
    sleep 1
done

if ! nc -z "$HOST" "$PORT"; then
    echo "❌ Timeout: no connection to $HOST:$PORT"
    exit 1
fi

echo "✅ connection to $HOST:$PORT established."

echo "🔧 Executes: $CMD"
exec $CMD
