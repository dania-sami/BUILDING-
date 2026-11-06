"""STADSLINS reproducible statistical analysis using Python standard library only."""
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs"
FIELDS = ("lighting", "activity", "maintenance", "safety")
AREAS = ("Sodermalm", "Solna", "Kista", "Ostermalm")

def load_data(path=None):
    path = Path(path) if path else OUTPUT / "validated.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("No observations found. Run python scripts/pipeline.py first.")
    for row in rows:
        for field in FIELDS:
            row[field] = int(row[field])
        if not 1 <= row["safety"] <= 5:
            raise ValueError("Safety ratings must be between 1 and 5.")
    return rows

def summarize(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["area"], row["time"])].append(row)
    result = []
    for (area, time), group in sorted(grouped.items()):
        result.append({
            "area": area, "time": time, "n": len(group),
            "mean_safety": round(statistics.mean(x["safety"] for x in group), 3),
            "mean_lighting": round(statistics.mean(x["lighting"] for x in group), 3),
            "mean_activity": round(statistics.mean(x["activity"] for x in group), 3),
            "mean_maintenance": round(statistics.mean(x["maintenance"] for x in group), 3)
        })
    return result

def solve_linear(matrix, vector):
    """Gaussian elimination with partial pivoting; raises for singular matrices."""
    n = len(vector)
    a = [list(map(float, row)) + [float(vector[i])] for i, row in enumerate(matrix)]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(a[j][i]))
        if abs(a[pivot][i]) < 1e-10:
            raise ValueError("Regression design matrix is singular.")
        a[i], a[pivot] = a[pivot], a[i]
        divisor = a[i][i]
        a[i] = [v / divisor for v in a[i]]
        for j in range(n):
            if j != i:
                factor = a[j][i]
                a[j] = [a[j][k] - factor*a[i][k] for k in range(n+1)]
    return [row[-1] for row in a]

def regression(rows):
    """Illustrative OLS: safety ~ lighting + activity + maintenance + time + area."""
    names = ["intercept", "lighting", "activity", "maintenance",
             "evening", "Solna", "Kista", "Ostermalm"]
    x = [[1.0, r["lighting"], r["activity"], r["maintenance"],
          float(r["time"] == "evening"),
          float(r["area"] == "Solna"), float(r["area"] == "Kista"),
          float(r["area"] == "Ostermalm")] for r in rows]
    y = [r["safety"] for r in rows]
    p = len(names)
    xtx = [[sum(row[i]*row[j] for row in x) for j in range(p)] for i in range(p)]
    xty = [sum(row[i]*v for row, v in zip(x, y)) for i in range(p)]
    coefficients = solve_linear(xtx, xty)
    predictions = [sum(a*b for a,b in zip(row, coefficients)) for row in x]
    mean_y = statistics.mean(y)
    ss_res = sum((a-b)**2 for a,b in zip(y,predictions))
    ss_tot = sum((v-mean_y)**2 for v in y)
    return {
        "n": len(rows), "r_squared": round(1-ss_res/ss_tot, 5) if ss_tot else None,
        "rmse": round(math.sqrt(ss_res/len(y)), 5),
        "coefficients": dict(zip(names, [round(v,5) for v in coefficients]))
    }

def render_svg(rows, path):
    """Dependency-free SVG boxplot: median, quartiles and min/max whiskers."""
    grouped = {a: sorted(r["safety"] for r in rows if r["area"] == a) for a in AREAS}
    def quantile(v, q):
        if not v: return None
        index = (len(v)-1)*q
        lo = int(index); hi = min(lo+1, len(v)-1)
        return v[lo] + (v[hi]-v[lo])*(index-lo)
    def y(value):
        return 335-(value-1)*63
    palette = ("#5c9eac", "#b9d9b6", "#f4c47e", "#b7a7e4")
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="450" viewBox="0 0 900 450">',
             '<rect width="900" height="450" fill="#fafaf8"/>',
             '<text x="450" y="35" text-anchor="middle" font-size="21" font-family="Arial" fill="#182c36">Synthetic perceived safety by area</text>']
    for tick in range(1,6):
        yy = y(tick)
        parts.append(f'<line x1="90" y1="{yy}" x2="840" y2="{yy}" stroke="#d8e0e2"/>')
        parts.append(f'<text x="70" y="{yy+5}" text-anchor="end" font-size="15" font-family="Arial">{tick}</text>')
    for i, (area, values) in enumerate(grouped.items()):
        if not values: continue
        xx = 175+i*175
        q1, median, q3 = [quantile(values, q) for q in (.25,.5,.75)]
        parts += [f'<line x1="{xx}" y1="{y(max(values))}" x2="{xx}" y2="{y(min(values))}" stroke="#243744" stroke-width="3"/>',
                  f'<rect x="{xx-43}" y="{y(q3)}" width="86" height="{max(1,y(q1)-y(q3))}" fill="{palette[i]}" stroke="#243744" stroke-width="2"/>',
                  f'<line x1="{xx-43}" y1="{y(median)}" x2="{xx+43}" y2="{y(median)}" stroke="#243744" stroke-width="3"/>',
                  f'<text x="{xx}" y="382" text-anchor="middle" font-size="16" font-family="Arial">{area}</text>']
    parts.append('<text x="450" y="425" text-anchor="middle" font-size="14" font-family="Arial" fill="#586a75">Fictional demonstration data. Not empirical findings.</text></svg>')
    path.write_text("\n".join(parts), encoding="utf-8")

def run():
    OUTPUT.mkdir(exist_ok=True)
    rows = load_data()
    summaries = summarize(rows)
    with (OUTPUT / "python_area_time_means.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    model = regression(rows)
    import json
    (OUTPUT / "python_regression.json").write_text(json.dumps({
        "notice": "Synthetic demonstration only; ordinal outcome modeled as numeric for illustration.",
        **model}, indent=2), encoding="utf-8")
    render_svg(rows, OUTPUT / "python_safety_by_area.svg")
    print("STADSLINS | Python statistical analysis")
    print("Synthetic demonstration data. NOT empirical findings.")
    for row in summaries:
        print(f"{row['area']:12} {row['time']:8} n={row['n']:3} "
              f"mean safety={row['mean_safety']:.2f} mean lighting={row['mean_lighting']:.2f}")
    print(f"Illustrative OLS: R²={model['r_squared']}, RMSE={model['rmse']}")
    print("Outputs: python_area_time_means.csv, python_regression.json, python_safety_by_area.svg")

if __name__ == "__main__":
    run()
