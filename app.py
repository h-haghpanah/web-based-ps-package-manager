
from flask import Flask, render_template, send_from_directory, jsonify, request
import requests
import os
from api import rawg_search, package_sender, update_xml_file
import xml.etree.ElementTree as ET
import json
from tools import clean_url, parse_string_to_list
import configparser
import urllib.parse


LOCAL_PKG_PATH = "local_pkg"
SELECTED_PS_FILE_PATH = "selected_ps_ip.txt"

if not os.path.exists(LOCAL_PKG_PATH):
    os.mkdir(LOCAL_PKG_PATH)


def get_config():
    dirname = os.path.dirname(__file__)
    config = configparser.RawConfigParser()
    config_file = "./config.ini"
    default_config = """
[local_webserver]
local_port = 85

[general]
debug = False
ignore_list = ['.DS_Store', '.streams']
web_title = PS4 Pakcage sender

[local_system]
ip_address = 192.168.1.10

[remote_web_server]
address = http://192.168.1.20:8080

[rawg]
rawg_api_enabled = False
rawg_api_key =

[ps]
local_pkg_enabled = True
addresses = []
repository_type = ps4
    """
    if not os.path.isfile(config_file):
        with open(config_file, 'w') as file:
            file.write(default_config)
    config_path = os.path.join(dirname, config_file)
    config.read(config_path)
    return config


app = Flask(__name__)
app.config["SECRET_KEY"] = "mywebKey"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def root():
    config = get_config()
    web_title = config.get("general", "web_title")
    repository_type = config.get("ps", "repository_type")
    web_logo = f"logo-{repository_type}.png"
    return render_template("home.html", WEB_TITLE=web_title, WEB_LOGO=web_logo)


@app.route("/game_list")
def game_list():
    config = get_config()
    local_pkg_enabled = config.getboolean("ps", "local_pkg_enabled")
    remote_repository_address = config.get("remote_web_server", "address")
    ignore_list = config.get("general", "ignore_list")
    ignore_list = parse_string_to_list(ignore_list)
    rawg_api_enabled = config.getboolean("rawg", "rawg_api_enabled")
    rawg_api_key = config.get("rawg", "rawg_api_key")
    error = ""
    game_folder = []
    all_games = []
    if local_pkg_enabled:
        if not os.path.exists(LOCAL_PKG_PATH):
            os.mkdir(LOCAL_PKG_PATH)
        games = os.listdir(LOCAL_PKG_PATH)
    else:
        try:
            games = requests.get(remote_repository_address)
            if games.status_code == 200:
                games = games.text
                games = json.loads(games)
            else:
                error = "The root directory of the remote repository's web server does not contain an index.php file."
                games = "[]"
                games = json.loads(games)
        except Exception as e:
            print(e)
            error = "Remote repository web address not available"
            games = []

    for item in games:
        if local_pkg_enabled and not os.path.isdir(os.path.join(LOCAL_PKG_PATH, item)):
            continue
        if item in ignore_list:
            continue
        game_folder.append(item)
        xml_path = os.path.join("assets/game_info", item+".xml")
        if not os.path.exists(xml_path):
            if rawg_api_enabled:
                rawg_response = rawg_search(rawg_api_key, item.replace("_", " "), xml_path)
                if not rawg_response["status"]:
                    error += f'{rawg_response["error"]}\n'
            else:
                pass
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
    if error:
        response = {"status": False, "data": all_games, "error": error}
    else:
        response = {"status": True, "data": all_games, "error": error}
    return jsonify(response)


@app.route('/game/<path:path>', methods=['GET'])
def game(path):
    config = get_config()
    local_pkg_enabled = config.getboolean("ps", "local_pkg_enabled")
    remote_repository_address = config.get("remote_web_server", "address")
    web_title = config.get("general", "web_title")
    repository_type = config.get("ps", "repository_type")
    web_logo = f"logo-{repository_type}.png"
    xml_path = os.path.join("assets/game_info", path+".xml")
    rawg_api_enabled = config.getboolean("rawg", "rawg_api_enabled")
    if rawg_api_enabled:
        rawg_ap_reload_btn_status = ""
    else:
        rawg_ap_reload_btn_status = "disabled"
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
    if local_pkg_enabled:
        folders = os.listdir(os.path.join(LOCAL_PKG_PATH, path))
    else:
        subfolders_of_game = requests.get(f"{remote_repository_address}/index.php?folder_name={path}").text
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
    if not description or description == "None":
        description = ""
    return render_template("game.html", WEB_TITLE=web_title, WEB_LOGO=web_logo, background_image=background_image,
                           rating=rating, metacritic=metacritic, name=name, ratings_count=ratings_count, genres=genres,
                           platforms=platforms, released=released, updated=updated, install_btn=install_btn, update_btn=update_btn,
                           dlc_btn=dlc_btn, game_path=path, install_folder_name=install_folder_name, update_folder_name=update_folder_name,
                           dlc_folder_name=dlc_folder_name, description=description, rawg_ap_reload_btn_status=rawg_ap_reload_btn_status)


@app.route('/pkg_list/<path:path>', methods=['GET'])
def pkg_list(path):
    config = get_config()
    local_pkg_enabled = config.getboolean("ps", "local_pkg_enabled")
    remote_repository_address = config.get("remote_web_server", "address")
    path_split = path.split("/")
    if len(path_split) == 2:
        game_name = path_split[0]
        game_path = path_split[1]
    else:
        return jsonify({"success": False})
    links = []
    if local_pkg_enabled:
        pkgs = os.listdir(os.path.join(LOCAL_PKG_PATH, path))
        for pkg in pkgs:
            links.append({"pkg": pkg, "path": path})
    else:
        subfolders_of_game = requests.get(f"{remote_repository_address}/index.php?folder_name={game_name}").text
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


@app.route('/reload_rawg_game_info', methods=['POST'])
def reload_rawg_game_info():
    reload_option = request.form.get("reload_option")
    title = request.form.get("title")
    description = request.form.get("description")
    directory_name = request.form.get("directory_name")
    config = get_config()
    rawg_api_enabled = config.getboolean("rawg", "rawg_api_enabled")
    rawg_api_key = config.get("rawg", "rawg_api_key")
    directory_name = urllib.parse.unquote(directory_name)
    xml_path = os.path.join("assets/game_info", directory_name+".xml")
    error = None
    if rawg_api_enabled:
        if reload_option == "withTitle":
            rawg_response = rawg_search(rawg_api_key, title, xml_path, desc=description)
        elif reload_option == "withDirectory":
            rawg_response = rawg_search(rawg_api_key, directory_name.replace("_", " "), xml_path, desc=description)
        else:
            rawg_response = rawg_search(rawg_api_key, directory_name.replace("_", " "), xml_path, desc=description)
        if not rawg_response["status"]:
            error = str(rawg_response["error"])
    if error:
        response = {"status": False, "data": None, "error": error}
    else:
        response = {"status": True, "data": None, "error": None}
    return jsonify(response)


@app.route('/read_config', methods=['GET'])
def read_config():
    config = get_config()
    web_title = config.get("general", "web_title")
    local_system_ip_address = config.get("local_system", "ip_address")
    remote_web_server_address = config.get("remote_web_server", "address")
    rawg_api_enabled = config.getboolean("rawg", "rawg_api_enabled")
    rawg_api_key = config.get("rawg", "rawg_api_key")
    local_pkg_enabled = config.getboolean("ps", "local_pkg_enabled")
    ps_addresses = config.get("ps", "addresses")
    repository_type = config.get("ps", "repository_type")
    ps_addresses = json.loads(ps_addresses)
    ps_addresses_str = ""
    for address in ps_addresses:
        ps_addresses_str += f'{address["name"]}={address["ip_address"]}\n'
    return jsonify({"status": True, "data": {"web_title": web_title, "local_system_ip_address": local_system_ip_address, "remote_web_server_address": remote_web_server_address,
                                             "rawg_api_enabled": rawg_api_enabled, "rawg_api_key": rawg_api_key, "local_pkg_enabled": local_pkg_enabled,
                                             "ps_addresses": ps_addresses_str, "repository_type": repository_type}})


@app.route('/submit_config', methods=['POST'])
def submit_config():
    local_pkg_enabled = request.form.get("local_pkg_enabled")
    local_ip_address = request.form.get("local_ip_address")
    remote_repository_address = request.form.get("remote_repository_address")
    rawg_api_enabled = request.form.get("rawg_api_enabled")
    rawg_api_key = request.form.get("rawg_api_key")
    repository_type = request.form.get("repository_type")
    web_title = request.form.get("web_title")
    ps_ip_addresses = request.form.get("ps_ip_addresses")
    config = get_config()
    ignore_list = config.get("general", "IGNORE_LIST")
    debug = config.getboolean("general", "DEBUG")
    local_port = config.get("local_webserver", "LOCAL_PORT")
    if remote_repository_address[-1] == "/" or remote_repository_address[-1] == "\\":
        remote_repository_address = remote_repository_address[:-1]
    if not remote_repository_address.startswith(('http://', 'https://')):
        remote_repository_address = f'http://{remote_repository_address}'
    if local_pkg_enabled == "true":
        local_pkg_enabled = True
    else:
        local_pkg_enabled = False

    ps_ip_addresses = ps_ip_addresses.split("\n")
    ps_addresses = []
    for ps in ps_ip_addresses:
        seprated_ps_address = ps.split("=")
        if len(seprated_ps_address) == 2:
            ps_addresses.append({"name": ' '.join(seprated_ps_address[0].split()), "ip_address": ' '.join(seprated_ps_address[1].split())})
    ps_addresses = json.dumps(ps_addresses)
    if rawg_api_enabled == "true":
        rawg_api_enabled = True
    else:
        rawg_api_enabled = False

    if repository_type == "ps4" or repository_type == "ps5" or repository_type == "ps":
        pass
    else:
        repository_type = "ps"

    config['local_system'] = {
        'IP_ADDRESS': local_ip_address,
    }

    config['local_webserver'] = {
        'LOCAL_PORT': local_port
    }

    config['remote_web_server'] = {
        'ADDRESS': remote_repository_address
    }

    config['general'] = {
        'DEBUG': debug,
        'IGNORE_LIST': ignore_list,
        'WEB_TITLE': web_title,
    }

    config['rawg'] = {
        'RAWG_API_ENABLED': rawg_api_enabled,
        'RAWG_API_KEY': rawg_api_key
    }

    config['ps'] = {
        "LOCAL_PKG_ENABLED": local_pkg_enabled,
        'ADDRESSES': ps_addresses,
        'REPOSITORY_TYPE': repository_type,
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    response = {"status": True, "error": str("e")}
    return jsonify(response)


@app.route('/send_pkg/<path:path>', methods=['GET'])
def send_pkg(path):
    config = get_config()
    local_pkg_enabled = config.getboolean("ps", "local_pkg_enabled")
    remote_repository_address = config.get("remote_web_server", "address")
    local_operating_system_ip_address = config.get("local_system", "ip_address")
    local_web_server_port = config.get("local_webserver", "local_port")
    if local_pkg_enabled:
        pkg_url = f"http://{local_operating_system_ip_address}:{local_web_server_port}/{LOCAL_PKG_PATH}/{path}"
    else:
        pkg_url = f"{remote_repository_address}/{path}"
    pkg_url = clean_url(pkg_url)
    try:
        with open(SELECTED_PS_FILE_PATH, 'r') as file:
            ps_ip = file.read()
            file.close()
        response = package_sender(pkg_url, ps_ip)
        if response["status"] == "success":
            status = True
        else:
            status = False
        return jsonify({"success": status})
    except FileNotFoundError:
        with open(SELECTED_PS_FILE_PATH, 'w') as file:
            file.write('')
    except Exception as e:
        print(e)
        status = False
        return jsonify({"success": status})


@app.route('/update_ps_address', methods=['POST'])
def update_ps_address():
    try:
        ps_ip = request.form["ps_ip"]
        with open(SELECTED_PS_FILE_PATH, 'w') as file:
            file.write(ps_ip)
            file.close()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@app.route('/read_ps_addresses', methods=['GET'])
def read_ps_addresses():
    config = get_config()
    ps_addresses = config.get("ps", "addresses")
    ps_addresses = json.loads(ps_addresses)
    try:
        # addresses = []
        with open(SELECTED_PS_FILE_PATH, 'r') as file:
            ps_ip = file.read()
            file.close()
        default_selected = False
        addresses = []
        for item in ps_addresses:
            if item["ip_address"] == ps_ip:
                default_selected = True
                addresses.append({"name": item["name"], "address": item["ip_address"], "selected": True})
            elif ps_addresses.index(item) != len(ps_addresses) - 1:
                addresses.append({"name": item["name"], "address": item["ip_address"], "selected": False})
            else:
                if default_selected:
                    addresses.append({"name": item["name"], "address": item["ip_address"], "selected": False})
                else:
                    addresses.append({"name": item["name"], "address": item["ip_address"], "selected": True})
                    with open(SELECTED_PS_FILE_PATH, 'w') as file:
                        file.write(item["ip_address"])
                        file.close()
        return jsonify({"success": True, "addresses": addresses})
    except FileNotFoundError:
        with open(SELECTED_PS_FILE_PATH, 'w') as file:
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
    config = get_config()
    local_web_server_local_port = config.get("local_webserver", "local_port")
    debug = config.get("general", "debug")
    app.run(host="0.0.0.0", port=local_web_server_local_port, debug=debug)
