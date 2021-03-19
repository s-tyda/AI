# Open file and write it to the list of stripped lines
data = [x.strip() for x in open("resources/Wnioski.txt").readlines()]
# data = list(map(str.strip, open("Wnioski.txt").readlines()))

# Add facts to the list
facts = data[-1].split(",")

# Add formulas to the list
formulas = []
for formula in data[:-2]:
    splitted_formula = formula.split()
    conditions = splitted_formula[1].split(",")
    conclusion = splitted_formula[3]
    formulas.append((conditions, conclusion))

# Make forward chaining
is_changed = True
while is_changed:
    is_changed = False
    for formula in formulas:
        conditions, fact = formula
        if all(x in facts for x in conditions) and fact not in facts:
            facts.append(fact)
            is_changed = True

# Print all of the facts as output
print(facts)
