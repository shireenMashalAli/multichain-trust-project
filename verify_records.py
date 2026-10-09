import subprocess
import json

MULTICHAIN_FOLDER = r"C:\Users\user\Downloads\multichain-windows-2.3.3"
CLI_PATH = MULTICHAIN_FOLDER + r"\multichain-cli.exe"

result = subprocess.run(
    [
        CLI_PATH,
        "trustchain",
        "liststreamitems",
        "vehicle_reports"
    ],
    cwd=MULTICHAIN_FOLDER,
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("Failed to retrieve MultiChain records.")
    print(result.stderr)
    raise SystemExit(1)

# The CLI prints a metadata line before its JSON response.
output = result.stdout
json_start = output.find("[")
if json_start == -1:
    print("Could not find the records in the CLI output.")
    raise SystemExit(1)

records = json.loads(output[json_start:])

print("Total records:", len(records))
print("\nDecoded MultiChain records:")

for record in records:
    decoded_data = bytes.fromhex(record["data"]).decode("utf-8")
    report = json.loads(decoded_data)

    print("\nVehicle:", record["keys"][0])
    print("Record:", json.dumps(report, indent=2))
    print("Transaction ID:", record["txid"])
    print("Confirmations:", record["confirmations"])