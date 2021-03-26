from flask import Flask, render_template, request, jsonify
import base64

app = Flask(__name__)

# function to encode
def Encode(key, message):
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))

    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


# function to decode
def Decode(key, message):
    dec = []
    message = base64.urlsafe_b64decode(message).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))

    return "".join(dec)

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
       message = request.form.get("msg")
       key = request.form.get("key")
       type = request.form.get("encdec")

       if type == 'e':
           encrptMessage = Encode(key, message)
           output = {
               "Encrypted Message": encrptMessage
           }
           return jsonify(output)

       elif type == 'd':
           decrpytMessage = Decode(key, message)
           output = {
               "Decrypted Message": decrpytMessage
           }
           return jsonify(output)

    return render_template("main.html")

if __name__ == '__main__':
   app.run(debug = True)