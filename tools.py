import requests
import re
import ast


def get_dir_lists(url):
    response = requests.get(url)
    print(response.text)


def clean_url(url: str) -> str:
    url = url.replace('\\', '/')
    url = url.replace(' ', '%20')
    url = re.sub(r'(?<!:)//+', '/', url)
    return url


def parse_string_to_list(string):
    try:
        parsed_value = ast.literal_eval(string)
        if not isinstance(parsed_value, list):
            return []
        return parsed_value
    except (ValueError, SyntaxError) as e:
        print(e)
        return []
