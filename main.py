#imports the library you need to read the files
import json
import pandas as pd
from legal_names import legal_names

problem_children = []

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
        name = words_to_year(name, 'senior', '24')
        return name
    elif "junior" in name:
        name = words_to_year(name, 'junior', '25')
        return name
    elif "sophomore" in name:
        name = words_to_year(name, 'sophomore', '26')
        return name
    elif "sophmore" in name:
        name = words_to_year(name, 'sophmore', '26')
        return name
    elif "freshman" in name:
        name = words_to_year(name, 'freshman', '27')
        return name
    else:
        return name


def split_sales(num, sale):
    i = 1
    while i <= num:
        if i == 1:
            first = input("First students name: ")
            if first not in legal_names:
                print(f"{first} not found in directory")
                print("Ensure you put the year in the correct format")
                first = input("First students name: ")
        elif i == 2:
            second = input("Second students name: ")
            if second not in legal_names:
                print(f"{second} not found in directory")
                print("Ensure you put the year in the correct format")
                second = input("Second students name: ")
        elif i == 3:
            third = input("Third students name: ")
            if third not in legal_names:
                print(f"{third} not found in directory")
                print("Ensure you put the year in the correct format")
                third = input("Third students name: ")
        elif i == 4:
            fourth = input("Fourth students name: ")
            if fourth not in legal_names:
                print(f"{fourth} not found in directory")
                print("Ensure you put the year in the correct format")
                third = input("Fourth students name: ")
        i += 1
    if num == 2:
        sale = sale / 2
        legal_names[first] += sale
        legal_names[second] += sale

    elif num == 3:
        sale = sale / 3
        legal_names[first] += sale
        legal_names[second] += sale
        legal_names[third] += sale

    elif num == 4:
        sale = sale / 4
        legal_names[first] += sale
        legal_names[second] += sale
        legal_names[third] += sale
        legal_names[fourth] += sale


#sets all values to 0 for student counts
for name in legal_names:                    #if this stays in could delete save function to delete the need for this one too
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

print("")
print("Special Commands:")
print("'Split 2' - Splits the sales between two students")
print("'Split 3' - Splits the sales between three students")
print("'Split 4' - Splits the sales between four students")
print("'Apply to any' (case sensitive) - Adds the sale to the 'Apply to any' category")
print("'Problem Child' (case sensitive) - If the name is unrecognizable.")
print(" Flags and returns the name at the end. Adds their sale to a separate category for totaling.")

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
        print("")
        print(f"Unrecognized Name: {name}")
        entering_name = True
        while entering_name:
            legal = input(f"What is this {name}'s legal name?\nInclude the graduation year (e.g. '25 at the end)\n")


            if legal.lower() == "split 2":
                split_sales(2, sale)
                entering_name = False
            elif legal.lower() == "split 3":
                split_sales(3, sale)
                entering_name = False
            elif legal.lower() == "split 4":
                split_sales(4, sale)
                entering_name = False

            elif legal in legal_names:
                if legal == "Problem child":
                    problem_children.append(name)
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

total = 0

for name in legal_names:
    print(f"{name}: {legal_names[name]}")
    total += legal_names[name]

print("")
print(f"Total Sales: {total}")


if len(problem_children) > 0:
    print("Problem Children:")
    for name in problem_children:
        print(name)


