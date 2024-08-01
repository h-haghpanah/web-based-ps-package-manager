import requests
import json
from urllib.parse import quote
import xml.etree.ElementTree as ET
import os
# import json


# def package_sender(pkg_name, web_ip, web_port, ps4_ip):
#     pkg_url = f"http://{web_ip}:{web_port}/{pkg_name}"
#     ps4_api = f"http://{ps4_ip}:12800/api/install"
#     pkg_url = quote(pkg_url)
#     data = {
#         "type": "direct",
#         "packages": [pkg_url]
#     }
#     print(data)
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = requests.post(ps4_api, data=json.dumps(data), headers=headers)
#     return json.loads(response.text)


def package_sender(pkg_url, ps4_ip):
    # pkg_url = f"http://{web_ip}:{web_port}/{pkg_name}"
    print(pkg_url)
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
    game_info_path = os.path.dirname(xml_path)
    if not os.path.exists(game_info_path):
        os.mkdir(game_info_path)
    if api_key is None or api_key == "":
        name_find = query
        rating_find = "-"
        released_find = "-"
        genres_find = ["-"]
        platforms_find = ["-"]
        ratings_count_find = "0"
        updated_find = "-"
        metacritic_find = "-"
        background_image_find = "/assets/images/icons/pkg.png"
    else:
        base_url = 'https://api.rawg.io/api/'
        endpoint = 'games'
        params = {'key': api_key, 'search': query}
        try:
            response = requests.get(f'{base_url}{endpoint}', params=params)
            if response.status_code == 200:
                data = response.json()
                games = data.get('results', [])

                if games:
                    most_similar_game = games[0]
                    name_find = most_similar_game['name']
                    rating_find = str(most_similar_game['rating'])
                    released_find = most_similar_game['released']
                    genres_find = [genre['name'] for genre in most_similar_game['genres']]
                    platforms_find = [platform['platform']['name'] for platform in most_similar_game['platforms']]
                    ratings_count_find = str(most_similar_game['ratings_count'])
                    updated_find = most_similar_game['updated']
                    metacritic_find = str(most_similar_game['metacritic'])
                    background_image_find = most_similar_game['background_image']
                else:
                    print('No games found for the given search query.')
            else:
                print(f'Error: {response.status_code}')
        except Exception as e:
            print(f'An error occurred: {str(e)}')
    root = ET.Element("game")
    name = ET.SubElement(root, "name")
    name.text = name_find
    rating = ET.SubElement(root, "rating")
    rating.text = rating_find
    released = ET.SubElement(root, "released")
    released.text = released_find
    genres = ET.SubElement(root, "genres")
    genre_names = genres_find
    genres.text = ', '.join(genre_names)
    platforms = ET.SubElement(root, "platforms")
    platform_names = platforms_find
    platforms.text = ', '.join(platform_names)
    ratings_count = ET.SubElement(root, "ratings_count")
    ratings_count.text = ratings_count_find
    updated = ET.SubElement(root, "updated")
    updated.text = updated_find
    metacritic = ET.SubElement(root, "metacritic")
    metacritic.text = metacritic_find
    background_image = ET.SubElement(root, "background_image")
    background_image.text = background_image_find
    description = ET.SubElement(root, "description")
    description.text = ""
    tree = ET.ElementTree(root)
    tree.write(xml_path)


def update_xml_file(xml_path_update, title_update, genres_update, platforms_update, released_update, image_update, description_update, rating_update, ratings_count_update, updated_update, metacritic_update):
    game_info_path = os.path.dirname(xml_path_update)
    if not os.path.exists(game_info_path):
        os.mkdir(game_info_path)
    root = ET.Element("game")
    name = ET.SubElement(root, "name")
    name.text = title_update
    rating = ET.SubElement(root, "rating")
    rating.text = str(rating_update)
    released = ET.SubElement(root, "released")
    released.text = released_update
    genres = ET.SubElement(root, "genres")
    genres.text = genres_update
    platforms = ET.SubElement(root, "platforms")
    platforms.text = platforms_update
    ratings_count = ET.SubElement(root, "ratings_count")
    ratings_count.text = str(ratings_count_update)
    updated = ET.SubElement(root, "updated")
    updated.text = updated_update
    metacritic = ET.SubElement(root, "metacritic")
    metacritic.text = metacritic_update
    background_image = ET.SubElement(root, "background_image")
    background_image.text = image_update
    description = ET.SubElement(root, "description")
    description.text = description_update
    tree = ET.ElementTree(root)
    tree.write(xml_path_update)
