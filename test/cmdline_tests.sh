#!/usr/bin/env bash

# This script contains command line tests for TRTools utilities

die()
{
    BASE=$(basename "$0")
    echo "$BASE error: $1" >&2
    exit 1
}

runcmd_pass()
{
    echo "[runcmd_pass]: $1"
    bash -c "$1" >/dev/null 2>&1 || die "Error running: $1"
}

runcmd_fail()
{
    echo "[runcmd_fail]: $1"
    bash -c "$1" >/dev/null 2>&1 && die "Command should have failed: $1"
}

TMPDIR=$(mktemp -d -t tmp-XXXXXXXXXX)

echo "Saving tmp files in ${TMPDIR}"

# Check version
runcmd_pass "citrus --version"
runcmd_pass "python -c 'import citrus; print(citrus.__version__)'"
