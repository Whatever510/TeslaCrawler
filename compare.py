import difflib
from datetime import date

from diff_match_patch import diff_match_patch


def generate_diff_custom(filename1, filename2, country_code=""):
    today = date.today().strftime("%d_%m_%y")
    outfile_name = filename2.split("_")[-1].replace(".js", "")
    outfile_name = "differences/" + country_code + "/diff_" + outfile_name + "_" + today + ".diff"

    with open(filename1, "r") as file1, open(filename2, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

        diff = difflib.unified_diff(lines2, lines1)

    with open(outfile_name, "w") as output_file:
        for line in diff:
            output_file.writelines(line)
