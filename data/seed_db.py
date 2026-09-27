import json
import os
from data.generator import generate_synthetic_dataset

def seed_database():
    dataset = generate_synthetic_dataset()
    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "synthetic_database.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"[Seed DB] Generated synthetic dataset with {len(dataset['locations'])} locations, "
          f"{len(dataset['stations'])} stations, {len(dataset['pollution_observations'])} pollution records, "
          f"{len(dataset['weather_observations'])} weather records, {len(dataset['user_alert_configs'])} user alert configs, "
          f"and {len(dataset['alert_events'])} alert events at {out_path}.")

if __name__ == "__main__":
    seed_database()
