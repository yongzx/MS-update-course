import csv
import re
import pprint

course_catalog_u = list()
course_desc_u = list()
course_name_u = list()
course_prerequisite_u = list()
course_short_name_u = list()
catalog_college_name_u = list()

with open("updated_course_data.csv", "r+", encoding="utf-8") as updated_course_data:
    updated = csv.reader(updated_course_data)
    next(updated)
    for i in updated:
        course_catalog_u.append(i[0])
        course_desc_u.append(i[1])
        course_name_u.append(i[2])
        course_prerequisite_u.append(i[3])
        course_short_name_u.append(i[4])
        catalog_college_name_u.append(i[5])

code_to_desc = dict(zip(course_catalog_u, course_desc_u))
code_to_name = dict(zip(course_catalog_u, course_name_u))
code_to_pre = dict(zip(course_catalog_u, course_prerequisite_u))
code_to_college = dict(zip(course_catalog_u, catalog_college_name_u))

# print(course_updated)

course_code_w = list()
course_name_w = list()
course_desc_w = list()
college_name_w = list()

with open("website_course_data.csv", "r+", encoding="utf-8") as website_course_data:
    website = csv.reader(website_course_data)
    next(website)
    for i in website:
        course_code_w.append(i[0])
        course_name_w.append(i[1])
        course_desc_w.append(i[2])
        college_name_w.append(i[3])

name_to_code = {
    "Arts and Humanities": "AH",
    "Computational Sciences": "CS",
    "Natural Sciences": "NS",
    "Social Sciences": "SS",
    "Business": "B"
}
for i, n in enumerate(college_name_w):
    course_code_w[i] =  name_to_code[n] + course_code_w[i]


# courses to be removed
remove_code_L = list()
for i, code in enumerate(course_code_w):
    if code not in code_to_desc:
        remove_code_L.append(i)

code_to_remove = [code for i, code in enumerate(course_code_w) if i in remove_code_L]
name_to_remove = [name for i, name in enumerate(course_name_w) if i in remove_code_L]
desc_to_remove = [desc for i, desc in enumerate(course_desc_w) if i in remove_code_L]
college_to_remove = [name for i, name in enumerate(college_name_w) if i in remove_code_L]
pprint.pprint(code_to_remove)
pprint.pprint(name_to_remove)


# add course
code_add_L = list()
name_add_L = list()
desc_add_L = list()
college_name_add_L = list()
for code in (set(course_catalog_u) - set(course_code_w)):
    code_add_L.append(code)
    name_add_L.append(course_name_u[course_catalog_u.index(code)])
    desc_add_L.append(course_desc_u[course_catalog_u.index(code)])
    college_name_add_L.append(catalog_college_name_u[course_catalog_u.index(code)])

pprint.pprint(list(zip(*[code_add_L, name_add_L, desc_add_L, college_name_add_L])))



# check description change
for i, code in enumerate(course_code_w):
    if code in code_to_desc:
        if (course_desc_w[i]) != code_to_desc[code] and (course_desc_w[i][:course_desc_w[i].find("**")].rstrip()) != code_to_desc[code]:
            print("Original: ", course_code_w[i])
            print(course_desc_w[i][:course_desc_w[i].find("**")].rstrip() if course_desc_w[i].find("**") > 10 else course_desc_w[i])
            print()
            print("Updated: ", course_code_w[i])
            print(code_to_desc[code])
            print("-----")

# check prerequisite
for i, desc in enumerate(course_desc_w):
    preq_pos = course_desc_w[i].find("**Prerequisite:**")
    if preq_pos == -1 and not code_to_pre[course_code_w[i]]:
        pass
    elif desc[preq_pos+17:].rstrip() != code_to_pre[course_code_w[i]]:
        print("Original: ", desc[preq_pos+17:].rstrip())
        print("Updated: ", code_to_pre[course_code_w[i]])
    elif preq_pos == -1 and code_to_pre[course_code_w[i]]:
        print("Original: None")
        if code_to_pre[course_code_w[i]].lower()[:2] != "co":
            print("Prerequisite: ", code_to_pre[course_code_w[i]])
        else:
            print(code_to_pre[course_code_w[i]])
    else:
        print()
    print("--------------")


# check names
for i, name in enumerate(course_name_w):
    if course_code_w[i] in code_to_name and name != code_to_name[course_code_w[i]]:
        print("Original: ", course_code_w[i])
        print(name)
        print()
        print("Updated:", course_code_w[i])
        print(code_to_name[course_code_w[i]])
        print("----------")

