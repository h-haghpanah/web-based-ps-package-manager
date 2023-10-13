
from flask import Flask,render_template,send_from_directory,jsonify
import os
import configparser
from api import rawg_search,package_sender
import xml.etree.ElementTree as ET

dirname = os.path.dirname(__file__)
config = configparser.RawConfigParser()
config_path = os.path.join(dirname,"./config.ini")
config.read(config_path)

web_server_ip = config.get("web_info","ip")
web_server_port = config.get("web_info","port")

pkg_path = config.get("pkg","path")

api_key = config.get("rawg","api_key")
igone_list = ['.DS_Store']
# Upload_attachment = os.path.abspath(os.path.dirname(__file__))+"/assets/images/fund_attachments"
# Gallery_attachment = os.path.abspath(os.path.dirname(__file__))+"/assets/images/project_gallery"


app = Flask(__name__)
app.config["SECRET_KEY"] = "mywebKey"
# app.config["ATTACHMENT_UPLOADS"] =Upload_attachment
# app.config["GALLERY_UPLOADS"] =Gallery_attachment


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




@app.route("/")
def root():
    # games = os.listdir("/Users/hesam/Desktop/pkg")
    # igone_list = ['.DS_Store']
    # game_list = ""
    # for item in games:
    #     game_list += '<div class="row" style="flex-direction: row-reverse;">'+\
    #     '</div>'
    return render_template("home.html")

@app.route("/game_list")
def game_list():
    games = os.listdir(pkg_path)
    game_folder = []
    all_games = []
    for item in games:
        if os.path.isdir(os.path.join(pkg_path, item)):
            game_folder.append(item)
            xml_path = os.path.join("assets/game_info", item+".xml")
            if  not os.path.exists(xml_path):
                rawg_search(api_key,item.replace("_"," "),xml_path)
                name = item
                background_image = "assets/images/icons/pkg.png"
                url = "game/"+item
            else:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                name = root.find("name").text
                # game_rating = root.find("rating").text
                # game_released = root.find("released").text
                background_image = root.find("background_image").text
                url = "game/"+item
            all_games.append({"name":name,"background_image":background_image,"url":url})

            

    return jsonify(all_games)
    
@app.route('/game/<path:path>' , methods=['GET', 'POST'])
def game(path):
    xml_path = os.path.join("assets/game_info", path+".xml")
    if  not os.path.exists(xml_path):
        name = path
        background_image = "assets/images/icons/pkg.png"
    else:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        name = root.find("name").text
        background_image = root.find("background_image").text
    install_path = os.path.join(pkg_path, path, "Install")
    if os.path.exists(install_path):
        install_btn = True
        # pkgs = os.listdir(install_path)
        # install_links = ""
        # for pkg in pkgs:
        #     install_links += f'<a href="/send_pkg/{path}/Install/{pkg}" class="btn btn-primary">{pkg}</a>'
    else:
        install_btn = False
        # install_links = ""
    
    update_path = os.path.join(pkg_path, path, "Update")
    if os.path.exists(update_path):
        update_btn = True
        pkgs = os.listdir(update_path)
        # update_links = ""
        # for pkg in pkgs:
        #     update_links += f'<a href="/send_pkg/{path}/Update/{pkg}" class="btn btn-primary">{pkg}</a>'
    else:
        update_btn = False
        # update_links = ""
        
    dlc_path = os.path.join(pkg_path, path, "DLC")
    if os.path.exists(dlc_path):
        dlc_btn = True
        # pkgs = os.listdir(dlc_path)
        # dlc_links = ""
        # for pkg in pkgs:
        #     dlc_links += f'<a href="/send_pkg/{path}/Update/{pkg}" class="btn btn-primary">{pkg}</a>'
    else:
        dlc_btn = False
        # dlc_links  = ""
        
    return render_template("game.html",background_image=background_image,name=name,install_btn=install_btn,update_btn=update_btn,dlc_btn=dlc_btn,game_path=path)

@app.route('/pkg_list/<path:path>' , methods=['GET', 'POST'])
def pkg_list(path):
    pkgs = os.listdir(os.path.join(pkg_path, path))
    # path = path.split("/")
    # folder = path[1]
    links = []
    for pkg in pkgs:
        links.append({"pkg":pkg,"path":path})
    return jsonify(links)

@app.route('/send_pkg/<path:path>' , methods=['GET', 'POST'])
def send_pkg(path):
    package_sender(path,web_server_ip,web_server_port,"172.16.5.60")
    return jsonify({"success":True})

#############################################
#############################################
################## ASSETS ###################
#############################################
#############################################


@app.route('/assets/<path:path>' , methods=['GET', 'POST'])
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/programs/<path:path>' , methods=['GET', 'POST'])
def send_php(path):
    return send_from_directory('programs', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=True)