import json
import sys
import math

SW_ENG_HOURLY_RATE = 185
INCLUDE_COMMENTS = True

# Average multiplier for COCOMO model, computed from prior customer projects
# (see, for example, ego_sd_multiplier.sh, grilla_sd_multiplier.sh)
if INCLUDE_COMMENTS:
    COCOMO_SD_MULTIPLIER = (.244 + .124) / 2 # code + comments
else:
    COCOMO_SD_MULTIPLIER = (.306 + .145) / 2 # code only, no comments

def calc_loc(cloc_report):
    if INCLUDE_COMMENTS:
        return cloc_report["code"] + cloc_report["comment"]
    else:
        return cloc_report["code"]

# COCOMO: PersonHours = a * KLOC ^ b * HoursPerMonth * SDMultiplier
def cocomo_estimate(loc, sd_mult):
    a = 3.6
    b = 1.2
    hours_per_month = 140
    kloc = loc / 1000.
    model_output = a * kloc ** b * hours_per_month * sd_mult
    # round up to nearest hour
    return int(math.ceil(model_output))

if __name__ == "__main__":
    # Parse input arguments
    with open(sys.argv[1]) as f:
        loc_json = json.load(f)

    # key = component name, val = COCOMO estimate of hours
    components = {}

    # key = project name, val = COCOMO estimate of hours
    projects = {}

    # val = COCOMO estimate of hours
    tools_hours = 0

    for key, val in loc_json.items():
        if key == "header" or key == "SUM":
            continue

        if key.startswith("code/components"):
            component_name = key.split('/')[2]
            loc = calc_loc(val)
            hours = cocomo_estimate(loc, COCOMO_SD_MULTIPLIER)
            if component_name in components:
                components[component_name] += hours
            else:
                components[component_name] = hours
        elif key.startswith("code/projects"):
            project_name = key.split('/')[2]
            loc = calc_loc(val)
            hours = cocomo_estimate(loc, COCOMO_SD_MULTIPLIER)
            if project_name in projects:
                projects[project_name] += hours
            else:
                projects[project_name] = hours
        elif key.startswith("tools"):
            loc = calc_loc(val)
            hours = cocomo_estimate(loc, COCOMO_SD_MULTIPLIER)
            tools_hours += hours

    # print(components)
    # print(projects)
    # print(tools_hours)

    print("{:<30s} {:5s}   {}".format("Name", "Hours", "Est Cost"))
    print("--COMPONENTS-------------------------------------")
    for name, hours in components.items():
        print("{:<30s} {:5d}   ${:,.2f}".format(name, hours, hours * SW_ENG_HOURLY_RATE))
    print("--PROJECTS---------------------------------------")
    for name, hours in projects.items():
        print("{:<30s} {:5d}   ${:,.2f}".format(name, hours, hours * SW_ENG_HOURLY_RATE))
    print("--TOOLS------------------------------------------")
    print("{:<30s} {:5d}   ${:,.2f}".format("Tools", tools_hours, tools_hours * SW_ENG_HOURLY_RATE))
    print("-------------------------------------------------")

    total_hours = sum([hours for hours in components.values()])
    total_hours += sum([hours for hours in projects.values()])
    total_hours += tools_hours
    print("{:<30s} {:5d}   ${:,.2f}".format("Total", total_hours, total_hours * SW_ENG_HOURLY_RATE))
