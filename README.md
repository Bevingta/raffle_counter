# raffle_counter
An application which cuts down the time it takes to parse through a spreadsheet of student sales by up to 80%

How it works:
1. Import the .xlsx file with students names and ticket sales
2. A student directory is loaded with the legal names of each student in the school
3. Reads through each students names and their cooresponding sales
4. If their name their legal name then it automatically adds their sales to a total count for that student
5. If their name is a nickname the user is prompted to enter their legal name
6. The nickname and the legal name are then tied and if the nickname is read it will automatically
   be associated with the student in the future
7. If a sale needs to be split between 2-4 students there is a function to do this by inputting "Split _"(2,3 or 4)
8. Categories are also available as "Apply to any" (no name provided) and "Problem Child" (unrecognizable name)
9. The totals of each student are given at the end along with a total of all sales for all students
