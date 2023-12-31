#imports the library you need to read the files
import json
import pandas as pd

excel_file_name = "StudentDatabase.xlsx"

legal_names_imported = {}
nicknames_imported = {}

first_step = True
while first_step:
    try:
        #excel_file_name = input("File Name (include '.xlsx' at the end): ")
        df = pd.read_excel(excel_file_name)
        first_step = False
    except FileNotFoundError:
        print("File Not Found. Make sure that you downloaded it to the same place as this python file")

#reads through the names in the column 'Name' and checks them against the legal name list
col_name = "Last name"
for row, last in enumerate(df[col_name]):
    print(last)
    #gets the sale value for the student
    first = df.iat[row, 1]
    print(first)
    grade = df.iat[row, 4]
    print (grade)
    grade = f"'{grade%2000}"

    name = f"{first} {last} {grade}"
    print(name)

    #adding legal names to legal_names_imported
    legal_names_imported[name] = 0

    nickname = df.iat[row, 3]
    print(nickname)

    if not pd.isnull(nickname):
        nickname_add = f"{nickname} {last} {grade}"
        nicknames_imported[nickname_add] = name

print("")
print("Saving Nicknames...")
with open('nicknames.json', 'w') as file:
    json.dump(nicknames_imported, file, indent=4)
print("Done")

#writes the new sales values into the file
print("")
print("Saving Sales...")
with open("venv/legal_names.py", "w") as out:
    out.write("legal_names = {\n")
    for name, sales in legal_names_imported.items():
        out.write(f'    "{name}":{int(sales)},\n')
    out.write("}\n")
print("Done")
print("")

