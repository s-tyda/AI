# Open file and write it to the list of stripped lines
data = [x.strip() for x in open("resources/baza-wiedzy-negacja.txt").readlines()]

# Add facts to the list
facts = data[-1].split(",")

# Add formulas to the list
formulas = []
for formula in data[:-2]:
    splitted_formula = formula.split("->")
    conclusion = splitted_formula[1]
    splitted_formula = splitted_formula[0].split(".")
    conditions = splitted_formula[1].split(",")
    formulas.append((conditions, conclusion))

hypothesis = input("Jaką hipotezę sprawdzić?\n")


# Function that checks thesis using backtracking
def backtracking(thesis):
    if thesis in facts:
        return True
    for formula in [x for x in formulas if x[1] == thesis]:
        conditions = formula[0]
        if all([not backtracking(x[1]) if x.startswith("~") else backtracking(x) for x in conditions]):
            return True
    return False


# Print True if thesis is satisfied
print(backtracking(hypothesis))
