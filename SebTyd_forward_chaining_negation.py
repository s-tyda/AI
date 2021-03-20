# Open file and write it to the list of stripped lines
data = [x.strip() for x in open("resources/baza-wiedzy-negacja-2.txt").readlines()]

# Add facts to the list
facts = data[-1].split(",")

# Add formulas to the dictionary, where conclusions are keys
formulas = {}
for formula in data[:-2]:
    splitted_formula = formula[2:].split("->")
    conclusion = splitted_formula[1]
    conditions = splitted_formula[0].split(",")
    if conclusion not in formulas:
        formulas.update({conclusion: []})
    formulas[conclusion].append(conditions)


def check_formula(formula):
    # Function to check a single formula
    return all(x[1] not in facts if x.startswith("~") else x[0] in facts for x in formula)


# Make forward chaining
is_changed = True
while is_changed:
    is_changed = False
    for fact in formulas:
        if fact in facts and not any(check_formula(x) for x in formulas[fact]):
            facts.remove(fact)
            is_changed = True
        elif fact not in facts and any(check_formula(x) for x in formulas[fact]):
            facts.append(fact)
            is_changed = True

# Print all of the facts as output
print(facts)
