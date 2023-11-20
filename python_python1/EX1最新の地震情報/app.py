from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# 地震情報取得関数
def get_earthquake_info():
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'

    try:
        response = requests.get(p2pquake_url)
        response.raise_for_status()
        earthquake_info = response.json()[0]  # 最新の地震情報を取得
        return earthquake_info
    except requests.RequestException as e:
        print(f"Error fetching earthquake data: {e}")
        return None

# 地震情報をクライアントに送信する関数
def send_earthquake_info():
    while True:
        info = get_earthquake_info()
        if info:
            magnitude = info.get("earthquake", {}).get("magnitude")
            if magnitude and magnitude >= 5.0: #マグニチュード
                socketio.emit('new_earthquake', {'magnitude': magnitude})
        socketio.sleep(30) #30秒ごとに

# 地震情報送信用スレッドの開始
threading.Thread(target=send_earthquake_info, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
