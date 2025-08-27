import requests

# URLs
url_raw = "https://raw.githubusercontent.com/mathpferreira/ranking-gta/main/docs/ranking.png"
url_pages = "https://mathpferreira.github.io/ranking-gta/ranking.png"

def get_headers(url):
    r = requests.head(url)
    return r.headers

def main():
    headers_raw = get_headers(url_raw)
    headers_pages = get_headers(url_pages)

    print("🔄 RAW (sempre atualizado):")
    print("ETag:", headers_raw.get("ETag"))
    print("Last-Modified:", headers_raw.get("Last-Modified"))
    print()
    print("🌍 Pages (pode estar atrasado):")
    print("ETag:", headers_pages.get("ETag"))
    print("Last-Modified:", headers_pages.get("Last-Modified"))

    if headers_raw.get("ETag") == headers_pages.get("ETag"):
        print("\n✅ Pages já está sincronizado com o repositório!")
    else:
        print("\n⏳ Pages ainda está servindo uma versão antiga (cache do CDN).")

if __name__ == "__main__":
    main()
