# Open file and write it to the list of stripped lines
data = [x.strip() for x in open("resources/Wnioski.txt").readlines()]
# data = list(map(str.strip, open("Wnioski.txt").readlines()))

# Add facts to the list
facts = data[-1].split(",")

# Add formulas to the dictionary, where conclusions are keys
formulas = {}
for formula in data[:-2]:
    splitted_formula = formula.split()
    conditions = splitted_formula[1].split(",")
    conclusion = splitted_formula[3]
    if conclusion not in formulas:
        formulas.update({conclusion: []})
    formulas[conclusion].append(conditions)


def check_formula(formula):
    # Function to check a single formula
    return all(x in facts for x in formula)


# Make forward chaining
is_changed = True
while is_changed:
    is_changed = False
    for fact in formulas:
        if fact not in facts and any(check_formula(formula) for formula in formulas[fact]):
            facts.append(fact)
            is_changed = True

# Print all of the facts as output
print(facts)
