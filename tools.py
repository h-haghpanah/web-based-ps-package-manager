import requests


def get_dir_lists(url):
    response = requests.get(url)
    print(response.text)
    
get_dir_lists("")