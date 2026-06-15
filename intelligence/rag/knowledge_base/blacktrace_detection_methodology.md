# BlackTrace Detection Methodology — How This Alert Was Generated

## Two-stage detection pipeline
BlackTrace uses two machine learning models in sequence:

1. **Isolation Forest** — an unsupervised anomaly detector trained only on
   benign network traffic. It flags flows that deviate statistically from
   normal patterns.

2. **Random Forest classifier** — a supervised model trained on labelled
   examples of FTP-Patator, SSH-Patator, and benign traffic. When a flow is
   flagged, this model identifies the specific attack type with a
   confidence score.

## What drives the classification
For FTP-Patator and SSH-Patator, the Random Forest relies most heavily on:

- **Destination Port** — the single strongest signal, since these attacks
  exclusively target ports 21 and 22 respectively
- **TCP initial window size** (forward and backward) — automated
  brute-force tools often have distinguishable TCP stack signatures
  compared to standard clients
- **Packet length statistics** (mean, standard deviation, max) — the
  repetitive, automated nature of brute force produces consistent packet
  sizes across many flows

## Confidence scores
The confidence score reported with each alert represents the proportion of
decision trees in the Random Forest ensemble that agreed on the predicted
class. A confidence above 0.90 indicates strong agreement across the model
ensemble.

## Known limitations
The Isolation Forest component, while effective for volumetric anomalies
(e.g. DoS, port scans), does not reliably detect brute force attacks on a
per-flow basis. This is because individual brute-force flows can resemble
individual legitimate authentication attempts in isolation — the attack
signature only emerges in aggregate, across many flows over time. The
supervised Random Forest classifier is the primary detector for FTP-Patator
and SSH-Patator specifically.
