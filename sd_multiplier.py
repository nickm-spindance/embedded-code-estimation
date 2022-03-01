import json
import sys

def calc_loc(cloc_report):
    return cloc_report["code"] + cloc_report["comment"]
    # return cloc_report["code"]

if __name__ == "__main__":
    # Parse input arguments
    with open(sys.argv[1]) as f:
        loc_first_json = json.load(f)
    with open(sys.argv[2]) as f:
        loc_last_json = json.load(f)
    openair_hours = int(sys.argv[3])

    # Compute total LOC over first..last commit range
    loc_first = calc_loc(loc_first_json["SUM"])
    loc_last = calc_loc(loc_last_json["SUM"])
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

    print("-------------------------------------------------")
    print("Total OpenAir hours         : {}".format(openair_hours))
    print("Total LOC diff              : {}".format(loc_diff))
    print("SpinDance COCOMO multiplier : {}".format(sd_multiplier))
    print("-------------------------------------------------")
