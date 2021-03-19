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


# Make forward chaining
is_changed = True
while is_changed:
    is_changed = False
    for formula in formulas:
        conditions, fact = formula
        check = True
        for condition in conditions:
            if condition.startswith("~"):
                condition = condition[1:]
                if condition in facts:
                    check = False
                    if fact in facts:
                        facts.remove(fact)
                        is_changed = True
            else:
                if condition not in facts:
                    check = False

        if check and fact not in facts:
            facts.append(fact)
            is_changed = True

# Print all of the facts as output
print(facts)
