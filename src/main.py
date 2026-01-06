import db.database as datab
import web.web as web

if __name__ == "__main__":
    info = datab.DataManagement()
    website = web.website()
    info.import_data()
    website.run()