import pymongo
import os

class Database():
    def __init__(self, url: str = os.getenv("MONGO_URL")) -> None:
        self.url = url
        dbClient = pymongo.MongoClient(self.url)
        self.db = dbClient.echotron
        
    def getName(self):
        return self.db.name
    
    def checkGuild(self, guildId: str):
        data = self.db.guilds.find_one({ "_id": guildId })
        return data
    
    def addGuild(self, guildId: str):
        getData = self.checkGuild(guildId)
        if getData is None:
            data = self.db.guilds.insert_one({ "_id": guildId, "users": [] })
            return data
        else:
            return getData
    
    def checkUserData(self, userId: str):
        data = self.db.users.find_one({ "_id": userId })
        return data
        
    def addUserData(self, userId: str):
        getData = self.checkUserData(userId)
        if (getData is None):
            data = self.db.users.insert_one({ "_id": userId })
            print(data)
        else:
            print('User already has data')