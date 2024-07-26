import requests
import re


def get_dir_lists(url):
    response = requests.get(url)
    print(response.text)


def clean_url(url: str) -> str:
    # Convert backslashes to forward slashes
    url = url.replace('\\', '/')

    # Replace spaces with %20 (URL encoding for space)
    url = url.replace(' ', '%20')

    # Remove extra slashes, but keep the "http://" or "https://" at the beginning
    url = re.sub(r'(?<!:)//+', '/', url)

    return url
