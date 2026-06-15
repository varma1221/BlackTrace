# Attack Profile — FTP-Patator (FTP Brute Force)

## What it is
FTP-Patator refers to brute-force credential attacks against the File
Transfer Protocol (FTP) service, typically running on TCP port 21. The
name derives from "Patator", a popular open-source brute-forcing tool
that supports FTP among many other protocols.

## MITRE ATT&CK mapping
Primary technique: T1110 (Brute Force)
Most common sub-technique: T1110.001 (Password Guessing)

## Network characteristics
- Destination port is consistently 21
- Each connection attempt is short — the FTP server responds quickly to
  an authentication failure (response code 530)
- Packet sizes are small and consistent across attempts, since the FTP
  authentication exchange (USER/PASS commands and response codes) has a
  fixed, predictable structure
- A high volume of these short, similar-sized flows from one source IP to
  port 21 in a short time window is the defining signature

## Why machine learning models key on Destination Port
Because FTP brute force traffic exclusively targets port 21, and normal
FTP usage on a given network is comparatively rare, Destination Port alone
becomes a very strong discriminating feature between this attack type and
benign traffic. Combined with TCP-level signatures (initial window size,
packet length statistics) that differ between automated brute-force tools
and standard FTP clients, classifiers can achieve very high accuracy on
this attack type.

## Real-world impact
Successful FTP brute force grants the attacker file system access via FTP
credentials, which can lead to data exfiltration, malware upload, or use
of the compromised host as a pivot point.
