import requests
import json
from urllib.parse import urlsplit, urlunsplit, quote, unquote
import xml.etree.ElementTree as ET
import os
import socket
import time


RECEIVER_PORT = 12800
RECEIVER_ROOT = "/data/homebrew"
RECEIVER_TIMEOUT = 10
RECEIVER_DISCOVERY_PORT = 12801
RECEIVER_BEACON = b"PKGSENDER"


def receiver_endpoint(ps_ip, path):
    return f"http://{ps_ip}:{RECEIVER_PORT}{path}"


def receiver_parse(response):
    # every reply is http 200: json, an "error:" line, a plain ok line, or the webui html
    text = response.text.strip()
    if text.startswith("{"):
        try:
            return json.loads(text)
        except Exception as e:
            print(e)
            return {"error": "invalid json reply"}
    if text.startswith("error:"):
        return {"error": text[len("error:"):].strip()}
    if "test build, installs disabled" in text:
        return {"error": "receiver is a TEST_ONLY build, installs are disabled"}
    if text.startswith("ok:") or text.startswith("SUCCESS"):
        return {"status": "success"}
    if text.startswith("FAILED"):
        return {"error": text}
    return {"error": "unexpected reply from receiver"}


def receiver_get(ps_ip, path, params=None):
    try:
        response = requests.get(receiver_endpoint(ps_ip, path), params=params, timeout=RECEIVER_TIMEOUT)
        return receiver_parse(response)
    except Exception as e:
        print(e)
        return {"error": "receiver is not reachable"}


def receiver_post(ps_ip, path, payload):
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(receiver_endpoint(ps_ip, path), data=json.dumps(payload),
                                 headers=headers, timeout=RECEIVER_TIMEOUT)
        return receiver_parse(response)
    except Exception as e:
        print(e)
        return {"error": "receiver is not reachable"}


def receiver_probe(ps_ip):
    # /api always answers with a json body, unknown GET paths answer with html instead
    return "status" in receiver_get(ps_ip, "/api")


def receiver_version(ps_ip):
    return receiver_get(ps_ip, "/api/version").get("build")


def receiver_pc(ps_ip):
    return receiver_get(ps_ip, "/api/pc")


def receiver_status(ps_ip):
    return receiver_get(ps_ip, "/api/status")


def receiver_file_stat(ps_ip, remote_path):
    return receiver_get(ps_ip, "/api/files/stat", {"path": remote_path})


def receiver_fs_list(ps_ip, remote_path=RECEIVER_ROOT):
    return receiver_get(ps_ip, "/api/fs/list", {"path": remote_path})


def receiver_pause(ps_ip, paused):
    # the flag is read as a number and is global, so true would unpause and it outlives a transfer
    return receiver_post(ps_ip, "/api/pull/pause", {"paused": 1 if paused else 0})


def receiver_install(pkg_url, ps_ip, name=None, icon_url=None):
    payload = {
        "packages": [pkg_url]
    }
    if name:
        payload["name"] = name
    if icon_url:
        payload["icon_url"] = icon_url
    return receiver_post(ps_ip, "/api/install", payload)


def receiver_pull(file_url, ps_ip, remote_path, mode="overwrite"):
    return receiver_post(ps_ip, "/api/files/pull", {"url": file_url, "path": remote_path, "mode": mode})


def receiver_send(pkg_url, ps_ip, pkg_file, total_size=0, name=None, icon_url=None):
    # .pkg goes through the installer, single file game formats are pulled into /data/homebrew
    if pkg_file.lower().endswith(".pkg"):
        result = receiver_install(pkg_url, ps_ip, name=name, icon_url=icon_url)
        result["kind"] = "install"
        return result
    remote_path = f"{RECEIVER_ROOT}/{pkg_file}"
    stat = receiver_file_stat(ps_ip, remote_path)
    if stat.get("exists") and 0 < stat.get("size", 0) < total_size:
        mode = "resume"
    else:
        mode = "overwrite"
    receiver_pause(ps_ip, False)
    result = receiver_pull(pkg_url, ps_ip, remote_path, mode)
    if result.get("ok"):
        result["status"] = "success"
    result["kind"] = "pull"
    result["mode"] = mode
    return result


def discover_receivers(timeout=4):
    # the payload broadcasts "PKGSENDER v1" every 3s, only the sender address matters
    found = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except Exception as e:
        print(e)
    try:
        sock.bind(("", RECEIVER_DISCOVERY_PORT))
    except Exception as e:
        print(e)
        sock.close()
        return found
    sock.settimeout(1)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            data, address = sock.recvfrom(256)
        except Exception:
            continue
        if data.startswith(RECEIVER_BEACON) and address[0] not in found:
            found.append(address[0])
    sock.close()
    return found


def package_sender(pkg_url, ps_ip, pkg_type="ps4", local_destination="/data/etaHEN/games",
                   ps5_send_method="haghpanah-ps5_file_downloader", pkg_name=None, icon_url=None,
                   pkg_file=None, total_size=0):
    headers = {
            "Content-Type": "application/json"
    }
    parts = urlsplit(pkg_url)
    pkg_url = urlunsplit((
        parts.scheme,
        parts.netloc,
        quote(unquote(parts.path)),
        parts.query,
        parts.fragment,
    ))
    if pkg_type == "ps4":
        endpoint = f"http://{ps_ip}:12800/api/install"
        data = {
            "type": "direct",
            "packages": [pkg_url]
        }
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        return json.loads(response.text)
    elif pkg_type == "ps5":
        if ps5_send_method == "loopayeh-pkg_receiver":
            if not pkg_file:
                pkg_file = unquote(urlsplit(pkg_url).path.split("/")[-1])
            return receiver_send(pkg_url=pkg_url, ps_ip=ps_ip, pkg_file=pkg_file,
                                 total_size=total_size, name=pkg_name, icon_url=icon_url)
        endpoint = f"http://{ps_ip}:8283/api/v1/get_file"
        data = {
            "url": pkg_url,
            "local_destination": local_destination,
        }
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        print(response)
        print(response.text)
        print(data)
        return json.loads(response.text)
    return {"status": "failed"}


def task_status(task_id, ps_ip):
    ps4_api = f"http://{ps_ip}:12800/api/get_task_progress"
    data = {
        "task_id": task_id
    }

    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(ps4_api, data=json.dumps(data), headers=headers)
    print(response.text)


def rawg_search(api_key, query, xml_path, desc=None):
    game_info_path = os.path.dirname(xml_path)
    if not os.path.exists(game_info_path):
        os.mkdir(game_info_path)
    default_xml = False
    error = None
    if api_key is None or api_key == "":
        default_xml = True
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
                    default_xml = True
            else:
                error = response.text
                default_xml = True
        except Exception as e:
            error = f'An error occurred: {str(e)}'
    if default_xml:
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
        description.text = desc
        tree = ET.ElementTree(root)
        tree.write(xml_path)
    if error:
        response = {"status": False, "data": None, "error": error}
    else:
        response = {"status": True, "data": None, "error": error}
    return response


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
