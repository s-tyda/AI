# Open file and write it to the list of stripped lines
data = [x.strip() for x in open("resources/Wnioski.txt").readlines()]

# Add facts to the list
facts = data[-1].split(",")

# Add formulas to the list
formulas = []
for formula in data[:-2]:
    splitted_formula = formula.split()
    conditions = splitted_formula[1].split(",")
    conclusion = splitted_formula[3]
    formulas.append((conditions, conclusion))

hypothesis = input("Jaką hipotezę sprawdzić?\n")


# Function that checks thesis using backtracking
def backtracking(thesis):
    if thesis in facts:
        return True
    for idx, formula in enumerate(formulas):
        conclusion = formula[1]
        if thesis == conclusion:
            conditions = formula[0]
            if all(backtracking(x) for x in conditions):
                return True
    return False


# Print True if thesis is satisfied
print(backtracking(hypothesis))
