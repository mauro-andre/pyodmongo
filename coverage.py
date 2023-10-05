import json

with open("coverage.json", "r") as file:
    coverage = json.load(file)
    coverage_percentage_string = coverage["totals"]["percent_covered_display"] + "%"
with open("htmlcov/coverage_badge.json", "w") as file:
    json.dump(
        {
            "schemaVersion": 1,
            "label": "Coverage",
            "message": coverage_percentage_string,
            "color": "green",
        },
        file,
        indent=4,
    )
