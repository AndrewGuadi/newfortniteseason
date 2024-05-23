from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/theme')
def theme():
    return render_template('theme.html')

@app.route('/skins')
def skins():
    return render_template('skins.html')

@app.route('/vehicles')
def vehicles():
    return render_template('vehicles.html')

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

if __name__ == '__main__':
    app.run(debug=True)
