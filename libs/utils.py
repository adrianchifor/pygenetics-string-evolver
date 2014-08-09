import random
import bisect


def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += 1/float(w) if w > 0 else 0
        totals.append(running_total)

    rnd = random.random() * running_total
    return bisect.bisect_right(totals, rnd)   
