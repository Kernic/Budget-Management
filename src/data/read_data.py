import os

import db
import pandas as pds


def read_data() -> pds.DataFrame:
    with os.scandir("../res/data/uploaded") as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".csv"):
                get_global_values(entry.path)
                dataset = pds.read_csv(
                    entry.path,
                    sep=";",
                    encoding="latin1",
                    decimal=",",
                    skiprows=10,
                )
                dataset["Crédit euros"] = (
                    dataset["Crédit euros"]
                    .str.replace(",", ".")
                    .str.replace("\xa0", "")
                    .astype(float)
                )
                dataset["Débit euros"] = (
                    dataset["Débit euros"]
                    .str.replace(",", ".")
                    .str.replace("\xa0", "")
                    .astype(float)
                )
                dataset = dataset.fillna(0)
                dataset["amount"] = dataset["Crédit euros"] - dataset["Débit euros"]
                dataset["date"] = pds.to_datetime(dataset["Date"], dayfirst=True)
                dataset["description"] = dataset["Libellé"]
                dataset["category"] = dataset["Libellé"].str.split("\n").str[0]
                dataset = dataset.drop(
                    columns=[
                        "Date",
                        "Libellé",
                        "Crédit euros",
                        "Débit euros",
                        "Unnamed: 4",
                    ],
                    axis=1,
                )
                dataset = pds.DataFrame(
                    dataset[["date", "description", "amount", "category"]]
                )
                return dataset
    raise FileNotFoundError("No CSV file found in the directory")


def get_global_values(path: str) -> None:
    with open(path, "r", encoding="latin1") as file:
        first_lines = file.readlines()[:10]
    balance = float(
        first_lines[6].split(" ")[-2].strip().replace("\xa0", "").replace(",", ".")
    )
    first_date, last_update = (
        first_lines[8]
        .split("Liste des opérations du compte entre le ")[1]
        .split(" et le ")
    )
    last_update = last_update.replace(";\n", "")
    db.update_value("global_values", "value", 1, str(balance))
    db.update_value("global_values", "value", 3, first_date)
    db.update_value("global_values", "value", 2, last_update)


if __name__ == "__main__":
    db.drop_tables()
    db.create_tables()
    db.insert_values_as_dataframe("operations", read_data())
