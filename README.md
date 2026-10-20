# Spring Math

Ideal spring arithmetic. A spring rated 2.5 N/mm pushes back with 30 N when it is compressed 12 mm, and stores 180 mJ.

## What it computes

All numbers have at most one decimal place. Rate is 0.1 to 1000 N/mm, compression 0.1 to 1000 mm, force 0.1 to 10000 N.

- **The force truth** - rate times compression, in newtons.
- **The energy truth** - the energy stored, half the rate times the compression squared, in millijoules.
- **The travel truth** - the compression that gives a force, force divided by rate.
- **The pair truth** - two springs side by side (rates add) and end to end (compliances add).

## Boundary

Arithmetic only. A spring is treated as a straight line from rate and compression. It does not know any real spring, where its rate stops being a straight line, how far it can travel before it bottoms out, how long it will last, or whether a part is safe to build with it, and it gives no verdict on any of that. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on tenths, half-up rounding).
- `oracle.py` - the Python mirror (Fractions, summed slices for energy, added compliances for series) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/springmath/
Repo: https://github.com/iLanis-agent/springmath
