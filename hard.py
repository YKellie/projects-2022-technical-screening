"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: This challenge is EXTREMELY hard and we are not expecting anyone to pass all
our tests. In fact, we are not expecting many people to even attempt this.
For complete transparency, this is worth more than the easy challenge. 
A good solution is favourable but does not guarantee a spot in Projects because
we will also consider many other criteria.
"""
import json

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

# Bool: Determines if the course had been completed by the student
def find_course_in_courses_list(courses_list, course):
    if course in courses_list:
        return True
    return False

# Bool: Determines if an "OR" condition is satisfied
def valid_or_condition(courses_list, words, i):
    if words[i - 1] in courses_list or words[i + 1] in courses_list:
        return True
    
    # Check if next or if available 
    # case: ... or ... or ... where first two courses were not found
    if i + 2 > len(words):
        return False
    
    if words[i + 2] is "or":
        # recursively calls function
        return (valid_and_condition(courses_list, words, i + 2))
    return False

# Bool: determines if "AND" condiiton is satisfied
def valid_and_condition(courses_list, words, i):
    if words[i - 1] in courses_list and words[i + 1] in courses_list:
        return True
    return False

# Int: Calculates units of credits within completed comp courses based on a given level
def calc_uoc_in_level(courses_list, level):
    comp_course_level = "COMP" + level
    uoc = 0
    for course in courses_list:
        if comp_course_level in course:
            uoc += 6
    return uoc

# Bool: determines if "units of credit" condition is satisfied
def valid_units_of_credit(courses_list, words, i):
    uoc_required = int(words[i - 1])
    uoc = 0

    # Check extra conditions e.g. "in": COMP, level 1, level 3, (..., ..., ...)
    if i + 3 < len(words):
        if (words[i + 3] is "in"):
            # only comp courses
            if words[i + 4].lower() is "comp":
                for course in courses_list:
                    if "comp" in course.lower():
                        uoc += 6
            
            # level course req            
            elif i + 5 < len(words):
                level = words[i + 5].lower() 
                if level in ["1", "2", "3"]:
                    uoc = calc_uoc_in_level(courses_list, level)

            # range of courses that meet req  
            elif i + 4 < len (words): 
                if "(" in words[i + 4]:
                    j = i + 4 
                    while j < len(words):
                        course = words[j].split("(", ")")
                        if find_course_in_courses_list(courses_list, course):
                            uoc += 6
                        j += 1

    # No extra requirements 
    else: 
        uoc = len(courses_list) * 6
    
    if (uoc >= uoc_required):
        return True
    return False


def find_index(words, target):
    i = 0
    while i < len(words):
        if words[i] is target:
            return i
        i += 1
    return None


def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    # NOTE: All course codes are unique
    
    subjects_list = ["COMP", "DPST", "MTRN", "ELEC", "MATH"]
    # Find target course conditions in condition.txt
    conditions_list = []
    with open("./conditions.json") as f:
        CONDITIONS = json.load(f)
        conditions_list = CONDITIONS.split(":")
        f.close
    index = conditions_list.index(target_course)
    conditions_for_target_course = conditions_list[index + 1]
    
    # Validate if conditions have been met
    words = conditions_for_target_course.split(" ")
    # if there are no conditions
    if not words:
        return True
    # There are conditions
    else:
        i = 0
        condition_met = True
        while i < len(words) and condition_met:
            # validates "OR" condition
            word = words[i].lower()
            if word is "or":
                if not valid_or_condition:
                    return False
            # validate "AND" condition
            elif word is "and":
                if not valid_and_condition(courses_list, words, i):
                    return False
            # validate "units of credit condition"
            elif word is "units":
                if not valid_units_of_credit(courses_list, words, i):
                    return False

            # Find course codes if they are present in sourses list 
            else:
                course_code = word.split(subjects_list)
                # Find course codes
                if course_code.isdigit() and int(course_code > 1000):
                    if not (find_course_in_courses_list(courses_list, course_code)):
                        return False
            i += 1
        return True




    