# To test in repl
# dict = {"key":"item"}
# dog_1 = {"name":"Castle", "age":5, "breed":"Golden Retriever"}
# dog_2 = {"name":"Blessing", "age":5, "breed":"Golden Retriever"}
# dog_1["color"] = "gold"
# dog_1["age"] = 6
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

class Pet:
    def __init__(self, name, energy = 0, happiness = 0):
        self.name = name
        self.energy = energy
        self.happiness = happiness

    def __repr__(self):
        return f'Pet(name={self.name}, energy={self.energy}, happiness={self.happiness}, weight={self.weight})'

    def __str__(self):
        return f"{self.name} is {self.energy} with {self.happiness} happiness."

    def health(self, bcs):
        "returns pet's health based upon bcs input"
        self.bcs = bcs
        if bcs < 6:
            self.weight = 'healthy'
            self.energy += 1
        else:
            self.weight = 'unhealthy'
            self.energy -=1
        return self.weight, self.energy

    def feed(self):
        "every time function is run, pet is fed"
        self.energy += 1
        return self.energy

    def play(self):
        "every time function is run, pet gets to play."
        self.energy -= 1
        self.happiness += 1
        return self.energy, self.happiness

    def check_energy(self):
        "checks pet's energy."
        print("Your pet's energy is {self.energy}.")

    def check_happiness(self):
        "checks pet's happiness."
        print("Your pet's happiness is {self.happiness}.")