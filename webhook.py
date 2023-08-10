from flask import Flask, request
import requests

app = Flask(__name__)

# Votre clé API Telegram pour envoyer des messages (le token apparait avec des :)
TELEGRAM_API_KEY = "TELEGRAM TOKEN"

# Votre identifiant Telegram pour recevoir les messages (doit commencer par -100)
TELEGRAM_CHAT_ID = "-1001836804819"

# Votre clé de protection pour valider les notifications
PROTECTION_KEY = "qbz5n2kfra8p0"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Vérifier si la clé de protection est correcte
    protection_key = data.get('protection_key')
    if protection_key != PROTECTION_KEY:
        return 'Invalid protection key'

    # Récupérer les données de la notification
    symbol = data['symbol']
    entry_price = data['price']
    direction = data['direction']
    # Ajoutez les autres données de notification à récupérer selon vos besoins
    entry_price = int(float(entry_price))

    # Calculer les niveaux de TP et de SL en fonction de la direction du trade
    if direction == 'buy':
        tp1 = entry_price +  3
        tp2 = entry_price +  5
        tp3 = entry_price +  8
        sl = entry_price - 4
    elif direction == 'sell':
        tp1 = entry_price - 3
        tp2 = entry_price - 5
        tp3 = entry_price - 8
        sl = entry_price + 4
    else:
        return 'Invalid direction'

    # Envoyer le message à Telegram
    message = f"🔊 {direction} {symbol}\nEntry :  "+ str(entry_price) + "\n✅TP1 : " + str(tp1) + "\n✅TP2 : " + str(tp2) + "\n✅TP3 : " + str(tp3) + "\n⛔️SL : " + str(sl)
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(telegram_url, params=params)

    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)