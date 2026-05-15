import csv
import json
from pathlib import Path


def save_csv(rows: list[dict], out_file: Path) -> None:
    with out_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["runtime", "benchmark", "time_ms", "memory_kb"])
        writer.writeheader()
        writer.writerows(rows)


def build_chart_dataset(rows: list[dict], metric: str) -> dict:
    labels = sorted({r["benchmark"] for r in rows})
    runtimes = sorted({r["runtime"] for r in rows})
    datasets = []
    palette = ["#2563eb", "#16a34a", "#dc2626", "#7c3aed", "#0d9488", "#ea580c"]
    for idx, runtime in enumerate(runtimes):
        data = []
        for bench in labels:
            matched = [r for r in rows if r["runtime"] == runtime and r["benchmark"] == bench]
            data.append(matched[0][metric] if matched else 0.0)
        datasets.append(
            {
                "label": runtime,
                "data": data,
                "backgroundColor": palette[idx % len(palette)],
            }
        )
    return {"labels": labels, "datasets": datasets}


def write_html_report(rows: list[dict], out_file: Path, title: str = "JIT Benchmark Report") -> None:
    time_data = json.dumps(build_chart_dataset(rows, "time_ms"), ensure_ascii=False)
    memory_data = json.dumps(build_chart_dataset(rows, "memory_kb"), ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    .chart {{ width: 100%; max-width: 1100px; margin-bottom: 32px; }}
    h1, h2 {{ margin-bottom: 8px; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>Сравнение времени и памяти по бенчмаркам.</p>

  <h2>Время выполнения (ms)</h2>
  <div class="chart"><canvas id="timeChart"></canvas></div>

  <h2>Память (KB)</h2>
  <div class="chart"><canvas id="memoryChart"></canvas></div>

  <script>
    const timeData = {time_data};
    const memoryData = {memory_data};

    new Chart(document.getElementById("timeChart"), {{
      type: "bar",
      data: timeData,
      options: {{
        responsive: true,
        scales: {{
          y: {{ title: {{ display: true, text: "milliseconds" }} }},
          x: {{ title: {{ display: true, text: "benchmark" }} }}
        }}
      }}
    }});

    new Chart(document.getElementById("memoryChart"), {{
      type: "bar",
      data: memoryData,
      options: {{
        responsive: true,
        scales: {{
          y: {{ title: {{ display: true, text: "kilobytes" }} }},
          x: {{ title: {{ display: true, text: "benchmark" }} }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""
    out_file.write_text(html, encoding="utf-8")
