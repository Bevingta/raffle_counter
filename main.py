#imports the library you need to read the files
import json
import pandas as pd
from legal_names import legal_names
import time


#creates a dictionary for problem children
problem_children = []
problem_children_sales = []

def words_to_year(name, word, year):
    name = name.replace(word, '')
    name = name.strip()
    name = name.title()
    return name + " '" + year

#gets the year of the student
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

    #checks for word version of class years
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

#splits the sales between x number of students
def split_sales(num, sale):
    i = 1
    while i <= num:
        if i == 1:
            first = input("First students name: ")
            if first.lower() == "back":
                return False
            if first not in legal_names:
                print(f"{first} not found in directory")
                print("Ensure you put the year in the correct format")
                first = input("First students name: ")
        elif i == 2:
            second = input("Second students name: ")
            if second.lower() == "back":
                return False
            if second not in legal_names:
                print(f"{second} not found in directory")
                print("Ensure you put the year in the correct format")
                second = input("Second students name: ")
        elif i == 3:
            third = input("Third students name: ")
            if third.lower() == "back":
                return False
            if third not in legal_names:
                print(f"{third} not found in directory")
                print("Ensure you put the year in the correct format")
                third = input("Third students name: ")
        elif i == 4:
            fourth = input("Fourth students name: ")
            if fourth.lower() == "back":
                return False
            if fourth not in legal_names:
                print(f"{fourth} not found in directory")
                print("Ensure you put the year in the correct format")
                fourth = input("Fourth students name: ")
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

    return True


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
print("'Back' - Goes back one step")
print("'Split 2' - Splits the sales between two students")
print("'Split 3' - Splits the sales between three students")
print("'Split 4' - Splits the sales between four students")
print("'Apply to any' (case sensitive) - Adds the sale to the 'Apply to any' category")
print("'Skip' - If the name is unrecognizable. Flags and returns the name at the end. Adds their sale to a separate category for totaling.")
print(" ")

#TODO
unrecognized = 0
recognized = 0
total = 0

# Get the current time (start time)
start_time = time.time()

#reads through the names in the column 'Name' and checks them against the legal name list
col_name = "Name"
for row, name in enumerate(df[col_name]):
    #gets the sale value for the student
    sale = df.iat[row, 3]
    #TODO
    total += sale

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

            #looks for the special commands
            if legal.lower() == "split 2":
                split = split_sales(2, sale)
                if split:
                    entering_name = False
            elif legal.lower() == "split 3":
                split = split_sales(3, sale)
                if split:
                    entering_name = False
            elif legal.lower() == "split 4":
                split = split_sales(4, sale)
                if split:
                    entering_name = False

            elif legal.lower() == "skip":
                problem_children.append(name)
                problem_children_sales.append(sale)
                legal_names["Skipped"] += sale
                entering_name = False

            #if no special commands triggered then makes it a nickname
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

#TODO (add back in total here)

#prints the names and total sales of all students in the Excel
for name in legal_names:
    if legal_names[name] > 0:
        print(f"{name}: {legal_names[name]}")


#prints the total sales
print("")
print(f"Total Sales: {total}")
print("")

#prints the skipped kids and their totals
if len(problem_children) > 0:
    print("Skipped:")
    for idx, name in enumerate(problem_children):
        print(f"{name}: {problem_children_sales[idx]}")

    print("")
    print("")


# Get the current time again (end time)
end_time = time.time()

# Calculate the elapsed time in seconds
elapsed_time = end_time - start_time

print(f"Elapsed Time: {elapsed_time} seconds")



