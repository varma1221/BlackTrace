"""
Threat Intelligence enrichment service.

This module enriches suspicious IP addresses with
security intelligence metadata that helps analysts
understand attacker context and risk.
"""

def enrich_ip(source_ip: str):
    """
    Enriches an IP address with threat intelligence data.
    
    Args:
        source_ip: The IPv4 address to investigate.
    Returns:
        A dictionary containing country, ISP, threat_score and
        known_malicious status
    """
    simulated_threat_data = {
        "185.220.101.1": {
           "country": "Germany",
           "isp": "TOR Exit Node",
           "threat_source": 95,
           "known_malicious": True 
        },
        "91.240.118.12": {
            "country": "Russia",
            "isp": "Offshore Hosting Provider",
            "threat_source": 88,
            "known_malicious": True
        }
    }
    
    return simulated_threat_data.get(
        source_ip,
        {
            "country": "Unknown",
            "isp": "Unknown",
            "threat_score": 15,
            "known_malicious": False
        }
    )
