from ipwhois.net import Net
from ipwhois.asn import IPASN
try:
    net = Net("122.146.12.30")
    obj = IPASN(net)
    results = obj.lookup()
    print(" ASN:", results['asn'], '|', +"Country:", results['asn_country_code'], '|', "ASN registry:", results['asn_registry'].upper(), '|', "Description:", results['asn_description'])
except Exception:
    print("\nNo ASN records")
