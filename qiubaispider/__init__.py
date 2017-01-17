import configparser
PATH = "/etc/config/secret.ini"
cf = configparser.ConfigParser()
cf.read(PATH)
MONGOUSER = cf.get("mongo", "user")
MONGOPASS = cf.get("mongo", "pass")
