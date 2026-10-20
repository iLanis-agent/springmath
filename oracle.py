#!/usr/bin/env python3
# Spring Math oracle - mirrors engine.js with Fractions: force is rate times compression, energy is the area under the line found by summing thin slices, series rate comes from adding compliances (1/k), rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

RATE = "the spring rate must be from 0.1 to 1000 N/mm with at most one decimal place"
RATE2 = "the second spring rate must be from 0.1 to 1000 N/mm with at most one decimal place"
MM = "the compression must be from 0.1 to 1000 mm with at most one decimal place"
FORCE = "the force must be from 0.1 to 10000 N with at most one decimal place"
def dec(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,5}(\.[0-9])?", t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def txt(fr, places):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10 ** places); fs = str(fp).zfill(places).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
def k_(t): return dec(t, RATE, "0.1", "1000")
def x_(t): return dec(t, MM, "0.1", "1000")

def force(a, b):
    k = k_(a); x = x_(b)
    return f"A spring rated {txt(k,1)} N/mm pushes back with {txt(k * x, 2)} N when it is compressed {txt(x,1)} mm."
def energy(a, b):
    k = k_(a); x = x_(b)
    n = 2000; area = F(0)                      # sum of thin slices of the force line, trapezoids are exact for a straight line
    for i in range(n):
        x0, x1 = x * i / n, x * (i + 1) / n
        area += (k * x0 + k * x1) / 2 * (x1 - x0)
    assert area == k * x * x / 2
    return f"Compressed {txt(x,1)} mm, a spring rated {txt(k,1)} N/mm stores {txt(area, 2)} mJ."
def travel(a, b):
    k = k_(a); f = dec(b, FORCE, "0.1", "10000")
    x = f / k
    assert k * x == f
    return f"To push back with {txt(f,1)} N, a spring rated {txt(k,1)} N/mm is compressed {txt(x, 2)} mm."
def pair(a, b):
    k1 = k_(a); k2 = dec(b, RATE2, "0.1", "1000")
    series = 1 / (1 / k1 + 1 / k2)             # compliances add
    return f"Two springs rated {txt(k1,1)} and {txt(k2,1)} N/mm add up to {txt(k1 + k2, 1)} N/mm side by side, and give {txt(series, 2)} N/mm end to end."

FNS = {"forceTruth": force, "energyTruth": energy, "travelTruth": travel, "pairTruth": pair}

def cases():
    c = []
    rates = ["0.1", "1", "2.5", "10", "33.3", "100", "999.9", "1000", " 2.5 "]
    mms = ["0.1", "1", "12", "12.5", "50", "333.3", "999.9", "1000"]
    for k in rates:
        for x in mms[::2] + ["12.5"]:
            c.append(("forceTruth", [k, x])); c.append(("energyTruth", [k, x]))
    for k in rates:
        for f in ["0.1", "30", "7.7", "100", "10000", "9999.9"]: c.append(("travelTruth", [k, f]))
    for a in ["0.1", "2.5", "10", "1000", "33.3"]:
        for b in ["0.1", "3.5", "10", "1000", "7.7"]: c.append(("pairTruth", [a, b]))
    for k, x in [("0.1", "0.1"), ("0.3", "0.3"), ("1", "0.1"), ("0.7", "1.1"), ("3", "0.5")]:
        c += [("forceTruth", [k, x]), ("energyTruth", [k, x])]
    bad = ["", "x", "0", "0.0", "0.05", "1.25", "1000.1", "10001", "-1", ".5", "5.", "1e2", "100000"]
    for v in bad:
        c += [("forceTruth", [v, "12"]), ("energyTruth", [v, "12"]), ("travelTruth", [v, "30"]), ("pairTruth", [v, "3.5"]),
              ("forceTruth", ["2.5", v]), ("energyTruth", ["2.5", v]), ("pairTruth", ["2.5", v])]
    for v in ["", "x", "0", "0.05", "10000.1", "100000", "-5", "1.25"]: c.append(("travelTruth", ["2.5", v]))
    r = random.Random(709)
    for _ in range(12):
        k = f"{r.randint(0, 999)}.{r.randint(0, 9)}"; x = f"{r.randint(0, 999)}.{r.randint(0, 9)}"; f = f"{r.randint(0, 9999)}.{r.randint(0, 9)}"
        if k == "0.0": k = "0.1"
        if x == "0.0": x = "0.1"
        if f == "0.0": f = "0.1"
        c += [("forceTruth", [k, x]), ("energyTruth", [k, x]), ("travelTruth", [k, f]), ("pairTruth", [k, x])]
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":")) for o in out) + "\n]\n")
print(len(out), "cases written")
