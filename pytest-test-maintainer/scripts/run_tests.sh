#!/usr/bin/env bash
# Purpose: Run pytest with standardized modes (quick/cov/report/changed) for local development and maintenance.

set -euo pipefail

MODE="${1:-quick}"
if [[ $# -gt 0 ]]; then
  shift
fi

EXTRA_ARGS=("$@")
PYTEST_BIN="${PYTEST_BIN:-pytest}"
XDIST_WORKERS="${XDIST_WORKERS:-auto}"
COV_TARGET="${COV_TARGET:-.}"
COV_REPORT="${COV_REPORT:-term-missing}"
HTML_REPORT="${HTML_REPORT:-report.html}"

usage() {
  cat <<'USAGE'
Usage: ./scripts/run_tests.sh <mode> [pytest args...]

Modes:
  quick    Fast smoke run. Uses xdist when available.
  cov      Run with coverage and generate htmlcov/.
  report   Run with pytest-html and generate report.html.
  changed  Run tests mapped from staged/unstaged and recent committed changes.

Examples:
  ./scripts/run_tests.sh quick
  ./scripts/run_tests.sh cov -k sandbox
  ./scripts/run_tests.sh report -q
  ./scripts/run_tests.sh changed -q
USAGE
}

die() {
  echo "Error: $*" >&2
  exit 1
}

has_xdist() {
  "$PYTEST_BIN" --help 2>/dev/null | grep -q -- "--numprocesses"
}

has_cov() {
  "$PYTEST_BIN" --help 2>/dev/null | grep -q -- "--cov"
}

has_html() {
  "$PYTEST_BIN" --help 2>/dev/null | grep -q -- "--html"
}

run_pytest() {
  if has_xdist; then
    "$PYTEST_BIN" -n "$XDIST_WORKERS" "$@"
  else
    "$PYTEST_BIN" "$@"
  fi
}

collect_changed_files() {
  {
    git diff --name-only --diff-filter=ACMR 2>/dev/null || true
    git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true
    if git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
      git diff --name-only --diff-filter=ACMR HEAD~1..HEAD 2>/dev/null || true
    fi
  } | sed '/^[[:space:]]*$/d' | sort -u
}

map_changed_tests() {
  local changed_files
  local file
  local noext
  local stem
  local candidates=""

  changed_files="$(collect_changed_files)"
  [[ -z "$changed_files" ]] && return 0

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue

    case "$file" in
      tests/*.py|test_*.py|*_test.py)
        candidates+="$file"$'\n'
        ;;
    esac

    [[ "$file" != *.py ]] && continue

    noext="${file%.py}"
    stem="$(basename "$noext")"

    if [[ -d tests ]]; then
      candidates+="tests/test_${stem}.py"$'\n'
      candidates+="tests/${noext}_test.py"$'\n'
      candidates+="tests/${noext}.py"$'\n'

      while IFS= read -r found; do
        [[ -n "$found" ]] && candidates+="$found"$'\n'
      done < <(find tests -type f \( -name "test_${stem}.py" -o -name "${stem}_test.py" \) 2>/dev/null)
    fi
  done <<< "$changed_files"

  printf "%s" "$candidates" | sed '/^[[:space:]]*$/d' | awk '!seen[$0]++' | while IFS= read -r p; do
    [[ -f "$p" ]] && printf "%s\n" "$p"
  done
}

if git rev-parse --show-toplevel >/dev/null 2>&1; then
  cd "$(git rev-parse --show-toplevel)"
fi

case "$MODE" in
  quick)
    run_pytest "${EXTRA_ARGS[@]}"
    ;;
  cov)
    has_cov || die "pytest-cov is required for 'cov' mode. Install pytest-cov first."
    run_pytest --cov="$COV_TARGET" --cov-report="$COV_REPORT" --cov-report=html "${EXTRA_ARGS[@]}"
    ;;
  report)
    has_html || die "pytest-html is required for 'report' mode. Install pytest-html first."
    run_pytest --html="$HTML_REPORT" --self-contained-html "${EXTRA_ARGS[@]}"
    ;;
  changed)
    targets=()
    while IFS= read -r t; do
      [[ -n "$t" ]] && targets+=("$t")
    done < <(map_changed_tests)

    if [[ ${#targets[@]} -eq 0 ]]; then
      echo "No mapped changed tests found, fallback to full quick run." >&2
      run_pytest "${EXTRA_ARGS[@]}"
    else
      echo "Running mapped tests:" >&2
      printf ' - %s\n' "${targets[@]}" >&2
      run_pytest "${targets[@]}" "${EXTRA_ARGS[@]}"
    fi
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage
    die "unknown mode: $MODE"
    ;;
esac
