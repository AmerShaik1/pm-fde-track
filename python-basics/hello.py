name = "Amer"
age = 36
is_learning_python = True

print("Hello",name)
print("You are",age,"years old")
print("Currently learning Python:", is_learning_python)

next_year_age = age + 1
print("Next year you'll be", next_year_age)

years_until_50 = 50 - age
print("Years until 50:", years_until_50)

hours_per_week = 10
weeks = 6
total_hours = hours_per_week * weeks
print("Total study hours:", total_hours)

split_three_ways = total_hours / 3
print("Hours per person if split 3 ways:", split_three_ways)

students = 7
groups_of = 3

full_groups = students // groups_of
leftover = students % groups_of

print("Full groups of 3:", full_groups)
print("Students left over:", leftover)

total_tasks = 100
tasks_per_day = 8

full_days = total_tasks // tasks_per_day
left_over = total_tasks % tasks_per_day

#print("No. of full days:",full_days)
#print("No. of left over days:", left_over)

message = f"{full_days} are full days and {left_over} are left over days"
print(message)

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

for i in range(5):
    print("Iteration number:", i)

count = 0
while count < 3:
    print("Count is:",count)
    count += 1

skills = ["Product Management", "Git", "Python"]

print(skills)
print(skills[0])
print(skills[1])

skills.append("SQL")
print(skills)

for skill in skills:
    print("I know",skill)

def greet(person_name):
    print(f"Hello, {person_name}!")

greet("Amer")
greet("Sara")
greet("Team")
greet(18)

def calculate_age_in_days(years):
    days=years*365
    return days
#age_in_days=calculate_age_in_days(36)
#print(f"You are {age_in_days} days old")
years = int(input("Enter your age in years: "))
age_in_days = calculate_age_in_days(years)
print(age_in_days)

profile = {
    "name": "Amer",
    "age": 36,
    "role": "PM/FDE apprentice"
}

print(profile["name"])
print(profile["age"])
print(profile["role"])

profile["role"] = "PM/FDE Candidate"
profile["location"] = "Georgia"

for key in profile:
    print(key,":",profile[key])
