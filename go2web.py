import sys
import ssl
import socket
import os
import hashlib
import warnings
from urllib.parse import urlparse
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=DeprecationWarning)
CACHE_DIRECTORY = "http_cache"

def print_help():
    print("Usage:")
    print("go2web.py -u <URL> # makes an HTTP request to the specified URL and prints the response")
    print("go2web.py -s <search-term> # makes an HTTP request to search the term using your favorite "
          "search engine and prints top 10 results")
    print("go2web.py -h # shows this help")
    
# fetches the url content
def fetch_url(url):
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIRECTORY, cache_key)

    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            print("Cashed from http_cache:\n")
            return f.read()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    parsed_url = urlparse(url)
    host, port, path = parsed_url.netloc, 443, parsed_url.path

    client_socket = ssl.wrap_socket(client_socket)

    try:
        client_socket.settimeout(2)
        client_socket.connect((host, port))

        request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = b""
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data
            except socket.timeout:
                break

        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(response.decode('utf-8', errors='ignore'))

        client_socket.close()
        return response.decode('utf-8', errors='ignore')

    except socket.error as e:
        print("Error making request:", e)
        sys.exit(1)

# prints the content of the given url
def print_url_response(url):
    response = fetch_url(url)
    soup = BeautifulSoup(response, "html.parser")

    print(f"\nContent of '{url}':")
    for header in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        print(header.get_text().strip())

    for paragraph in soup.find_all("p"):
        print(paragraph.get_text().strip())

    for link_element in soup.find_all("a", href=True):
        link = link_element.get("href")

        if link.startswith("http"):
            print(f"\n{link_element.get_text()}")
            print(f"Link: {link}\n")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        print_help()
    elif sys.argv[1] == "-u":
        if len(sys.argv) < 3:
            print("Invalid syntax. Use -h for help.")
        else:
            url = sys.argv[2]
            print_url_response(url)
    else:
        print("Invalid syntax. Use -h for help.")

if __name__ == "__main__":
    main()