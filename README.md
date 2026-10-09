# MultiChain-Based Adaptive Trust Management

## Project Overview

This project implements a basic trust-management prototype using Python and MultiChain. It updates trust scores based on reliable and unreliable observations and stores the resulting records in a MultiChain stream.

## Technologies Used

- Python
- MultiChain 2.3.3
- JSON
- MultiChain command-line interface

## Features

- Trust-score calculation with a range of 0–100
- Trust updates based on reliable and unreliable observations
- Persistent storage of trust records in a MultiChain stream
- Sequence numbers for newer trust-update records
- Retrieval and verification of stored trust scores
- Unit tests for trust-score calculations

## Project Files

- `persistent_trust_manager.py` — Main application for retrieving scores and publishing updates
- `trust_utils.py` — Trust-score calculation function
- `test_trust_score.py` — Unit tests for trust-score calculation
- `test_latest_scores.py` — Read-only test for retrieving the latest scores
- `verify_records.py` — Displays and verifies stored stream records
- `multichain_test.py` — Tests the MultiChain connection
- `trust_manager.py` — Initial trust-management implementation

## Configuration

Update `MULTICHAIN_FOLDER` in the Python scripts if MultiChain is installed in a different directory.

The current configuration uses:

- Blockchain: `trustchain`
- Stream: `vehicle_reports`

Ensure the MultiChain node is running and the stream exists and is subscribed to before running the application.

## Running the Project

Run these commands from the project directory.

Test trust-score calculations:

```powershell
py test_trust_score.py
```

Retrieve the latest trust scores without publishing new transactions:

```powershell
py test_latest_scores.py
```

Verify stored stream records:

```powershell
py verify_records.py
```

Publish new trust updates:

```powershell
py persistent_trust_manager.py
```

**Warning:** Running the main application publishes new transactions to the MultiChain stream.

## Test Results

The trust-score unit tests passed all six test cases.

The latest verified trust scores in the recorded test run were:

- VEHICLE001: 90/100
- VEHICLE002: 0/100

## Limitations

Reliable and unreliable observations are simulated inputs. The prototype does not automatically detect malicious vehicles or implement the complete adaptive trust-management framework from the referenced research paper.

## Future Work

- Integrate actual vehicle or network observations
- Evaluate additional trust-update strategies
- Add stronger validation of incoming reports
- Evaluate the system with larger datasets and more participants

## Research Context

This project is an adaptation of blockchain-based adaptive trust-management concepts. It uses Python for trust calculations and MultiChain streams for recording trust updates.
