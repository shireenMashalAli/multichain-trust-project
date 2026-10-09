import subprocess
import json

MULTICHAIN_FOLDER = r"C:\Users\user\Downloads\multichain-windows-2.3.3"
CLI_PATH = MULTICHAIN_FOLDER + r"\multichain-cli.exe"


# Function to calculate the trust score
def update_trust_score(current_score, report_is_reliable):
    if report_is_reliable:
        current_score += 5
    else:
        current_score -= 10

    return max(0, min(100, current_score))


# Initial trust scores of simulated vehicles
vehicles = {
    "VEHICLE001": 50,
    "VEHICLE002": 50,
}


# Simulated observations
# True = reliable report; False = unreliable report
observations = [
    ("VEHICLE001", True),
    ("VEHICLE001", True),
    ("VEHICLE002", False),
    ("VEHICLE002", False),
]


# Calculate trust and publish each update to MultiChain
for vehicle_id, reliable in observations:

    old_score = vehicles[vehicle_id]

    new_score = update_trust_score(old_score, reliable)

    vehicles[vehicle_id] = new_score

    status = "Reliable" if reliable else "Unreliable"

    print(
        f"\n{vehicle_id}: {status} report | "
        f"Trust: {old_score} -> {new_score}"
    )

    # Create a record for the blockchain
    vehicle_report = {
        "vehicle_id": vehicle_id,
        "report": status,
        "previous_trust": old_score,
        "trust": new_score
    }

    # Convert the record to JSON and hexadecimal
    report_json = json.dumps(vehicle_report)
    report_hex = report_json.encode("utf-8").hex()

    # Publish the record to the MultiChain stream
    result = subprocess.run(
        [
            CLI_PATH,
            "trustchain",
            "publish",
            "vehicle_reports",
            vehicle_id,
            report_hex
        ],
        cwd=MULTICHAIN_FOLDER,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Blockchain publication successful!")
        print("Transaction ID:", result.stdout.strip())
    else:
        print("Blockchain publication failed.")
        print("Output:", result.stdout)
        print("Details:", result.stderr)


# Display final trust scores
print("\nFinal trust scores:")

for vehicle_id, score in vehicles.items():
    print(f"{vehicle_id}: {score}/100")
