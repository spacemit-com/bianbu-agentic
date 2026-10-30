#!/usr/bin/env bash
# Helper for working with the bianbu-agentic submodules.
#
#   ./scripts/submodules.sh init      # register URLs and clone every component
#   ./scripts/submodules.sh update    # fast-forward to the commits pinned here
#   ./scripts/submodules.sh sync [p]  # move to the tracked branch head (all, or path p)
#   ./scripts/submodules.sh status    # pinned commit / branch / dirty state
#   ./scripts/submodules.sh check     # compare pins with the remote branch head
#   ./scripts/submodules.sh list      # print submodule paths
#   ./scripts/submodules.sh foreach CMD

set -euo pipefail

root=$(git rev-parse --show-toplevel)
cd "$root"

usage() {
	sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
	exit "${1:-0}"
}

paths() {
	git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | sort
}

cmd=${1:-help}
[ $# -gt 0 ] && shift

case "$cmd" in
init)
	git submodule sync --recursive
	git submodule update --init --recursive
	;;
update)
	git submodule update --init --recursive
	;;
sync)
	git submodule sync --recursive
	if [ $# -gt 0 ]; then
		git submodule update --init --recursive --remote -- "$@"
	else
		git submodule update --init --recursive --remote
	fi
	;;
status)
	git submodule status --recursive
	;;
list)
	paths
	;;
check)
	printf '%-28s %-14s %-10s %s\n' PATH BRANCH PIN REMOTE
	rc=0
	while read -r path; do
		branch=$(git config -f .gitmodules --get "submodule.${path}.branch" || echo main)
		url=$(git config -f .gitmodules --get "submodule.${path}.url")
		pin=$(git ls-files -s -- "$path" | awk '{print $2}' | cut -c1-10)
		remote=$(git ls-remote "$url" "refs/heads/${branch}" | awk '{print $1}' | cut -c1-10)
		if [ -z "${remote}" ]; then
			state="NO-BRANCH"
			rc=1
		elif [ "${pin}" = "${remote}" ]; then
			state="up-to-date"
		elif ! git -C "$path" rev-parse --git-dir >/dev/null 2>&1; then
			state="not-init"
		elif git -C "$path" merge-base --is-ancestor "$pin" "$remote" 2>/dev/null; then
			state="behind"
		elif git -C "$path" merge-base --is-ancestor "$remote" "$pin" 2>/dev/null; then
			state="ahead"
		else
			state="diverged"
		fi
		printf '%-28s %-14s %-10s %s (%s)\n' "$path" "$branch" "$pin" "$remote" "$state"
	done <<<"$(paths)"
	exit "$rc"
	;;
foreach)
	[ $# -gt 0 ] || usage 1
	git submodule foreach --recursive "$@"
	;;
help | -h | --help)
	usage 0
	;;
*)
	echo "unknown command: $cmd" >&2
	usage 1
	;;
esac
