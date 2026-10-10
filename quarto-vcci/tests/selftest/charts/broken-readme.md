# Broken README examples (layer 8 self-test)

An example that fails to run (misspelt function):

```python
import matplotlib.pyplot as plt
import vcci_charts as vcci
vcci.uze()
fig, ax = plt.subplots()
ax.bar(["2024", "2025"], [66.0, 67.4])
fig.savefig("broken-run.svg")
```

An example that runs but forgets the VCCI style (matplotlib's default colours):

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.bar(["2024", "2025"], [66.0, 67.4])
fig.savefig("default-colours.svg")
```
