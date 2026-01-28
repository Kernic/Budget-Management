import os

import pandas as pds


def read_data() -> pds.DataFrame:
    with os.scandir("./res/data/uploaded") as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".csv"):
                dataset = pds.read_csv(
                    entry.path,
                    sep=";",
                    encoding="latin1",
                    decimal=",",
                    skiprows=10,
                    infer_datetime_format=True,
                )
                dataset = dataset.fillna(0)
                dataset = dataset.drop(len(dataset) - 10)
                return dataset
    raise FileNotFoundError("No CSV file found in the directory")


if __name__ == "__main__":
    print(read_data())
