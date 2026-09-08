import csv
import os

def open_csv_file(csv_path: str) -> list[tuple[int, str, float]]:
    results: list[tuple[int, str, float]] = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            house_id = int(row['HouseID'])
            timestamp = row['Timestamp']
            consumption = float(row['TotalConsumption'])
            results.append((house_id, timestamp, consumption))
    return results

def export_to_csv(rows: list[tuple[int, str, float]], file_path: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['HouseID', 'Timestamp', 'TotalConsumption'])
        for house_id, timestamp, value in rows:
            writer.writerow([house_id, timestamp, value])
