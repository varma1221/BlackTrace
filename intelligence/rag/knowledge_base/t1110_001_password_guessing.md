# MITRE ATT&CK T1110.001 — Password Guessing

## Overview
Password guessing is the most common brute-force sub-technique. The
attacker has (or assumes) a valid username and systematically attempts a
list of candidate passwords against it. Lists range from a few hundred
common passwords ("password123", "admin", "letmein") to dictionaries with
millions of entries.

## Behavioral pattern
- Single username, many password attempts
- High frequency of failed authentication attempts in a short window
- Often automated using tools that iterate through a wordlist sequentially
- Attempts typically continue until success, a rate limit, or an account
  lockout is reached

## Relevance to FTP and SSH
FTP and SSH both expose a username/password authentication prompt over a
fixed, well-known port (21 and 22 respectively). Automated tools such as
Patator and Hydra are commonly used to perform password guessing against
these services because the protocols are simple to script and the ports
are predictable.

## Detection considerations
The defining signal is volume: a normal user might fail a login once or
twice. A password guessing attack produces dozens to thousands of failed
attempts from the same source in a short period, all targeting the same
destination port.
