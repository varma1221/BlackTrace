"""
Threat Intelligence enrichment service.

Enriches suspicious IP addresses with reputation data and geographic context
to aid in security investigations.
"""
def enrich_ip(source_ip: str):
    """
    Enriches an IP address with intelligence metadata.

    Args:
        source_ip (str): The IPv4 address to investigate.

    Returns:
        dict: Metadata including country, ISP, threat score, and malicious status.
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
