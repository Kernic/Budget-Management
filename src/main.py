import db.database as datab
import web.web as web

if __name__ == "__main__":
    info = datab.DataManagement()
    website = web.website()
    info.init_random()
    website.run()