# Attack Profile — SSH-Patator (SSH Brute Force)

## What it is
SSH-Patator refers to brute-force credential attacks against the Secure
Shell (SSH) service, typically running on TCP port 22. As with FTP-Patator,
the name derives from the Patator brute-forcing tool.

## MITRE ATT&CK mapping
Primary technique: T1110 (Brute Force)
Common sub-techniques: T1110.001 (Password Guessing) and T1110.003
(Password Spraying) — SSH is targeted by both patterns depending on
whether the attacker has a known username or is sweeping multiple accounts.

## Network characteristics
- Destination port is consistently 22
- SSH connection attempts involve a key exchange and protocol negotiation
  before authentication, making each flow slightly more complex than FTP,
  but still short-lived on authentication failure
- TCP window size and initial handshake characteristics of automated SSH
  brute-force tools often differ measurably from standard SSH clients
  (e.g. OpenSSH client, PuTTY)
- A high volume of short flows to port 22 from one source IP, often with
  near-identical packet length statistics, indicates automated brute force

## Real-world impact
Successful SSH brute force grants shell access to the target host —
typically one of the most severe outcomes possible, as it can lead to
full system compromise, lateral movement, and persistence.

## Distinguishing from legitimate SSH traffic
The challenge in detecting SSH brute force is that port 22 also carries
entirely legitimate administrative traffic. The distinguishing factors are
volume (many attempts in a short window), failure rate (legitimate users
rarely fail authentication repeatedly), and the consistency of flow
statistics across attempts (automated tools produce highly repetitive flow
shapes; human-driven SSH sessions vary).
