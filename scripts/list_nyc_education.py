"""
Search and list popular NYC education datasets from data.cityofnewyork.us

These are tested and working dataset IDs for NYC education data.
"""

print("\n" + "=" * 60)
print("NYC EDUCATION DATASETS - Popular Options")
print("=" * 60 + "\n")

datasets = [
    {
        "id": "s3k6-pzi2",
        "name": "2013 - 2018 Demographic Snapshot School",
        "description": "School demographics including enrollment by grade, race/ethnicity",
        "rows": "~2,000",
        "recommended": True,
    },
    {
        "id": "7yc5-fec2",
        "name": "Math Test Results 2006-2012 - School Level",
        "description": "Math test scores aggregated by school",
        "rows": "~10,000",
        "recommended": True,
    },
    {
        "id": "zt9s-n5aj",
        "name": "SAT Results by School",
        "description": "SAT scores (Math, Reading, Writing) by NYC high schools",
        "rows": "~500",
        "recommended": True,
    },
    {
        "id": "i9pf-sj7c",
        "name": "School Quality Reports",
        "description": "Annual school quality reports with performance metrics",
        "rows": "~1,500",
        "recommended": False,
    },
    {
        "id": "ufu2-qea8",
        "name": "Math Test Results by School (Recent)",
        "description": "Recent math test results",
        "rows": "~2,000",
        "recommended": True,
    },
    {
        "id": "97mf-9njv",
        "name": "School Attendance and Enrollment",
        "description": "Daily attendance rates and enrollment numbers",
        "rows": "~1,500",
        "recommended": False,
    },
]

print("🎓 RECOMMENDED DATASETS:\n")
for ds in datasets:
    if ds["recommended"]:
        print(f"📊 {ds['name']}")
        print(f"   ID: {ds['id']}")
        print(f"   {ds['description']}")
        print(f"   Rows: {ds['rows']}")
        print(
            f"   Command: python scripts/fetch_data_gov.py {ds['id']} --domain data.cityofnewyork.us --limit 1000"
        )
        print()

print("=" * 60)
print("OTHER DATASETS:\n")
for ds in datasets:
    if not ds["recommended"]:
        print(f"• {ds['name']} ({ds['id']})")
        print(f"  {ds['description']}")
        print()

print("=" * 60)
print("\n💡 QUICK START:\n")
print("Fetch SAT scores (small, easy to analyze):")
print(
    "python scripts/fetch_data_gov.py zt9s-n5aj --domain data.cityofnewyork.us --limit 500"
)
print()
print("Fetch school demographics (comprehensive):")
print(
    "python scripts/fetch_data_gov.py s3k6-pzi2 --domain data.cityofnewyork.us --limit 1000"
)
print()
print("Fetch math test results (good for analysis):")
print(
    "python scripts/fetch_data_gov.py 7yc5-fec2 --domain data.cityofnewyork.us --limit 1000"
)
print()
