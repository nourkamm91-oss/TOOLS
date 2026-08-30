import random
import csv
import argparse
import time

# US Area Codes mapping
US_AREA_CODES = {
    "NY": {"state": "New York", "city": "New York City", "codes": [212, 646, 332, 718, 347, 917]},
    "CA": {"state": "California", "city": "Los Angeles", "codes": [310, 424, 213, 323, 818, 626]},
    "FL": {"state": "Florida", "city": "Miami", "codes": [305, 786]},
    "TX": {"state": "Texas", "city": "Houston", "codes": [713, 281, 832]},
    "IL": {"state": "Illinois", "city": "Chicago", "codes": [312, 773]},
    "WA": {"state": "Washington", "city": "Seattle", "codes": [206, 564]},
    "GA": {"state": "Georgia", "city": "Atlanta", "codes": [404, 678, 470]}
}

def generate_number_row(fmt="e164", state_key=None):
    """Generates a single phone number row tuple instantly."""
    all_keys = list(US_AREA_CODES.keys())
    selected_key = state_key if state_key in US_AREA_CODES else random.choice(all_keys)
    loc = US_AREA_CODES[selected_key]
    
    area_code = random.choice(loc["codes"])
    exchange = f"{random.randint(2, 9)}{random.randint(0, 99):02d}"
    subscriber = f"{random.randint(0, 9999):04d}"

    if fmt == "e164":
        phone = f"+1{area_code}{exchange}{subscriber}"
    elif fmt == "dashes":
        phone = f"{area_code}-{exchange}-{subscriber}"
    elif fmt == "plain":
        phone = f"{area_code}{exchange}{subscriber}"
    else:
        phone = f"({area_code}) {exchange}-{subscriber}"

    return (phone, area_code, loc["city"], loc["state"], fmt)

def stream_to_csv(count, filename, fmt, state_key):
    """Streams data directly to disk in chunks to avoid RAM overload."""
    start_time = time.time()
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["phone_number", "area_code", "city", "state", "format"])

        # Write rows directly to disk in batches
        batch_size = 10000
        for i in range(0, count, batch_size):
            current_batch_size = min(batch_size, count - i)
            batch = [generate_number_row(fmt, state_key) for _ in range(current_batch_size)]
            writer.writerows(batch)

    elapsed = round(time.time() - start_time, 2)
    print(f"Successfully generated {count:,} numbers to '{filename}' in {elapsed} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=200000)
    parser.add_argument("-s", "--state", type=str, default=None)
    parser.add_argument("-f", "--format", type=str, default="e164")
    parser.add_argument("-o", "--output", type=str, default="200k_numbers.csv")

    args = parser.parse_args()
    stream_to_csv(count=args.count, filename=args.output, fmt=args.format, state_key=args.state)
