"""hack file list to remove extensions"""

# pylint: disable=line-too-long

input_list = []
output_list = []

x = "EOF"
with open("pdfs/all_pdfs.txt", "r", encoding="utf-8") as f:
    while x != "":
        x = f.readline()
        print("read", x)
        input_list.append(x)

for z in input_list:
    y_tuple = z.partition(".")
    print("found", y_tuple)
    y = y_tuple[0]
    community_name = '"'+y+'", '
    output_list.append(community_name)

with open("pdfs/all_files.txt", "w", encoding="utf-8") as f:
    for y in output_list:
        f.writelines(y)

