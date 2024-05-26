from flask import Flask, render_template, Response, url_for, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/theme')
def theme():
    return render_template('theme.html')

@app.route('/skins')
def skins():
    with open('/workspaces/newfortniteseason/static/data/skins.json') as f:
        skins = json.load(f)

    return render_template('skins.html', skins=skins)

@app.route('/vehicles')
def vehicles():
    with open('/workspaces/newfortniteseason/static/data/vehicle_mods.json') as f:
        vehicle_mods = json.load(f)
    
    with open('/workspaces/newfortniteseason/static/data/mod_boxes.json') as f:
        mod_boxes = json.load(f)

    return render_template('vehicles.html', vehicle_mods=vehicle_mods, mod_boxes=mod_boxes)


@app.route('/emotes')
def emotes():
    return render_template('emotes.html')

@app.route('/guests')
def guests():
    return render_template('guests.html')

@app.route('/epic')
def epic():
    return render_template('epic.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/weapons')
def weapons():
    items_path = '/workspaces/newfortniteseason/static/data/items.json'
    with open(items_path) as f:
        items_data = json.load(f)

    weapons_path = '/workspaces/newfortniteseason/static/data/weapons.json'
    with open(weapons_path, "r", encoding='utf-8') as f:
        weapons_data = json.load(f)
    return render_template('weapons.html', weapons=weapons_data, items=items_data)

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    current_time = datetime.now().strftime("%Y-%m-%d")

    # Add static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            priority = '1.0' if rule.rule == '/' else '0.8'
            pages.append(
                ["https://www.newfortniteseason.com" + str(rule.rule), current_time, priority]
            )

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    return Response(sitemap_xml, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)

