# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import ConfigParser
class Config:
    PATH = "/etc/config/secret.ini"
    MONGOUSET = ""
    MONGOPASS = ""
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read(self.PATH)
        self.MONGOUSET = cf.get("mongo", "user")
        self.MONGOPASS = cf.get("mongo", "pass")


