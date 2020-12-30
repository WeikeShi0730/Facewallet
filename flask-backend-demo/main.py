from flask import Flask, jsonify, request, json
import time

app = Flask("__main__")


@app.route("/register", methods=['POST'])
def register():
    data = json.loads(request.data, strict=False)
    if "photo" in data:
        register_photo(data)
    else:
        register_info(data)
    return data


def register_info(info_data):
    time.sleep(1)
    return info_data, 201


def register_photo(photo_data):
    time.sleep(5)
    return photo_data, 201


@app.route("/register", methods=['GET'])
def register_message():
    info = True
    photo = True
    message = "ok" if (info and photo) else "nok"
    return jsonify({'message': message})


@app.route("/payment")
def payment():
    return "payment"
