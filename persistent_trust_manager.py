from trust_utils import update_trust_score
import subprocess
import json

MULTICHAIN_FOLDER = r"C:\Users\user\Downloads\multichain-windows-2.3.3"
CLI_PATH = MULTICHAIN_FOLDER + r"\multichain-cli.exe"
CHAIN_NAME = "trustchain"
STREAM_NAME = "vehicle_reports"


def run_multichain_command(arguments):
    result = subprocess.run(
        [CLI_PATH, CHAIN_NAME] + arguments,
        cwd=MULTICHAIN_FOLDER,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"MultiChain command failed:\n"
            f"{result.stdout}\n{result.stderr}"
        )

    return result.stdout


def get_stream_records():
    output = run_multichain_command(
        ["liststreamitems", STREAM_NAME]
    )

    json_start = output.find("[")
    if json_start == -1:
        raise ValueError("Could not find stream records.")

    return json.loads(output[json_start:])


def decode_record(record):
    data_hex = record.get("data", "")

    if not data_hex:
        return None

    try:
        return json.loads(
            bytes.fromhex(data_hex).decode("utf-8")
        )
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def get_latest_trust_scores():
    records = get_stream_records()
    latest_records = {}

    for record in records:
        report = decode_record(record)

        if not report:
            continue

        vehicle_id = report.get("vehicle_id")
        trust = report.get("trust")

        if vehicle_id is None or trust is None:
            continue

        sequence = report.get("sequence")
        blocktime = record.get("blocktime", 0)
        txid = record.get("txid", "")

        # Prefer sequence numbers for new records.
        # Use block time for older records without sequence numbers.
        if isinstance(sequence, int):
            ordering = (1, sequence, blocktime, txid)
        else:
            ordering = (0, blocktime, txid)

        previous = latest_records.get(vehicle_id)

        if previous is None or ordering > previous["ordering"]:
            latest_records[vehicle_id] = {
                "trust": trust,
                "ordering": ordering
            }

    return {
        vehicle_id: record["trust"]
        for vehicle_id, record in latest_records.items()
    }


def publish_trust_update(vehicle_id, old_score, new_score, reliable):
    records = get_stream_records()
    latest_sequence = 0

    # Find the highest sequence number already published
    # for this vehicle. Older records without sequence numbers
    # are not counted because sequence numbering was introduced later.
    for record in records:
        item = decode_record(record)

        if not item:
            continue

        if item.get("vehicle_id") != vehicle_id:
            continue

        sequence = item.get("sequence")

        if isinstance(sequence, int) and not isinstance(sequence, bool):
            latest_sequence = max(latest_sequence, sequence)

    report = {
        "vehicle_id": vehicle_id,
        "sequence": latest_sequence + 1,
        "report": "Reliable" if reliable else "Unreliable",
        "previous_trust": old_score,
        "trust": new_score
    }

    report_hex = json.dumps(report).encode("utf-8").hex()

    txid = run_multichain_command([
        "publish",
        STREAM_NAME,
        vehicle_id,
        report_hex
    ])

    print("Sequence:", report["sequence"])
    print("Published transaction:", txid.strip())


def main():
    vehicles = get_latest_trust_scores()

    if not vehicles:
        print("No existing trust scores found. Nothing to update.")
        raise SystemExit(1)

    print("Current scores from MultiChain:")

    for vehicle_id, score in vehicles.items():
        print(f"{vehicle_id}: {score}/100")

    new_observations = [
        ("VEHICLE001", True),
        ("VEHICLE002", False)
    ]

    print("\nApplying new observations:")

    for vehicle_id, reliable in new_observations:
        if vehicle_id not in vehicles:
            print(f"Skipping {vehicle_id}: no previous score found.")
            continue

        old_score = vehicles[vehicle_id]
        new_score = update_trust_score(old_score, reliable)

        print(f"{vehicle_id}: {old_score} -> {new_score}")

        publish_trust_update(
            vehicle_id,
            old_score,
            new_score,
            reliable
        )

        vehicles[vehicle_id] = new_score

    print("\nUpdated scores:")

    for vehicle_id, score in vehicles.items():
        print(f"{vehicle_id}: {score}/100")


if __name__ == "__main__":
    main()