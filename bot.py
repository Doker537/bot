from flask import Flask, request, jsonify
from flask_cors import CORS
import vk_api
import random
import os  # <--- Добавь эту строку

app = Flask(__name__)
CORS(app)  # Разрешаем браузеру делать запросы к этому серверу

# НАСТРОЙКИ VK
VK_TOKEN = "vk1.a.fjzY_usU73FKHA70o_Vle0ToZJ_DksvK2CsqRvDNX6ag7HF464Gd2RVwsktxFwSZWaYTA1eY1N5UuaDO_opzJtAKT7yReflI_ZPJTORttKBhzeOvyZ7dPW0Pep10Z6kxJpOLA4xVgfoadbQ19RYekJJGuFoxeJ3BzyutxXod_R5yVSq2sV-pd1_vJ56M40BJ1CNBHBEzP5eOLDQx2OuYaQ"  # Получается в настройках сообщества (Работа с API)
USER_ID = "118818612"  # Кому придет сообщение (цифрами)


def send_vk_message(text):
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    vk.messages.send(
        user_id=USER_ID,
        message=text,
        random_id=random.getrandbits(64)
    )


@app.route('/send_to_vk', methods=['POST'])
def handle_form():
    data = request.json

    # Обновили текст сообщения: теперь тут "из 50"
    msg = (f"🚀 Новый результат в тренажёре!\n"
           f"👤 Студент: {data['firstName']} {data['lastName']}\n"
           f"✅ Решено задач: {data['score']} из 50")

    try:
        send_vk_message(msg)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Ошибка VK: {e}")
        return jsonify({"status": "error"}), 500


if __name__ == '__main__':
    # Получаем порт от Render, а если запускаем локально — используем 5000
    port = int(os.environ.get("PORT", 5000))
    print(f"Сервер запускается на порту {port}...")
    app.run(host='0.0.0.0', port=port)
