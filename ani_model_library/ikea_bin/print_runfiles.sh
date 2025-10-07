#!/bin/bash
# Print locations of the staged runfiles for quick bazel run testing.
set -euo pipefail

echo "Runfiles root: ${RUNFILES_DIR:-$0.runfiles}"

# Try to print the runfiles path for the package data
if [ -n "${RUNFILES_DIR:-}" ]; then
  echo "SDF runfile:" "$RUNFILES_DIR/$(basename $(dirname $PWD))/ani_model_lib/ikea_bin/ikea_bin.sdf"
fi

echo "Listing package runfiles for this package (may vary by Bazel layout):"
ls -la "${RUNFILES_DIR:-.}"
