
import subprocess
import json

MULTICHAIN_FOLDER = r"C:\Users\user\Downloads\multichain-windows-2.3.3"
CLI_PATH = MULTICHAIN_FOLDER + r"\multichain-cli.exe"

# Example report from a simulated vehicle
vehicle_report = {
    "vehicle_id": "VEHICLE002",
    "report": "Accident reported",
    "trust": 65
}

# Convert the report to JSON, then to hexadecimal for MultiChain
report_json = json.dumps(vehicle_report)
report_hex = report_json.encode("utf-8").hex()

result = subprocess.run(
    [
        CLI_PATH,
        "trustchain",
        "publish",
        "vehicle_reports",
        vehicle_report["vehicle_id"],
        report_hex
    ],
    cwd=MULTICHAIN_FOLDER,
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Vehicle report published successfully!")
    print("Vehicle ID:", vehicle_report["vehicle_id"])
    print("Report:", vehicle_report["report"])
    print("Trust score:", vehicle_report["trust"])
    print("MultiChain response:")
    print(result.stdout)
else:
    print("Publishing failed.")
    print("Output:", result.stdout)
    print("Error:", result.stderr)
