import io
import random
import string

import numpy as np
import pandas as pds
import sqlite3
from sqlite3 import Error

class DataManagement:
    raw_data = None
    def __init__(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect("../res/db/main.db")
        except Error as e:
            print (f"Error {e}")

    def __open_data__(self, path: str):
        # Transforming the raw data to a more usable data
        raw_data = pds.read_csv(path, encoding="cp1252", skiprows=10, sep=';', engine="c").drop("Unnamed: 4", axis=1)
        for col in ["Débit euros", "Crédit euros"]:
            raw_data[col] = raw_data[col].str.replace(",", ".").str.replace("\xa0", "").astype("float32")
        raw_data = raw_data.fillna(0)
        raw_data["operation"] = raw_data["Crédit euros"] - raw_data["Débit euros"]
        raw_data.drop("Crédit euros", axis=1, inplace=True)
        raw_data.drop("Débit euros", axis=1, inplace=True)

        raw_data["operation type"] = raw_data["Libellé"].apply(
            lambda x : x.split("\n")[0].strip()
        )
        raw_data["operator"] = raw_data["Libellé"].apply(
            lambda x : x.split("\n")[1].split(" ")[0].strip()
            if x.split("\n")[1].split(" ")[0].strip().startswith("X") else "OTHER"
        )
        raw_data["name"] = raw_data["Libellé"].apply(
            lambda x : ' '.join(x.split("\n")[1].split(" ")[1:]).strip()
            if x.split("\n")[1].split(" ")[0].strip().startswith("X") else x.split("\n")[1]
        )
        raw_data.drop("Libellé", axis=1, inplace=True)

        raw_data = raw_data[["name", "operation type", "operator", "operation", "Date"]]

        print(raw_data.to_numpy().tolist())
        return raw_data

    def init_random(self):
        random_data_list = {
            "name": [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(100)],
            "operation type": [random.choices(["CB", "Virement", "Prelevement"])[0] for _ in range(100)],
            "operator": [random.choices(["Person A", "Person B", "Other"])[0] for _ in range(100)],
            "operation": [random.uniform(-1000.00, 1000.00) for _ in range(100)],
            "Date": [random.choices(["01/01/2026", "05/01/2026", "08/08/2026", "07/12/2025"])[0] for _ in range(100)]
        }
        random_data = pds.DataFrame(random_data_list)
        print(random_data)
        if type(self.connection) != type(None):
            random_data.to_sql(name="raw_data", con=self.connection, if_exists="replace")
        pass

    def import_data(self):
        data = self.__open_data__(r"../res/db/tmp/data.csv")
        if type(self.connection) != type(None):
            data.to_sql(name="raw_data", con=self.connection, if_exists="replace")

    def close(self):
        self.connection.close()

    def open(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect("../res/db/main.db")
        except Error as e:
            print (f"Error {e}")