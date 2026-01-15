from pymongo import MongoClient
import certifi
uri = "mongodb+srv://saurabh123:oSe4BijxpjKIfnKX@cluster0.rc3hanw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

print(client.admin.command("ping"))