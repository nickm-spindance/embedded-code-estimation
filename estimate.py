import json
import sys

SW_ENG_HOURLY_RATE=185

if __name__ == "__main__":
    # Parse input arguments
    with open(sys.argv[1]) as f:
        loc_first_json = json.load(f)
    with open(sys.argv[2]) as f:
        loc_last_json = json.load(f)
    total_lines_added = int(sys.argv[3])
    total_lines_deleted = int(sys.argv[4])
    openair_hours = int(sys.argv[5])

    # Compute total LOC over first..last commit range
    loc_first = loc_first_json["SUM"]["code"]
    loc_last = loc_last_json["SUM"]["code"]
    loc_diff = loc_last - loc_first

    # Compute SD COCOMO multiplier from total hours and LOC
    # COCOMO: PersonHours = a * KLOC ^ b * HoursPerMonth * SDMultiplier
    #
    # We are solving for SDMultiplier (SpinDance Multiplier)
    a = 3.6
    b = 1.2
    hours_per_month = 140
    kloc = loc_diff / 1000.
    sd_multiplier = openair_hours / (a * kloc ** b * hours_per_month)

    # Compute total commit changes over first..last commit range
    commit_diff = total_lines_added + total_lines_deleted

    for key in loc_first_json:
        if key == "header" or key == "SUM":
            continue
        print(key)

    # For each component:
    #   Compute replacement cost using Tol model

    # COCOMO: Compute SpinDance multiplier from total LOC and hours
    # For each component:
    #   Compute replacement cost using COCOMO model with SD multiplier

    print("Total LOC diff              : {}".format(loc_diff))
    print("Total commit diff           : {}".format(commit_diff))
    print("SpinDance COCOMO multiplier : {}".format(sd_multiplier))
