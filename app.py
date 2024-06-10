from flask import Flask, render_template, request, jsonify, flash, Response, url_for, redirect
from flask_wtf.csrf import CSRFProtect
import stripe
import os
import json
from datetime import datetime
from forms import CheckoutForm
import stripe 

# Initialize Flask app
app = Flask(__name__)

# CSRF Protection setup
csrf = CSRFProtect(app)

# Secret key for Flask session
app.secret_key = os.urandom(24)
stripe.api_key = os.getenv('testapikey')


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

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    form = CheckoutForm()
    if form.validate_on_submit():
        # Define shipping rates
        shipping_options = [
            {
                'shipping_rate_data': {
                    'type': 'fixed_amount',
                    'fixed_amount': {
                        'amount': 699,  # Amount in cents
                        'currency': 'usd'
                    },
                    'display_name': 'Ground Shipping',
                    'delivery_estimate': {
                        'minimum': {
                            'unit': 'business_day',
                            'value': 7
                        },
                        'maximum': {
                            'unit': 'business_day',
                            'value': 10
                        }
                    }
                }
            },
            {
                'shipping_rate_data': {
                    'type': 'fixed_amount',
                    'fixed_amount': {
                        'amount': 1299,  # Amount in cents
                        'currency': 'usd'
                    },
                    'display_name': 'Expedited Shipping',
                    'delivery_estimate': {
                        'minimum': {
                            'unit': 'business_day',
                            'value': 3
                        },
                        'maximum': {
                            'unit': 'business_day',
                            'value': 5
                        }
                    }
                }
            }
        ]

        # Create a new Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                    },
                    'unit_amount': 2999,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://fuzzy-umbrella-wj647wrrp7p2w94-5000.app.github.dev/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cancel', _external=True),
            shipping_address_collection={
                'allowed_countries': ['US']
            },
            shipping_options=shipping_options,
            phone_number_collection={
                "enabled": True
            },
            metadata={
                'shirt_size': form.shirt_size.data,
            }
        )
        return redirect(session.url, code=303)
    return render_template('shop.html', form=form)

@app.route('/success', methods=['GET', 'POST'])
def success():
    session_id = request.args.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    shirt_size = session.metadata['shirt_size']
    return render_template('success.html', shirt_size=shirt_size)

@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    return render_template('cancel.html')

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
