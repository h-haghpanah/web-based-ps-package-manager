
from flask import Flask, render_template, send_from_directory, jsonify, request
import requests
import os
from api import rawg_search, package_sender, update_xml_file
import xml.etree.ElementTree as ET
from decouple import config
import json
from tools import clean_url, parse_string_to_list


REMOTE_PKG_REPOSITORY_WEB_PROTOCOL = config("REMOTE_PKG_REPOSITORY_WEB_PROTOCOL", cast=str, default="http")
REMOTE_PKG_REPOSITORY_WEB_IP_ADDRESS = config("REMOTE_PKG_REPOSITORY_WEB_IP_ADDRESS", cast=str)
REMOTE_PKG_REPOSITORY_WEB_PORT = config("REMOTE_PKG_REPOSITORY_WEB_PORT", cast=str)
LOCAL_PKG = config("LOCAL_PKG", cast=bool)
LOCAL_PKG_PATH = "local_pkg"
if not os.path.exists(LOCAL_PKG_PATH):
    os.mkdir(LOCAL_PKG_PATH)
if LOCAL_PKG_PATH[-1] == "/" or LOCAL_PKG_PATH[-1] == "\\":
    LOCAL_PKG_PATH = LOCAL_PKG_PATH[:-1]
LOCAL_IP_ADDRESS = config("LOCAL_IP_ADDRESS", cast=str)
LOCAL_PORT = config("LOCAL_PORT", cast=str, default="80")
RAWG_API_KEY = config("RAWG_API_KEY", cast=str, default="")
PS_ADDRESSES = config("PS_ADDRESSES", cast=str)
CURRENT_SELECTED_PS_FILE_PATH = "selected_ps_ip.txt"
DEBUG = config("DEBUG", cast=bool, default=False)
REPOSITORY = config("REPOSITORY", cast=str, default="mixed")
if REPOSITORY.lower() == "ps4":
    WEB_TITLE = "PS4 Package Sender"
    WEB_LOGO = "logo-ps4.png"
elif REPOSITORY.lower() == "ps5":
    WEB_TITLE = "PS5 Package Sender"
    WEB_LOGO = "logo-ps5.png"
else:
    WEB_TITLE = "PS Package Sender"
    WEB_LOGO = "logo.png"
IGNORE_LIST = config("IGNORE_LIST", cast=str, default="[]")
IGNORE_LIST = parse_string_to_list(IGNORE_LIST)

app = Flask(__name__)
app.config["SECRET_KEY"] = "mywebKey"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def root():
    return render_template("home.html", WEB_TITLE=WEB_TITLE, WEB_LOGO=WEB_LOGO)


@app.route("/game_list")
def game_list():
    if LOCAL_PKG:
        games = os.listdir("local_pkg")
    else:
        games = requests.get(f"{REMOTE_PKG_REPOSITORY_WEB_PROTOCOL}://{REMOTE_PKG_REPOSITORY_WEB_IP_ADDRESS}:{REMOTE_PKG_REPOSITORY_WEB_PORT}").text
        games = json.loads(games)
    game_folder = []
    all_games = []
    for item in games:
        if LOCAL_PKG and not os.path.isdir(os.path.join(LOCAL_PKG_PATH, item)):
            continue
        if item in IGNORE_LIST:
            continue
        game_folder.append(item)
        xml_path = os.path.join("assets/game_info", item+".xml")
        if not os.path.exists(xml_path):
            rawg_search(RAWG_API_KEY, item.replace("_", " "), xml_path)
            name = item
            genres = ""
            platforms = ""
            released = ""
            updated = ""
            rating = ""
            ratings_count = ""
            metacritic = ""
            background_image = "assets/images/icons/pkg.png"
            url = "game/"+item
        else:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            name = root.find("name").text
            genres = root.find("genres").text
            platforms = root.find("platforms").text
            released = root.find("released").text
            updated = root.find("updated").text
            rating = root.find("rating").text
            try:
                ratings_count = int(root.find("ratings_count").text)
                if ratings_count >= 1000:
                    ratings_count = round(ratings_count / 1000, 1)
                    ratings_count = str(ratings_count) + "k"
                else:
                    ratings_count = str(ratings_count)
            except Exception as e:
                print(e)
                ratings_count = "Not specified"
            metacritic = root.find("metacritic").text
            background_image = root.find("background_image").text
            url = "game/"+item
        all_games.append({"name": name, "background_image": background_image, "url": url, "genres": genres, "platforms": platforms, "released": released, "updated": updated, "rating": rating, "ratings_count": ratings_count, "metacritic": metacritic})
    return jsonify(all_games)


@app.route('/game/<path:path>', methods=['GET'])
def game(path):
    xml_path = os.path.join("assets/game_info", path+".xml")
    if not os.path.exists(xml_path):
        name = path
        background_image = "assets/images/icons/pkg.png"
        genres = "Not specified"
        platforms = "Not specified"
        released = "Not specified"
        updated = "Not specified"
        rating = "Not specified"
        ratings_count = "Not specified"
        metacritic = "Not specified"
        description = ""
    else:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        name = root.find("name").text
        genres = root.find("genres").text
        platforms = root.find("platforms").text
        released = root.find("released").text
        updated = root.find("updated").text
        rating = root.find("rating").text
        description = root.find("description").text
        try:
            ratings_count = int(root.find("ratings_count").text)
            if ratings_count >= 1000:
                ratings_count = round(ratings_count / 1000, 1)
                ratings_count = str(ratings_count) + "k"
            else:
                ratings_count = str(ratings_count)
        except Exception as e:
            print(e)
            ratings_count = "Not specified"
        metacritic = root.find("metacritic").text
        background_image = root.find("background_image").text
    if LOCAL_PKG:
        folders = os.listdir(os.path.join(LOCAL_PKG_PATH, path))
    else:
        subfolders_of_game = requests.get(f"{REMOTE_PKG_REPOSITORY_WEB_PROTOCOL}://{REMOTE_PKG_REPOSITORY_WEB_IP_ADDRESS}:{REMOTE_PKG_REPOSITORY_WEB_PORT}/index.php?folder_name={path}").text
        subfolders_of_game = json.loads(subfolders_of_game)
        folders = subfolders_of_game.keys()
    install_folder_name = ""
    update_folder_name = ""
    dlc_folder_name = ""
    install_btn = False
    update_btn = False
    dlc_btn = False
    for key in folders:
        if key.lower() == "install":
            install_folder_name = key
            install_btn = True
        elif key.lower() == "update":
            update_folder_name = key
            update_btn = True
        elif key.lower() == "dlc":
            dlc_folder_name = key
            dlc_btn = True

    return render_template("game.html", WEB_TITLE=WEB_TITLE, WEB_LOGO=WEB_LOGO, background_image=background_image,
                           rating=rating, metacritic=metacritic, name=name, ratings_count=ratings_count, genres=genres,
                           platforms=platforms, released=released, updated=updated, install_btn=install_btn, update_btn=update_btn,
                           dlc_btn=dlc_btn, game_path=path, install_folder_name=install_folder_name, update_folder_name=update_folder_name,
                           dlc_folder_name=dlc_folder_name, description=description)


@app.route('/pkg_list/<path:path>', methods=['GET'])
def pkg_list(path):
    path_split = path.split("/")
    if len(path_split) == 2:
        game_name = path_split[0]
        game_path = path_split[1]
    else:
        return jsonify({"success": False})
    links = []
    if LOCAL_PKG:
        pkgs = os.listdir(os.path.join(LOCAL_PKG_PATH, path))
        for pkg in pkgs:
            links.append({"pkg": pkg, "path": path})
    else:
        subfolders_of_game = requests.get(f"{REMOTE_PKG_REPOSITORY_WEB_PROTOCOL}://{REMOTE_PKG_REPOSITORY_WEB_IP_ADDRESS}:{REMOTE_PKG_REPOSITORY_WEB_PORT}/index.php?folder_name={game_name}").text
        subfolders_of_game = json.loads(subfolders_of_game)
        if game_path in subfolders_of_game:
            pkgs = subfolders_of_game[game_path]
            for pkg in pkgs:
                links.append({"pkg": pkg, "path": path})
    return jsonify(links)


@app.route('/submit_game_info', methods=['POST'])
def submit_game_info():
    title = request.form.get("title")
    genres = request.form.get("genres")
    platforms = request.form.get("platforms")
    released = request.form.get("released")
    image = request.form.get("image")
    description = request.form.get("description")
    rating = request.form.get("rating")
    try:
        rating = float(rating)
    except Exception as e:
        print(e)
        rating = "None"
    ratings_count = request.form.get("ratings_count")
    try:
        ratings_count = int(ratings_count)
    except Exception as e:
        print(e)
        ratings_count = "Not specified"
    updated = request.form.get("updated")
    metacritic = request.form.get("metacritic")
    game_xml_name = request.form.get("game_xml_name")
    xml_path = f"assets/game_info/{game_xml_name}"
    try:
        update_xml_file(xml_path_update=xml_path, title_update=title, genres_update=genres, platforms_update=platforms,
                        released_update=released, image_update=image, description_update=description, rating_update=rating,
                        ratings_count_update=ratings_count, updated_update=updated, metacritic_update=metacritic)
        response = {"status": True, "data": {"rating": rating, "ratings_count": ratings_count}}
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {"status": False, "error": str(e)}
        return jsonify(response)


@app.route('/send_pkg/<path:path>', methods=['GET'])
def send_pkg(path):
    if LOCAL_PKG:
        pkg_url = f"http://{LOCAL_IP_ADDRESS}:{LOCAL_PORT}/{LOCAL_PKG_PATH}/{path}"
    else:
        pkg_url = f"{REMOTE_PKG_REPOSITORY_WEB_PROTOCOL}://{REMOTE_PKG_REPOSITORY_WEB_IP_ADDRESS}:{REMOTE_PKG_REPOSITORY_WEB_PORT}/{path}"
    pkg_url = clean_url(pkg_url)
    try:
        with open(CURRENT_SELECTED_PS_FILE_PATH, 'r') as file:
            ps_ip = file.read()
            file.close()
        response = package_sender(pkg_url, ps_ip)
        print(response)
        if response["status"] == "success":
            status = True
        else:
            status = False
        return jsonify({"success": status})
    except FileNotFoundError:
        with open(CURRENT_SELECTED_PS_FILE_PATH, 'w') as file:
            file.write('')
    except Exception as e:
        print(e)
        status = False
        return jsonify({"success": status})


@app.route('/update_ps_address', methods=['POST'])
def update_ps_address():
    try:
        ps_ip = request.form["ps_ip"]
        with open(CURRENT_SELECTED_PS_FILE_PATH, 'w') as file:
            file.write(ps_ip)
            file.close()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@app.route('/read_ps_addresses', methods=['GET'])
def read_ps_addresses():
    try:
        addresses = []
        with open(CURRENT_SELECTED_PS_FILE_PATH, 'r') as file:
            ps_ip = file.read()
            file.close()
        ps_addresses_array = PS_ADDRESSES.split("$")
        condition = False
        for item in ps_addresses_array:
            item2 = item.split("@")
            if item2[1] == ps_ip:
                condition = True
                addresses.append({"name": item2[0], "address": item2[1], "selected": True})
            elif ps_addresses_array.index(item) != len(ps_addresses_array) - 1:
                addresses.append({"name": item2[0], "address": item2[1], "selected": False})
            else:
                if condition:
                    addresses.append({"name": item2[0], "address": item2[1], "selected": False})
                else:
                    addresses.append({"name": item2[0], "address": item2[1], "selected": True})
                    with open(CURRENT_SELECTED_PS_FILE_PATH, 'w') as file:
                        file.write(item2[1])
                        file.close()
        return jsonify({"success": True, "addresses": addresses})
    except FileNotFoundError:
        with open(CURRENT_SELECTED_PS_FILE_PATH, 'w') as file:
            file.write('')
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@app.route('/assets/<path:path>', methods=['GET', 'POST'])
def send_assets(path):
    return send_from_directory('assets', path)


@app.route('/local_pkg/<path:path>', methods=['GET', 'POST'])
def send_local_pkg(path):
    return send_from_directory('local_pkg', path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=LOCAL_PORT, debug=DEBUG)
