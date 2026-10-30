SHELL := /bin/bash
SCRIPT := scripts/submodules.sh

.PHONY: help init update sync status check list foreach

help:
	@printf '%s\n' \
		'make init      Register submodule URLs and clone every component' \
		'make update    Fast-forward submodules to the commits pinned here' \
		'make sync      Move every submodule to the head of its tracked branch' \
		'make status    Show pinned commit, branch and dirty state' \
		'make check     Compare pins against remote branch heads' \
		'make list      Print submodule paths' \
		'make foreach CMD="git log -1 --oneline"'

init:
	@$(SCRIPT) init

update:
	@$(SCRIPT) update

sync:
	@$(SCRIPT) sync

status:
	@$(SCRIPT) status

check:
	@$(SCRIPT) check

list:
	@$(SCRIPT) list

foreach:
	@test -n "$(CMD)" || { echo 'usage: make foreach CMD="<command>"' >&2; exit 1; }
	@$(SCRIPT) foreach '$(CMD)'
