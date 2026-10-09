def update_trust_score(current_score, report_is_reliable):
    if report_is_reliable:
        current_score += 5
    else:
        current_score -= 10

    return max(0, min(100, current_score))