import random
import argparse
import time

US_AREA_CODES = {
    "NY": [212, 646, 332, 718, 347, 917],
    "CA": [310, 424, 213, 323, 818, 626],
    "FL": [305, 786],
    "TX": [713, 281, 832],
    "IL": [312, 773],
    "WA": [206, 564],
    "GA": [404, 678, 470]
}

def generate_phone_number(fmt="plain", state_key=None):
    all_keys = list(US_AREA_CODES.keys())
    selected_key = state_key if state_key in US_AREA_CODES else random.choice(all_keys)
    area_codes = US_AREA_CODES[selected_key]
    
    area_code = random.choice(area_codes)
    exchange = f"{random.randint(2, 9)}{random.randint(0, 99):02d}"
    subscriber = f"{random.randint(0, 9999):04d}"

    if fmt == "e164":
        return f"+1{area_code}{exchange}{subscriber}\n"
    elif fmt == "dashes":
        return f"{area_code}-{exchange}-{subscriber}\n"
    elif fmt == "plain":
        return f"{area_code}{exchange}{subscriber}\n"
    else:
        return f"({area_code}) {exchange}-{subscriber}\n"

def stream_to_txt(count, filename, fmt, state_key):
    start_time = time.time()
    
    with open(filename, "w", encoding="utf-8") as f:
        batch_size = 10000
        for i in range(0, count, batch_size):
            current_batch_size = min(batch_size, count - i)
            lines = [generate_phone_number(fmt, state_key) for _ in range(current_batch_size)]
            f.writelines(lines)

    elapsed = round(time.time() - start_time, 2)
    print(f"Successfully generated {count:,} numbers to '{filename}' in {elapsed} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=200000)
    parser.add_argument("-s", "--state", type=str, default=None)
    parser.add_argument("-f", "--format", type=str, default="plain")
    parser.add_argument("-o", "--output", type=str, default="Valid.txt")

    args, unknown = parser.parse_known_args()
    stream_to_txt(count=args.count, filename=args.output, fmt=args.format, state_key=args.state)
