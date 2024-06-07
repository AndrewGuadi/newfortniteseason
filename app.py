from flask import Flask, render_template, request, jsonify, flash, Response
from flask_wtf.csrf import CSRFProtect
import stripe
import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# CSRF Protection setup
csrf = CSRFProtect(app)

# Secret key for Flask session
app.secret_key = os.urandom(24)

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
    with open('/workspaces/newfortniteseason/static/data/emotes.json') as f:
        emotes = json.load(f)
    return render_template('emotes.html', emotes=emotes)

@app.route('/medallions')
def medallions():
    with open('/workspaces/newfortniteseason/static/data/medallions.json') as f:
        medallions_data = json.load(f)
    return render_template('medallions.html', medallions=medallions_data)

@app.route('/pois')
def pois():
    with open('/workspaces/newfortniteseason/static/data/pois.json') as f:
        pois_data = json.load(f)
    return render_template('pois.html', pois=pois_data)

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

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return jsonify({'status': 'success'}), 200

def handle_checkout_session(session):
    # Here you could update your database or send a confirmation email
    print("Payment was successful for session ID:", session.id)

@app.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.get_json()
    selected_size = data.get('size') if data else None
    
    if selected_size:
        try:
            # Create a new Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Llama Leisure - Winning in Style',
                        },
                        'unit_amount': 1999,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://www.newfortniteseason.com/success',
                cancel_url='https://www.newfortniteseason.com/cancel',
            )
            return jsonify({'id': checkout_session.id}), 200
        except Exception as e:
            return jsonify(error=str(e)), 400
    else:
        return jsonify({'error': 'Size not provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
