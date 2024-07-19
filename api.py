import requests
import json
from urllib.parse import quote
import xml.etree.ElementTree as ET
# import json


def package_sender(pkg_name, web_ip, web_port, ps4_ip):
    pkg_url = f"http://{web_ip}:{web_port}/{pkg_name}"
    ps4_api = f"http://{ps4_ip}:12800/api/install"
    pkg_url = quote(pkg_url)
    data = {
        "type": "direct",
        "packages": [pkg_url]
    }
    print(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(ps4_api, data=json.dumps(data), headers=headers)
    return json.loads(response.text)


def task_status(task_id, ps4_ip):
    ps4_api = f"http://{ps4_ip}:12800/api/get_task_progress"
    data = {
        "task_id": task_id
    }

    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(ps4_api, data=json.dumps(data), headers=headers)
    print(response.text)


def rawg_search(api_key, query, xml_path):
    base_url = 'https://api.rawg.io/api/'
    endpoint = 'games'
    params = {'key': api_key, 'search': query}
    print(params)
    try:
        response = requests.get(f'{base_url}{endpoint}', params=params)
        if response.status_code == 200:
            data = response.json()
            games = data.get('results', [])

            if games:
                most_similar_game = games[0]
                root = ET.Element("game")
                name = ET.SubElement(root, "name")
                name.text = most_similar_game['name']
                rating = ET.SubElement(root, "rating")
                rating.text = str(most_similar_game['rating'])
                released = ET.SubElement(root, "released")
                released.text = most_similar_game['released']
                genres = ET.SubElement(root, "genres")
                genre_names = [genre['name'] for genre in most_similar_game['genres']]
                genres.text = ', '.join(genre_names)
                platforms = ET.SubElement(root, "platforms")
                platform_names = [platform['platform']['name'] for platform in most_similar_game['platforms']]
                platforms.text = ', '.join(platform_names)
                ratings_count = ET.SubElement(root, "ratings_count")
                ratings_count.text = str(most_similar_game['ratings_count'])
                released = ET.SubElement(root, "released")
                released.text = most_similar_game['released']
                updated = ET.SubElement(root, "updated")
                updated.text = most_similar_game['updated']
                metacritic = ET.SubElement(root, "metacritic")
                metacritic.text = str(most_similar_game['metacritic'])
                # description = ET.SubElement(root, "description")
                # description.text = most_similar_game['description']
                background_image = ET.SubElement(root, "background_image")
                background_image.text = most_similar_game['background_image']
                # background_image_additional = ET.SubElement(root, "background_image_additional")
                # background_image_additional.text = most_similar_game['background_image_additional']
                tree = ET.ElementTree(root)
                tree.write(xml_path)
            else:
                print('No games found for the given search query.')
        else:
            print(f'Error: {response.status_code}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
