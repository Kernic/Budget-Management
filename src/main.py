import db.database as datab
import web.web as web

if __name__ == "__main__":
    info = datab.DataManagement()
    info.init_random()
    tmp = info.get_globals()
    website = web.website(tmp[0][1])
    website.run()