from flask import Flask, request, jsonify
from flask_cors import CORS
import vk_api
import random

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
    print("Сервер запущен на http://127.0.0.1:5000")
    app.run(port=5000)