# To test in repl
# dict = {"key":"item"}
# dog_1 = {"name":"Castle", "age":5, "breed":"Golden Retriever"}
# dog_2 = {"name":"Blessing", "age":5, "breed":"Golden Retriever"}
#
# dog_1["color"] = "gold"
#
# dog_1["age"] = 6
#
#
# myString = "Castle"

def verify_identity(dict):
    if dict["name"] == "Castle":
        print("This dog is Castle.")
    else:
        print("This dog is not Castle.")


def str_to_dict(s):
    "turns a string into a dictionary with letters corresponding to item numbers"
    # dict[key] = value
    myDict = {}
    position = 0
    for letter in s:
        myDict[position] = letter
        position += 1
    return myDict


class Dog:
    def __init__(self, name):
        self.name = name

