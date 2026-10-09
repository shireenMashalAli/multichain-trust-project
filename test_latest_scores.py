from persistent_trust_manager import get_latest_trust_scores

scores = get_latest_trust_scores()

print("Latest trust scores retrieved from MultiChain:")

for vehicle_id, score in sorted(scores.items()):
    print(f"{vehicle_id}: {score}/100")