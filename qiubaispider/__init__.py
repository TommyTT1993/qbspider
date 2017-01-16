import ConfigParser
PATH = "/etc/config/secret.ini"
cf = ConfigParser.ConfigParser()
cf.read(PATH)
MONGOUSER = cf.get("mongo", "user")
MONGOPASS = cf.get("mongo", "pass")
