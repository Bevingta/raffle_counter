#imports the library you need to read the files
import json
import pandas as pd
from legal_names import legal_names


def words_to_year(name, word, year):
    name = name.replace(word, '')
    name = name.strip()
    name = name.title()
    return name + " '" + year

def get_year(name):
    year = ""
    for letter in name:
        if letter.isnumeric():
            year += letter
            name = name.replace(letter, "")
        elif not letter.isnumeric() and not letter.isalpha():
            name = name.replace(letter, " ")
    name = name.strip()
    if len(year) == 2 and int(year) > 20:
        return name + " '" + year
    elif len(year) == 4:
        year = year[2:4]
        return name + " '" + year

    name = name.lower()
    if "senior" in name:
        words_to_year(name, 'senior', '24')
    elif "junior" in name:
        words_to_year(name, 'junior', '25')
    elif "sophomore" in name:
        words_to_year(name, 'sophomore', '26')
    elif "sophmore" in name:
        words_to_year(name, 'sophmore', '26')
    elif "freshman" in name:
        words_to_year(name, 'freshman', '27')
    else:
        return name


def split_sales(num):
    i = 1
    while i <= num:
        None


#just for testing to set them all back to 0
for name in legal_names:                     #DELETE BEFORE SENDING#
    legal_names[name] = 0

with open("nicknames.json", "r") as file:
    nicknames = json.load(file)

#opens an Excel file and reads the content
first_step = True
while first_step:
    try:
        excel_file_name = input("File Name (include '.xlsx' at the end): ")
        df = pd.read_excel(excel_file_name)
        first_step = False
    except FileNotFoundError:
        print("File Not Found. Make sure that you downloaded it to the same place as this python file")

#reads through the names in the column 'Name' and checks them against the legal name list
col_name = "Name"
for row, name in enumerate(df[col_name]):
    #gets the sale value for the student
    sale = df.iat[row, 2]

    #formats the year automatically
    name = get_year(name)

    #checks if the name is their legal name
    if name in legal_names:
        legal_names[name] += sale

    #checks if their name is a nickname
    elif name in nicknames:
        legal = nicknames[name]
        legal_names[legal] += sale

    #triggered if it is not a legal name or nickname
    else:
        print(f"Unrecognized Name: {name}")
        entering_name = True
        while entering_name:
            print("")
            legal = input(f"What is this {name}'s legal name?\nInclude the graduation year (e.g. '25 at the end)\n")

            if legal == "Split 2":
                split_sales(2)
            elif legal in legal_names:
                legal_names[legal] += sale
                entering_name = False
                nicknames[name] = legal

            else:
                print("Entered name not found")

#writes the new nicknames into the file
print("")
print("Saving Nicknames...")
with open('nicknames.json', 'w') as file:
    json.dump(nicknames, file, indent=4)
print("Done")

#writes the new sales values into the file
print("")
print("Saving Sales...")
with open("legal_names.py", "w") as out:
    out.write("legal_names = {\n")
    for name, sales in legal_names.items():
        out.write(f'    "{name}":{int(sales)},\n')
    out.write("}\n")
print("Done")
print("")

for name in legal_names:
    print(f"{name}: {legal_names[name]}")


