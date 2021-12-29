# Imports
import logging
import os
import toml
import sys
import requests
# Gas Function | Returns gas from an api


def gas():
    # There's no need to have config.toml be in the $HOME dir, though we need to check if config.toml exists
    config_file = "config.toml"

    if os.path.exists(config_file):
        file_name = os.path.join(os.getcwd(), "config.toml")

    else:
        # No need for sys exit, just a return statement will do
        return 'Error: Your config.toml file is missing! Please ensure that the file is in the local directory.'

    f = open(file_name, "r")
    config_data = toml.load(f)
    f.close()

    tags = ["delay", "gas", "key", "log"]

    for tag in tags:
        if tag in tags:
            next
        else:
            sys.stdout.write(
                'Tag {} was not found in the config data.  Check config file to verify all tags are configured.'.format(tag))

    # TBD .. probably need some defaults to get around missing variables in the config file
    # TBD .. figure out how to dynamically create the variable from the tag in the loop above
    gas = config_data["gas"]
    delay = config_data["delay"]
    key = config_data["key"]
    log = config_data["log"]

    # Logging
    log_file = os.path.join(log, "python-gas.log")

    if os.path.isdir(log):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info("Logging directory exists and starting normal operation.")
    else:
        os.mkdir(log)
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info("Log file created and starting normal operation.")

    url = "https://ethgasstation.info/api/ethgasAPI.json?api-key=" + key
    r = requests.get(url)

    # Capture the json from request.
    x = r.json()

    # Print average gas from the json obs.
    query_result = "Current gas average :" + str(x['average'])
    logging.info(query_result)

    # Return whether or not gas is low or high

    avg_gas = x['average']

    if avg_gas <= gas:
        msg = "Current gas is LOW: " + str(x['average'])
        return msg
    else:
        alt_msg = "Current gas is not below threshold, current value = " + \
            str(x['average'])
        return alt_msg
