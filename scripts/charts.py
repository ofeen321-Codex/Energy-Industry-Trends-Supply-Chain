#!/usr/bin/env python3
"""Rebuild report charts from reviewed data; never scrape numbers into findings."""
import csv
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".research-cache" / "matplotlib"
CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".research-cache" / "xdg"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUT = ROOT / "charts"
OUT.mkdir(exist_ok=True)
with (ROOT / "data" / "chart_data.csv").open(newline="") as stream:
    ROWS = list(csv.DictReader(stream))

TEAL = "#147D92"
ORANGE = "#C56C19"
GRAY = "#718096"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "svg.fonttype": "none", "figure.facecolor": "white"})


def rows(chart):
    return [r for r in ROWS if r["chart"] == chart]


def save(fig, name, footnote, left=.09):
    fig.text(.07, .035, footnote, fontsize=9, color="#475569", va="bottom")
    fig.subplots_adjust(left=left, right=.96, bottom=.24, top=.80)
    for suffix in ["png", "svg"]:
        path = OUT / f"{name}.{suffix}"
        fig.savefig(path, dpi=180)
        if suffix == "svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)
    print(name)


data = rows("wholesale-price-dispersion")
fig, ax = plt.subplots(figsize=(10, 5.6))
bars = ax.bar([r["label"] for r in data], [float(r["value"]) for r in data],
              color=ORANGE, width=.55)
ax.axhline(0, color="#334155", lw=.9)
ax.set_ylim(-35, 55)
ax.set_ylabel("2026 vs. 2025 price change (%)")
ax.bar_label(bars, labels=[f'{float(r["value"]):+.0f}%' for r in data], padding=6)
fig.suptitle("Wholesale power: location changes the outlook", x=.07, ha="left", weight="bold", fontsize=17)
ax.set_title("Selected 2026 full-year forecasts; not retail bill changes", loc="left", fontsize=11, pad=18)
save(fig, "wholesale-price-dispersion",
     "Source: EIA October 6, 2026 STEO, electricity section (A01). All bars are forecasts.\nU.S. measure is EIA's 11-hub average; selected regional extremes are not the full distribution.")

data = rows("transformer-domestic-coverage")
fig, ax = plt.subplots(figsize=(10, 5.6))
bars = ax.barh([r["label"].replace(" transformers", "\ntransformers") for r in data], [float(r["value"]) for r in data],
               color=TEAL, height=.48)
ax.set_xlim(0, 100)
ax.set_xlabel("Domestic production as a share of U.S. demand (%)")
ax.bar_label(bars, labels=[r["value"] + "%" for r in data], padding=7)
ax.invert_yaxis()
fig.suptitle("U.S. transformer demand relies on global supply", x=.07, ha="left", weight="bold", fontsize=17)
ax.set_title("Reported 2025 estimates; not a forecast of unmet demand", loc="left", fontsize=11, pad=18)
save(fig, "transformer-domestic-coverage",
     "Source: RMI, May 8, 2026 (S09), 'Supply chain constraints'.\nImports help cover remaining demand. Equipment categories and individual quotes differ.", left=.22)

data = rows("battery-utilization")
fig, ax = plt.subplots(figsize=(10, 5.6))
bars = ax.bar([r["label"] for r in data], [float(r["value"]) for r in data],
              color=[TEAL if r["evidence_type"] == "reported_estimate" else "white" for r in data],
              edgecolor=[TEAL if r["evidence_type"] == "reported_estimate" else GRAY for r in data], width=.55)
bars[-1].set_hatch("///")
ax.set_ylim(0, 420)
ax.set_ylabel("Cycles per year")
ax.bar_label(bars, labels=[r["value"] for r in data], padding=6)
fig.suptitle("Battery installation is only part of the opportunity", x=.07, ha="left", weight="bold", fontsize=17)
ax.set_title("China, 2025: actual utilization estimates vs. optimization benchmark", loc="left", fontsize=11, pad=18)
save(fig, "battery-utilization",
     "Source: Ember, July 16, 2026 (S07), key takeaways.\n350 cycles is a modeled benchmark, not observed performance or a forecast for all batteries.")

data = rows("fuel-price-outlook")
fig, axes = plt.subplots(1, 2, figsize=(11, 5.8))
for ax, metric, title, unit in zip(axes, ["brent", "henry_hub"], ["Brent crude oil", "Henry Hub natural gas"],
                                 ["Dollars per barrel", "Dollars per MMBtu"]):
    group = [r for r in data if r["metric"] == metric]
    bars = ax.bar([r["period"] for r in group], [float(r["value"]) for r in group], width=.58,
                  color=[TEAL if r["evidence_type"] == "historical" else ORANGE for r in group])
    ax.set_title(title, loc="left", weight="bold")
    ax.set_ylabel(unit)
    ax.set_ylim(0, max(float(r["value"]) for r in group) * 1.28)
    ax.bar_label(bars, labels=[r["value"] for r in group], padding=5)
fig.suptitle("Fuel benchmarks: EIA projects easing, with disruption risk", x=.07, ha="left", weight="bold", fontsize=16)
fig.legend(handles=[Patch(facecolor=TEAL, label="Historical"), Patch(facecolor=ORANGE, label="Forecast")],
           loc="upper right", bbox_to_anchor=(.95, .92), ncol=2, frameon=False)
save(fig, "fuel-price-outlook",
     "Source: EIA October 6, 2026 STEO (D01/A02/A03). Annual averages; different axes and units.\n2027 extends beyond the report's Oct. 23 horizon. Forecast assumes recovering supply; not a guarantee.")

data = rows("regional-gas-benchmarks")
fig, ax = plt.subplots(figsize=(10, 5.8))
labels = [r["label"].replace(" Henry Hub", "\nHenry Hub").replace(" TTF", "\nTTF").replace(" LNG imports", "\nLNG imports") for r in data]
bars = ax.barh(labels, [float(r["value"]) for r in data], color=TEAL, height=.52)
bars[-1].set_hatch("///")
ax.set_xlim(0, 31)
ax.invert_yaxis()
ax.set_xlabel("U.S. dollars per MMBtu")
ax.bar_label(bars, labels=[r["value"] for r in data], padding=6)
fig.suptitle("Regional gas: same units, different benchmarks", x=.07, ha="left", weight="bold", fontsize=17)
ax.set_title("September 2026; not equivalent delivered industrial contracts", loc="left", fontsize=11, pad=18)
save(fig, "regional-gas-benchmarks",
     "Source: World Bank Pink Sheet, Oct. 2, 2026 (B01), monthly values and definitions.\nJapan is estimated LNG import price including cost, insurance and freight; hatched bar is an estimate.", left=.20)

data = rows("solar-generation-costs")
fig, ax = plt.subplots(figsize=(10, 5.8))
bars = ax.bar([r["label"] for r in data], [float(r["value"]) for r in data], color=TEAL, width=.58)
ax.set_ylim(0, 80)
ax.set_ylabel("2025 U.S. dollars per MWh")
ax.bar_label(bars, labels=[r["value"] for r in data], padding=6)
fig.suptitle("Solar generation cost is not a procurement quote", x=.07, ha="left", weight="bold", fontsize=16)
ax.set_title("IRENA 2025 project-based weighted generation LCOE estimates", loc="left", fontsize=11, pad=18)
save(fig, "solar-generation-costs",
     "Source: IRENA Renewable Power Generation Costs in 2025, July 2026 summary (B09), Fig. S3.\nNot a retail tariff, PPA offer, battery cost or firm 24-hour electricity price; markets have different inputs.")
