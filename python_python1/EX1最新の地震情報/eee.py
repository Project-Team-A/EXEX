import requests
import json
import RPi.GPIO as GPIO
import threading

def get_earthquake_info():
    api_url = "https://www.jma.go.jp/bosai/quake/data/list.json"
    response = requests.get(api_url)
    data = response.json()
    latest_earthquake = data[0]
    return float(latest_earthquake["magnitude"])

def activate_buzzer(buzzer_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    try:
        while not stop_buzzer.is_set():
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()

def main():
    try:
        buzzer_pin = 17
        stop_buzzer.clear()

        # ブザーを鳴らすスレッドを開始
        buzzer_thread = threading.Thread(target=activate_buzzer, args=(buzzer_pin,))
        buzzer_thread.start()

        while True:
            magnitude = get_earthquake_info()

            if magnitude >= 5.0:
                print("地震発生！ Enterキーを押してブザーを停止してください.")
                input()  # Enterキーが押されるまで待機

                # ブザーを停止
                stop_buzzer.set()
                buzzer_thread.join()

                # ブザーのピンをクリーンアップ
                GPIO.cleanup()

                # スレッドを再作成して新たな地震の発生を待つ
                stop_buzzer.clear()
                buzzer_thread = threading.Thread(target=activate_buzzer, args=(buzzer_pin,))
                buzzer_thread.start()

            time.sleep(300)  # 5分ごとに地震情報を確認

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    stop_buzzer = threading.Event()
    main()