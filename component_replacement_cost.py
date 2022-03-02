import json
import sys
import math

SW_ENG_HOURLY_RATE = 185
INCLUDE_COMMENTS = True

# Buckets for components, broad categories. If there's no mapping,
# It will show up as "Unknown" category
buckets = {
    'core': [
        'common_macros',
        'common_topics',
        'containers',
        'json_utils',
        'nvs_driver',
        'pool_allocator',
        'status_code',
        'string_utils',
        'fault_monitor',
        'crc',
    ],
    'ble': [
        'ble_endpoint',
        'provision_endpoint_config',
        'jwt',
    ],
    'wifi': [
        'wifi',
    ],
    'cloud_data_model': [
        'metrics',
        'cloud_aws',
    ],
    'hardware_and_os': [
        'hardware_abstraction_layer',
        'platform_abstraction_layer',
        'task_manager',
        'watchdog',
    ],
    'event_loop_messaging': [
        'event_loop',
        'pubsub',
        'work_queue',
    ],
    'ota': [
        'ota_firmware_update',
    ],
    'web_assembly': [
        'wasm_runner',
    ],
    'peripheral_drivers': [
        'rgb_status_led',
        'SPS30',
        'adc_average',
        'io_debounce',
        'MCP47CMB02',
        'nfc',
    ],
    'secure_boot_mfg_tools': [
        'test',
        'test_mode',
    ],
    'starter_application_projects': [
        'console_app',
        'test_on_device',
        'devkit',
    ],
    'documentation': [
        'README.md',
    ],
}

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

def init_buckets_data():
    d = {}
    for bucket in buckets.keys():
        d[bucket] = [[], 0]
    return d

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

    # key = bucket name, val [[components], hours]
    buckets_data = init_buckets_data()

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

            found_bucket = False
            for bucket, bcomponents in buckets.items():
                if component_name in bcomponents:
                    if component_name not in buckets_data[bucket][0]:
                        buckets_data[bucket][0].append(component_name)
                    buckets_data[bucket][1] += hours
                    found_bucket = True
                    break
            if not found_bucket:
                raise ValueError("component {} does not map to a bucket".format(component_name))
        elif key.startswith("code/projects"):
            project_name = key.split('/')[2]
            loc = calc_loc(val)
            hours = cocomo_estimate(loc, COCOMO_SD_MULTIPLIER)
            if project_name in projects:
                projects[project_name] += hours
            else:
                projects[project_name] = hours

            found_bucket = False
            for bucket, bcomponents in buckets.items():
                if project_name in bcomponents:
                    if project_name not in buckets_data[bucket][0]:
                        buckets_data[bucket][0].append(project_name)
                    buckets_data[bucket][1] += hours
                    found_bucket = True
                    break
            if not found_bucket:
                raise ValueError("project {} does not map to a bucket".format(project_name))
        elif key.startswith("tools"):
            loc = calc_loc(val)
            hours = cocomo_estimate(loc, COCOMO_SD_MULTIPLIER)
            tools_hours += hours

            # Place all tools into a single bucket.
            # Too complicated to break it down into categories.
            bucket_name = 'secure_boot_mfg_tools'
            if 'tools' not in buckets_data[bucket_name][0]:
                buckets_data[bucket_name][0].append('tools')
            buckets_data[bucket_name][1] += hours

    # print(components)
    # print(projects)
    # print(tools_hours)

    print("-------------------------------------------------")
    print(" Per-Component Cost")
    print("-------------------------------------------------\n\n")

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

    print("\n\n-------------------------------------------------")
    print(" Per-Category Cost")
    print("-------------------------------------------------\n\n")

    print("{:<30s} {:5s}   {}".format("Name", "Hours", "Est Cost"))
    print("-------------------------------------------------")
    bucket_total_hours = 0
    for bucket, data in buckets_data.items():
        bucket_total_hours += data[1]
        print("{:<30s} {:5d}   ${:>,.2f}".format(
            bucket, data[1], data[1] * SW_ENG_HOURLY_RATE))
    print("-------------------------------------------------")
    print("{:<30s} {:5d}   ${:,.2f}".format("Total", bucket_total_hours, bucket_total_hours * SW_ENG_HOURLY_RATE))

    if total_hours != bucket_total_hours:
        raise ValueError("Per-Category hours does not match per-component hours")
