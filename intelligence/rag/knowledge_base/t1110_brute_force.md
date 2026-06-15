# MITRE ATT&CK T1110 — Brute Force

## Overview
Brute force is a credential access technique where an attacker attempts
many username and password combinations against a service until a valid
combination is found. Unlike exploiting a software vulnerability, brute
force attacks rely purely on repeated authentication attempts and do not
require any flaw in the target software.

## Why attackers use it
Brute force is simple, requires no advanced exploit development, and
remains effective against any system using weak, default, reused, or
commonly-guessed passwords. It is frequently the first technique attempted
against any internet-facing service that exposes an authentication prompt.

## Sub-techniques
- T1110.001 Password Guessing — many passwords against one username
- T1110.002 Password Cracking — offline cracking of stolen password hashes
- T1110.003 Password Spraying — one or few passwords against many usernames
- T1110.004 Credential Stuffing — reusing leaked username/password pairs

## Common targets
FTP (port 21), SSH (port 22), RDP (port 3389), web login forms, VPN
gateways, and database services with exposed authentication.

## Network-level signature
Brute force attacks produce a high volume of authentication attempts in a
short time window, typically from a single source IP to a single
destination port. Individual flows are often short-lived, with consistent
packet sizes corresponding to the authentication protocol's handshake and
rejection messages.
