from diff_match_patch import diff_match_patch
from datetime import date

"""
# Generate the difference file for two files and save it
@param filename1: The name of the first file (should be today)
@param filename2: The name of the second file (should be yesterday)
"""
def generate_diff(filename1, filename2):


    today = date.today().strftime("%d_%m_%y")
    outfile_name = filename2.split("_")[-1].replace(".js","")
    #print("Outname" + outfile_name)
    outfile_name = "differences/diff_" + outfile_name + "_" + today +".diff"



    js_file1 = open(filename1)
    js_file2 = open(filename2)

    js1 = js_file1.read()
    js2 = js_file2.read()


    dmp = diff_match_patch()
    dmp.Diff_Timeout = 0
    diffs = dmp.diff_main(js1,js2)
    dmp.diff_cleanupSemantic(diffs)

    patches = dmp.patch_make(diffs)
    #print(diffs)
    #diff = dmp.patch_toText(diffs)
    #html = dmp.diff_prettyHtml(diffs)

    print("[INFO] Writing diff file to: " + outfile_name)
    js_file1.close()
    js_file2.close()


    with open(outfile_name, "w") as output_file:
        output_file.writelines(dmp.patch_toText(patches))
