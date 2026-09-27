from collections import Counter
from datetime import datetime
from pathlib import Path
import sys


VALID_LEVELS = {"DEBUG", "INFO", "WARN", "ERROR", "FATAL"}


def _parse_line(raw_line, seen):
    line = raw_line.rstrip("\r\n")
    if not line:
        return "ligne_vide", None
    if line[0].isspace():
        return "continuation_indentee", None
    if "\t" in line:
        return "separateurs_tabulation", None
    if line in seen:
        return "doublon", None
    seen.add(line)

    fields = line.split("|", 4)
    if len(fields) != 5:
        return "champs_insuffisants", None

    try:
        timestamp = datetime.fromisoformat(fields[0].strip())
    except ValueError:
        return "horodatage_invalide", None

    level = fields[1].strip().upper()
    if level not in VALID_LEVELS:
        return "niveau_inconnu", None
    if not fields[4].strip():
        return "message_vide", None
    return None, (timestamp, level)


def parse_log(lines):
    """Retourne les erreurs par heure et les decisions prises pour chaque ligne."""
    hourly_errors = Counter()
    decisions = Counter()
    candidates = []
    seen = set()

    for raw_line in lines:
        decisions["lues"] += 1
        reason, candidate = _parse_line(raw_line, seen)
        if reason:
            decisions[reason] += 1
            continue
        candidates.append(candidate)

    dates = Counter(timestamp.date() for timestamp, _ in candidates)
    reference_date = dates.most_common(1)[0][0] if dates else None

    for timestamp, level in candidates:
        if timestamp.date() != reference_date:
            decisions["jour_hors_periode"] += 1
            continue
        decisions["lignes_valides"] += 1
        if level in {"ERROR", "FATAL"}:
            hourly_errors[timestamp.hour] += 1

    return hourly_errors, decisions


def main():
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("app.log")
    with log_path.open(encoding="utf-8") as log_file:
        hourly_errors, decisions = parse_log(log_file)

    print("Erreurs par heure")
    for hour in sorted(hourly_errors):
        print(f"{hour:02d}h : {hourly_errors[hour]}")

    rejected = sum(value for key, value in decisions.items() if key not in {"lues", "lignes_valides"})
    print("\nBilan")
    print(f"Lignes lues : {decisions['lues']}")
    print(f"Lignes valides : {decisions['lignes_valides']}")
    print(f"Lignes écartées : {rejected}")
    for reason, count in sorted(decisions.items()):
        if reason not in {"lues", "lignes_valides"}:
            print(f"- {reason} : {count}")


if __name__ == "__main__":
    main()