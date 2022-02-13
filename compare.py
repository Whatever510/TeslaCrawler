""" This script calculated a diff file of the two provided files"""

import difflib
from datetime import date


def generate_diff_custom(filename1, filename2, country_code=""):
    """
    Generate the diff file for the two given files
    :param filename1: The first filename
    :param filename2: The second filename
    :param country_code: The country code for the diff file
    """
    today = date.today().strftime("%d_%m_%y")
    outfile_name = filename2.split("_")[-1].replace(".js", "")
    outfile_name = "differences/" + country_code + "/diff_" + outfile_name + "_" + today + ".diff"

    with open(filename1, "r", encoding="utf-8") as file1,\
            open(filename2, 'r', encoding="utf-8") as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

        diff = difflib.unified_diff(lines2, lines1)

    with open(outfile_name, "w", encoding="utf-8") as output_file:
        for line in diff:
            output_file.writelines(line)
