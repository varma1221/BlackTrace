# MITRE ATT&CK T1110.003 — Password Spraying

## Overview
Password spraying inverts the password guessing approach: instead of many
passwords against one username, the attacker tries one or a small handful
of common passwords against *many* different usernames. This is designed
specifically to avoid triggering per-account lockout policies, since each
individual account only receives one or two failed attempts.

## Behavioral pattern
- Many usernames, few passwords
- Low frequency per account, but high frequency overall across accounts
- Often deliberately slowed down ("low and slow") to blend in with normal
  traffic and avoid both lockout policies and naive rate-based detection

## Relevance to SSH
SSH password spraying against a server with multiple valid user accounts
follows this pattern — the attacker cycles through usernames like "admin",
"root", "ubuntu", "test" with one or two common passwords each.

## Detection considerations
Per-account thresholds are insufficient against spraying because no single
account exceeds the threshold. Detection requires looking at aggregate
failed-authentication volume from a source IP across *all* accounts on a
destination, not just one account.
