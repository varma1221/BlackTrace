# Mitigations — Brute Force (T1110) and Sub-techniques

## Account lockout policies
Lock an account after a small number of consecutive failed authentication
attempts (e.g. 3-5). Mitigates password guessing against a single account,
though it does not stop password spraying, which deliberately stays under
per-account thresholds.

## Multi-factor authentication (MFA)
The single most effective mitigation. Even if an attacker guesses the
correct password, MFA prevents authentication from succeeding without the
second factor. Strongly recommended for any internet-facing FTP, SSH, or
RDP service.

## Rate limiting and connection throttling
Limit the number of authentication attempts permitted from a single source
IP within a time window, at the firewall or service level. Tools like
fail2ban monitor authentication logs and automatically block source IPs
that exceed a failure threshold.

## IP allowlisting
Restrict FTP and SSH access to known, trusted IP ranges (e.g. corporate VPN
exit points). Eliminates exposure to internet-wide brute force entirely for
services that do not need to be publicly accessible.

## Disable unused or legacy services
FTP in particular is an older protocol that transmits credentials in clear
text. Where file transfer is needed, SFTP or FTPS should be used instead.
If FTP is not required, disabling it removes the attack surface entirely.

## Strong, unique credentials
Default credentials and weak, commonly-used passwords are the entire
reason brute force attacks succeed. Enforcing strong password policies and
eliminating default accounts removes the low-hanging fruit that automated
tools are designed to find.

## Monitoring and alerting
Even with the above controls in place, monitoring for spikes in failed
authentication attempts and short, repetitive flows to authentication ports
provides early warning of an attack in progress, allowing IP-level blocking
before the attack succeeds.
