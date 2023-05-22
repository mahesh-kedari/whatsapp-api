from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


uri = "mongodb+srv://kedarimahesh:F5CjYo9u0Z7a4ipI@shorelinecluster.pudipmm.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to server
print(f"connecting to {uri}")
cluster = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
try:
    print("Pinging to mongo server")
    cluster.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Printing exception")
    print(e)

db = cluster["shorelinecloud"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def respond_to_alarm():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    print(f"Request received from user {number}")
    user = users.find_one({"number": number})
    response = MessagingResponse()
    try:
        if bool(user) == False:
            msg = response.message("Hi, Thanks for connecting *Shoreline IoT* \n "
                            "Monitor your assets with our advanced Prescriptive maintainance servce. \n"
                            "To get started *type*\n"
                            "1️⃣ To *List your sites* \n"
                            "2️⃣ To *List your devices* \n" 
                            "3️⃣ To get *Vibration workflow* \n"
                            "4️⃣ To get *Asset Image* \n"
                            )
            msg.media("https://static.wixstatic.com/media/9dae82_a009238d26164b1193c51903d19e5a7e~mv2.png")
            users.insert_one({"number":number, "status": "first_visit", "messages": []})
        elif user["status"] == "first_visit":
            try:
                option = int(text)
            except:
                response.message("Please enter a valid response")
                return str(response)

            if option == 1:
                response.message("List your sites\n"
                                 "1️⃣ DCP Midstream\n"
                                 "2️⃣ GE Appliances\n"
                                 "3️⃣ Microsoft Corporations\n"
                                 "4️⃣ Amazon\n"
                                 "5️⃣ Google\n"
                                 "6️⃣ Apple\n"
                                 "7️⃣ LinkedIn\n"
                                 "8️⃣ Facebook\n"
                                 "9️⃣ Twitter\n"
                                 "1️⃣0️⃣ Instagram\n"
                                 )
            elif option == 2:
                response.message("List your sites\n"
                                 "1️⃣ Compressor 1\n"
                                 "2️⃣ Motor 2\n"
                                 "3️⃣ Compressor 3\n"
                                 "4️⃣ Engine 4\n"
                                 )
            elif option == 3:
                msg = response.message("Vibration Analysis")
                msg.media("https://cdn.shopify.com/s/files/1/0417/5439/4787/articles/IS9_2048x.jpg")
            elif option == 4:
                # https://www.sl-energie.com/files/template/img/engines/anwendungen/kompressorantrieb/q8-terminal/Q8T%20IMG_9601_ret.jpg
                msg = response.message("Asset Image")
                msg.media("https://www.sl-energie.com/files/template/img/engines/anwendungen/kompressorantrieb/q8-terminal/Q8T%20IMG_9601_ret.jpg")
    except Exception as e:
        print(e)
        response.message("Error has occurred");
    return str(response)


if __name__ == "__main__":
    app.run()