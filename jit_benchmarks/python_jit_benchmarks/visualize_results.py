#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
RESULTS_FILE = ROOT / "results" / "results.json"
HTML_FILE = ROOT / "results" / "comparison_report.html"


def load_results():
    if not RESULTS_FILE.exists():
        print(f"ERROR: {RESULTS_FILE} not found. Run benchmarks first.")
        return None
    
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)


def calculate_speedups(results):
    by_key = defaultdict(dict)
    
    for r in results:
        key = (r["task"], r["function"])
        by_key[key][r["jit"]] = r["time_ms"]
    
    speedups = {}
    for (task, func), jits in by_key.items():
        if "cpython" not in jits:
            continue
        
        baseline = jits["cpython"]
        if task not in speedups:
            speedups[task] = {}
        
        speedups[task][func] = {}
        for jit, time_ms in jits.items():
            speedups[task][func][jit] = baseline / time_ms if time_ms > 0 else 0.0
    
    return speedups


def prepare_chart_data(results):
    tasks = sorted(set(r["task"] for r in results))
    jits = sorted(set(r["jit"] for r in results))
    
    colors = {
        "cpython": "#2563eb",
        "cpython_jit": "#16a34a",
        "pypy": "#dc2626",
        "jax": "#7c3aed",
        "numba": "#ea580c"
    }
    
    time_data = {}
    memory_data = {}
    
    for task in tasks:
        functions = sorted(set(r["function"] for r in results if r["task"] == task))
        
        time_data[task] = {"labels": functions, "datasets": []}
        memory_data[task] = {"labels": functions, "datasets": []}
        
        for jit in jits:
            time_vals = []
            memory_vals = []
            
            for func in functions:
                matching = [r for r in results if r["task"] == task and r["function"] == func and r["jit"] == jit]
                if matching:
                    time_vals.append(matching[0]["time_ms"])
                    memory_vals.append(matching[0]["memory_kb"])
                else:
                    time_vals.append(None)
                    memory_vals.append(None)
            
            time_data[task]["datasets"].append({
                "label": jit,
                "data": time_vals,
                "backgroundColor": colors.get(jit, "#999999")
            })
            
            memory_data[task]["datasets"].append({
                "label": jit,
                "data": memory_vals,
                "backgroundColor": colors.get(jit, "#999999")
            })
    
    speedups = calculate_speedups(results)
    speedup_data = {}
    
    for task_name, functions in speedups.items():
        speedup_data[task_name] = {"labels": sorted(functions.keys()), "datasets": []}
        
        for jit in jits:
            if jit == "cpython":
                continue
            
            data = []
            for func_name in speedup_data[task_name]["labels"]:
                data.append(functions[func_name].get(jit))
            
            speedup_data[task_name]["datasets"].append({
                "label": jit,
                "data": data,
                "backgroundColor": colors.get(jit, "#999999")
            })
    
    return time_data, memory_data, speedup_data


def generate_html_report(results, output_file):
    tasks = sorted(set(r["task"] for r in results))
    jits = sorted(set(r["jit"] for r in results))
    
    time_data, memory_data, speedup_data = prepare_chart_data(results)
    
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Python JIT Comparison</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
    .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
    h1 {{ color: #333; border-bottom: 3px solid #2563eb; padding-bottom: 10px; }}
    .chart-container {{ margin: 30px 0; }}
    canvas {{ max-height: 400px; }}
    .stats {{ background: #f9fafb; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    details {{ margin: 20px 0; border: 1px solid #e5e7eb; border-radius: 8px; background: #fafafa; }}
    details[open] {{ background: white; }}
    summary {{ 
      padding: 15px 20px; 
      cursor: pointer; 
      font-size: 1.2em; 
      font-weight: bold; 
      color: #2563eb;
      user-select: none;
      transition: background 0.2s;
    }}
    summary:hover {{ background: #f0f0f0; border-radius: 8px; }}
    .task-content {{ padding: 20px; }}
    .hint {{ 
      background: #e0f2fe; 
      padding: 10px 15px; 
      border-left: 4px solid #0284c7; 
      margin: 15px 0; 
      border-radius: 4px;
      font-size: 0.9em;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Python JIT Benchmarks</h1>
    <div class="stats">
      <strong>Total:</strong> {len(results)} measurements<br>
      <strong>JITs:</strong> {', '.join(jits)}<br>
      <strong>Tasks:</strong> {', '.join(tasks)}
    </div>
    <div class="hint">
      Чтобы скрыть JIT, нажмите на его название в легенде.<br>
      Время отображается на логарифмической шкале, чтобы лучше видеть быстрые и медленные функции.
    </div>
"""
    
    for task in tasks:
        html += f"""
    <details open>
      <summary>{task}</summary>
      <div class="task-content">
        <div class="chart-container">
          <h3>Time (ms)</h3>
          <canvas id="time_{task}"></canvas>
        </div>
        <div class="chart-container">
          <h3>Memory (KB)</h3>
          <canvas id="memory_{task}"></canvas>
        </div>
"""
        if task in speedup_data:
            html += f"""
        <div class="chart-container">
          <h3>Speedup</h3>
          <canvas id="speedup_{task}"></canvas>
        </div>
"""
        html += """
      </div>
    </details>
"""
    
    html += """
  </div>
  <script>
"""
    
    for task in tasks:
        time_json = json.dumps(time_data[task])
        memory_json = json.dumps(memory_data[task])
        
        html += f"""
    new Chart(document.getElementById("time_{task}"), {{
      type: "bar",
      data: {time_json},
      options: {{
        responsive: true,
        interaction: {{
          mode: 'index',
          intersect: false,
        }},
        plugins: {{
          legend: {{
            display: true,
            position: 'top',
            onClick: function(e, legendItem, legend) {{
              const index = legendItem.datasetIndex;
              const ci = legend.chart;
              const meta = ci.getDatasetMeta(index);
              meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;
              ci.update();
            }},
            labels: {{
              padding: 15,
              usePointStyle: true,
              font: {{ size: 12 }}
            }}
          }},
          tooltip: {{
            callbacks: {{
              label: function(context) {{
                let label = context.dataset.label || '';
                if (label) {{ label += ': '; }}
                if (context.parsed.y === null || context.parsed.y === undefined) {{
                  label += 'N/A (skipped)';
                }} else {{
                  label += context.parsed.y.toFixed(2) + ' ms';
                }}
                return label;
              }}
            }}
          }}
        }},
        scales: {{
          y: {{
            type: 'logarithmic',
            title: {{ display: true, text: "Time (ms) - log scale" }},
            ticks: {{
              callback: function(value) {{
                if (value === 0.01 || value === 0.1 || value === 1 || value === 10 || 
                    value === 100 || value === 1000 || value === 10000) {{
                  return value;
                }}
                return null;
              }}
            }}
          }}
        }}
      }}
    }});
    
    new Chart(document.getElementById("memory_{task}"), {{
      type: "bar",
      data: {memory_json},
      options: {{
        responsive: true,
        interaction: {{
          mode: 'index',
          intersect: false,
        }},
        plugins: {{
          legend: {{
            display: true,
            position: 'top',
            onClick: function(e, legendItem, legend) {{
              const index = legendItem.datasetIndex;
              const ci = legend.chart;
              const meta = ci.getDatasetMeta(index);
              meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;
              ci.update();
            }},
            labels: {{
              padding: 15,
              usePointStyle: true,
              font: {{ size: 12 }}
            }}
          }},
          tooltip: {{
            callbacks: {{
              label: function(context) {{
                let label = context.dataset.label || '';
                if (label) {{ label += ': '; }}
                if (context.parsed.y === null || context.parsed.y === undefined) {{
                  label += 'N/A (skipped)';
                }} else {{
                  label += context.parsed.y.toFixed(2) + ' KB';
                }}
                return label;
              }}
            }}
          }}
        }},
        scales: {{
          y: {{
            title: {{ display: true, text: "Memory (KB)" }}
          }}
        }}
      }}
    }});
"""
        
        if task in speedup_data:
            speedup_json = json.dumps(speedup_data[task])
            html += f"""
    new Chart(document.getElementById("speedup_{task}"), {{
      type: "bar",
      data: {speedup_json},
      options: {{
        responsive: true,
        interaction: {{
          mode: 'index',
          intersect: false,
        }},
        plugins: {{
          legend: {{
            display: true,
            position: 'top',
            onClick: function(e, legendItem, legend) {{
              const index = legendItem.datasetIndex;
              const ci = legend.chart;
              const meta = ci.getDatasetMeta(index);
              meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;
              ci.update();
            }},
            labels: {{
              padding: 15,
              usePointStyle: true,
              font: {{ size: 12 }}
            }}
          }},
          tooltip: {{
            callbacks: {{
              label: function(context) {{
                let label = context.dataset.label || '';
                if (label) {{ label += ': '; }}
                if (context.parsed.y === null || context.parsed.y === undefined) {{
                  label += 'N/A (skipped)';
                }} else {{
                  label += context.parsed.y.toFixed(1) + 'x speedup';
                }}
                return label;
              }}
            }}
          }}
        }},
        scales: {{
          y: {{
            title: {{ display: true, text: "Speedup (x)" }},
            beginAtZero: true
          }}
        }}
      }}
    }});
"""
    
    html += """
  </script>
</body>
</html>
"""
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HTML_FILE)
    parser.add_argument("--no-console", action="store_true")
    args = parser.parse_args()
    
    results = load_results()
    if not results:
        return
    
    generate_html_report(results, args.output)
    print(f"\nHTML report: {args.output}")


if __name__ == "__main__":
    main()
