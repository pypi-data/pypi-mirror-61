#! /usr/bin/env bash
protoc -I=proto --python_out=. proto/*.proto
sed -i -E 's/^import.*_pb2/from . \0/' *.py
