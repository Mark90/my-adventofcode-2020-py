from collections import defaultdict

from collections import defaultdict


def part1(lines, full):
    # 2317
    allergen_ingredients = {}
    all_ing = set()
    ingcount = defaultdict(int)
    for l in lines:
        ing, alg = l.rstrip(")").split(" (contains ")
        all_ing.update(ing.split())
        for i in ing.split():
            ingcount[i] += 1
        for a in alg.split(", "):
            if a not in allergen_ingredients:
                allergen_ingredients[a] = set(ing.split())
            else:
                allergen_ingredients[a] &= set(ing.split())

    safe = all_ing.copy()
    for k, v in allergen_ingredients.items():
        safe -= v
    # Return sum of safe ingredient occurrences
    return sum(ingcount[s] for s in safe)


def part2(lines, full):
    # kbdgs,sqvv,slkfgq,vgnj,brdd,tpd,csfmb,lrnz
    allergen_ingredients = {}
    all_ing = set()
    for l in lines:
        ing, alg = l.rstrip(")").split(" (contains ")
        all_ing.update(ing.split())
        for a in alg.split(", "):
            if a not in allergen_ingredients:
                allergen_ingredients[a] = set(ing.split())
            else:
                allergen_ingredients[a] &= set(ing.split())

    # Deduce which allergen comes from which ingredient
    while any(len(v) > 1 for v in allergen_ingredients.values()):
        len_1 = {k: v for k, v in allergen_ingredients.items() if len(v) == 1}
        ones = set([i for v in len_1.values() for i in v])
        for k, v in allergen_ingredients.items():
            if k in len_1:
                continue
            v -= ones

    result = []
    for key in sorted(allergen_ingredients.keys()):
        vv = list(allergen_ingredients[key])
        result.append(vv[0])
    return ",".join(result)
