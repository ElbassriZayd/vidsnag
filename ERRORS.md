# Errors

Scan at session start. Add every failure here immediately.

| Date | Area | What failed | Root cause | Fix |
|------|------|-------------|------------|-----|
| 2026-05-29 | Filesystem | File writes failed / corrupted (README.md → 0 bytes) | C: drive 100% full (<50 MB free); ENOSPC truncates open files to 0 bytes | Free disk space; set pagefile AutomaticManagedPagefile=true; reboot; rewrite corrupted files. See global memory feedback_disk_full_silently_kills_pagefile |
