import requests
import dns.resolver
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def normalize_domain(domain):
    if not domain.startswith(("http://", "https://")):
        url = "https://" + domain
    else:
        url = domain
    parsed = urlparse(url)
    return parsed.netloc

def get_dns_records(domain):
    records = {}
    for record_type in ["A", "MX", "NS"]:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(r) for r in answers]
        except:
            records[record_type] = []
    return records

def get_website_info(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "Not Found"

        description = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            description = meta.get("content", "")

        return {
            "status_code": response.status_code,
            "title": title,
            "description": description
        }
    except Exception as e:
        return {"error": str(e)}

def generate_report(domain):
    domain = normalize_domain(domain)

    print("\n=== OSINT SOURCE CHECKER REPORT ===")
    print(f"Domain: {domain}\n")

    dns_data = get_dns_records(domain)
    print("DNS Records")
    for rtype, values in dns_data.items():
        print(f"{rtype}:")
        for value in values:
            print(f"  - {value}")

    site_info = get_website_info(domain)

    print("\nWebsite Information")
    for key, value in site_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    target = input("Enter domain: ")
    generate_report(target)
