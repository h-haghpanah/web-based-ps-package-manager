
from flask import Flask, render_template, send_from_directory, jsonify, request
import os
from api import rawg_search, package_sender
import xml.etree.ElementTree as ET
from decouple import config


PKG_STORE_WEB_IP_ADDRESS = config("PKG_STORE_WEB_IP_ADDRESS", cast=str)
PKG_STORE_WEB_PORT = config("PKG_STORE_WEB_PORT", cast=str)
LOCAL_IP_ADDRESS = config("LOCAL_IP_ADDRESS", cast=str)
LOCAL_PORT = config("LOCAL_PORT", cast=str)
LOCAL_SMB_PATH_TO_LIST_PKG = config("LOCAL_SMB_PATH_TO_LIST_PKG", cast=str)
RAWG_API_KEY = config("RAWG_API_KEY", cast=str)
PS_ADDRESSES = config("PS_ADDRESSES", cast=str)
DEBUG = config("DEBUG", cast=bool)
ignore_list = ['.DS_Store']

app = Flask(__name__)
app.config["SECRET_KEY"] = "mywebKey"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def root():
    return render_template("home.html")


@app.route("/game_list")
def game_list():
    games = os.listdir(LOCAL_SMB_PATH_TO_LIST_PKG)
    game_folder = []
    all_games = []
    for item in games:
        if os.path.isdir(os.path.join(LOCAL_SMB_PATH_TO_LIST_PKG, item)):
            game_folder.append(item)
            xml_path = os.path.join("assets/game_info", item+".xml")
            if not os.path.exists(xml_path):
                rawg_search(RAWG_API_KEY, item.replace("_", " "), xml_path)
                name = item
                background_image = "assets/images/icons/pkg.png"
                url = "game/"+item
            else:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                name = root.find("name").text
                background_image = root.find("background_image").text
                url = "game/"+item
            all_games.append({"name": name, "background_image": background_image, "url": url})
    return jsonify(all_games)


@app.route('/game/<path:path>', methods=['GET'])
def game(path):
    xml_path = os.path.join("assets/game_info", path+".xml")
    if not os.path.exists(xml_path):
        name = path
        background_image = "assets/images/icons/pkg.png"
    else:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        name = root.find("name").text
        background_image = root.find("background_image").text
    install_path = os.path.join(LOCAL_SMB_PATH_TO_LIST_PKG, path, "Install")
    if os.path.exists(install_path):
        install_btn = True
    else:
        install_btn = False

    update_path = os.path.join(LOCAL_SMB_PATH_TO_LIST_PKG, path, "Update")
    if os.path.exists(update_path):
        update_btn = True
    else:
        update_btn = False
    dlc_path = os.path.join(LOCAL_SMB_PATH_TO_LIST_PKG, path, "DLC")
    if os.path.exists(dlc_path):
        dlc_btn = True
    else:
        dlc_btn = False
    return render_template("game.html", background_image=background_image, name=name, install_btn=install_btn, update_btn=update_btn, dlc_btn=dlc_btn, game_path=path)


@app.route('/pkg_list/<path:path>', methods=['GET'])
def pkg_list(path):
    pkgs = os.listdir(os.path.join(LOCAL_SMB_PATH_TO_LIST_PKG, path))
    links = []
    for pkg in pkgs:
        links.append({"pkg": pkg, "path": path})
    return jsonify(links)


@app.route('/send_pkg/<path:path>', methods=['GET'])
def send_pkg(path):
    try:
        with open("ps_ip.txt", 'r') as file:
            ps_ip = file.read()
            file.close()
        response = package_sender(path, PKG_STORE_WEB_IP_ADDRESS, PKG_STORE_WEB_PORT, ps_ip)
        print(response)
        if response["status"] == "success":
            status = True
        else:
            status = False
        return jsonify({"success": status})
    except Exception as e:
        print(e)
        status = False
        return jsonify({"success": status})


@app.route('/update_ps_address', methods=['POST'])
def update_ps_address():
    try:
        ps_ip = request.form["ps_ip"]
        ps_ip_file = 'ps_ip.txt'
        with open(ps_ip_file, 'w') as file:
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
        with open("ps_ip.txt", 'r') as file:
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
                    ps_ip_file = 'ps_ip.txt'
                    with open(ps_ip_file, 'w') as file:
                        file.write(item2[1])
                        file.close()
        return jsonify({"success": True, "addresses": addresses})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@app.route('/assets/<path:path>', methods=['GET', 'POST'])
def send_assets(path):
    return send_from_directory('assets', path)


@app.route('/programs/<path:path>', methods=['GET', 'POST'])
def send_php(path):
    return send_from_directory('programs', path)


if __name__ == "__main__":
    app.run(host=LOCAL_IP_ADDRESS, port=LOCAL_PORT, debug=DEBUG)
