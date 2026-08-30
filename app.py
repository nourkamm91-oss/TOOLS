import random
import csv
import json
import argparse
from typing import List, Dict, Optional

US_AREA_CODES = {
    "NY": {"state": "New York", "city": "New York City", "codes": [212, 646, 332, 718, 347, 917]},
    "CA": {"state": "California", "city": "Los Angeles", "codes": [310, 424, 213, 323, 818, 626]},
    "FL": {"state": "Florida", "city": "Miami", "codes": [305, 786]},
    "TX": {"state": "Texas", "city": "Houston", "codes": [713, 281, 832]},
    "IL": {"state": "Illinois", "city": "Chicago", "codes": [312, 773]}
}

class USPhoneGenerator:
    @staticmethod
    def _generate_exchange_code() -> str:
        return f"{random.randint(2, 9)}{random.randint(0, 99):02d}"

    @staticmethod
    def _generate_subscriber_number() -> str:
        return f"{random.randint(0, 9999):04d}"

    @classmethod
    def generate(cls, count: int = 1, state_key: Optional[str] = None, fmt: str = "standard") -> List[Dict[str, str]]:
        results = []
        all_keys = list(US_AREA_CODES.keys())

        for _ in range(count):
            selected_key = state_key if state_key in US_AREA_CODES else random.choice(all_keys)
            location_data = US_AREA_CODES[selected_key]
            
            area_code = random.choice(location_data["codes"])
            exchange = cls._generate_exchange_code()
            subscriber = cls._generate_subscriber_number()
            
            if fmt == "e164":
                formatted_num = f"+1{area_code}{exchange}{subscriber}"
            elif fmt == "dashes":
                formatted_num = f"{area_code}-{exchange}-{subscriber}"
            elif fmt == "plain":
                formatted_num = f"{area_code}{exchange}{subscriber}"
            else:
                formatted_num = f"({area_code}) {exchange}-{subscriber}"

            results.append({
                "phone_number": formatted_num,
                "area_code": str(area_code),
                "city": location_data["city"],
                "state": location_data["state"],
                "format": fmt
            })

        return results

    @staticmethod
    def export_to_file(data: List[Dict[str, str]], filename: str, file_format: str = "csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["phone_number", "area_code", "city", "state", "format"])
            writer.writeheader()
            writer.writerows(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=50)
    parser.add_argument("-s", "--state", type=str)
    parser.add_argument("-f", "--format", type=str, default="e164")
    parser.add_argument("-o", "--output", type=str, default="generated_numbers.csv")

    args = parser.parse_args()
    data = USPhoneGenerator.generate(count=args.count, state_key=args.state, fmt=args.format)
    USPhoneGenerator.export_to_file(data, args.output, file_format="csv")
