from typing import Union
import simplejson as json
import os

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def read_xml(path: str) -> str:
    """
    Reads xml file from a given path

    Args:
        path (str): path to the xml file

    Returns:
        str: data contained in the xml file
    """

    with open(path, 'r') as f:
        data = f.read()
    f.close()

    return data


def convert_value(item: str) -> Union[float, str]:
    """
    Converts an element to type float or str

    Args:
        item (str): element to be converted

    Returns:
        Union[float, str]: returned value
    """
    if len(item) > 0:
        try:
            return float(item)
        except:
            return item
    else:
        return np.nan


def get_file_id(path: str, name: str, ext: str) -> int:
    """
    Finds id of a file to be saved

    Args:
        path (str): path where file will be saved
        name (str): name to be found in files in path
        ext (str): file extension

    Returns:
        int: file id
    """
    ids = 0
    files = os.listdir(path)

    for f in files:
        if (name in f) & (f.endswith(ext)):
            ids += 1
    return ids


def parse_xml(
    xml_object: str,
    save_path: str = None,
    ) -> None:
    """
    Parse witsml data from a given sting containing xml file data

    Args:
        xml_object (str): string contraining parsed xml data
        save_path (str): path where to save parsed objects
    """

    xml_object = BeautifulSoup(xml_object, 'xml')

    try:

        mnemonics_dict = {
            k: v for k, v in zip(
                xml_object.findChildren('mnemonicList')[0].get_text().split(","), 
                xml_object.findChildren('unitList')[0].get_text().split(",")
                )}

        fname = xml_object.findChildren('name')[0].get_text()

        data = {k: [] for k, v in mnemonics_dict.items()}
        for row in xml_object.findChildren('data'):
            row  = row.get_text().split(",")
            row = [convert_value(item) for item in row]
            for (_, v), item in zip(data.items(), row):
                v.append(item)

        data = pd.DataFrame.from_dict(data)
        if len(data) > 0:

            
            ids = get_file_id(save_path, fname, ".json")

            with open(os.path.join(save_path, f"{fname}_{ids}.json"), "w") as f:
                json.dump(mnemonics_dict, f)
            f.close()

            ids = get_file_id(save_path, fname, ".csv.gz")

            data.to_csv(os.path.join(save_path, f"{fname}_{ids}.csv.gz"), index=False)
            
    except Exception as e:
        pass