"""Usage: data_migrate.py [-ei] USER_CONFIG SYS_CONFIG DATAFILE
          data_migrate.py -h
Process data migrate.
Arguments:
  USER_CONFIG        user level config
  SYS_CONFIG    system level config
  DATAFILE  user data file to export or import
Options:
  -h --help
  -e       verbose mode
  -i       quiet mode
"""
import io
import json
import subprocess
from docopt import docopt


def get_config(filename):
    """
    get config items in file
    :param file: json config file
    :return: dict contains config item
    """
    # load config items dict
    with io.open(filename, encoding="utf-8-sig") as f:
        return json.loads(f.read())


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments.get("-e") and arguments.get("-i"):
        print("-e and -i should not appear at same time.")
        exit()

    sys_conf = get_config(arguments["SYS_CONFIG"])
    user_conf = get_config(arguments["USER_CONFIG"])

    database_host = sys_conf["database_host"]
    database_port = sys_conf["database_port"]
    database_name = user_conf["database_name"]
    table_name = user_conf["table_name"]
    user_instance_path = user_conf["path"]

    if arguments.get("-e"):
        # export data
        output_file = arguments["DATAFILE"]
        command = "mongoexport" \
                  + " --host " + database_host \
                  + " --port " + str(database_port) \
                  + " -d " + database_name \
                  + " -c " + table_name \
                  + output_file
        status = subprocess.call(command, shell=True)
        print(status)
        if status != 0:
            print("export data form database error. exit, log in stdout.")
            exit()

        zip_command = "zip -r user_instance.zip " \
                      + user_instance_path \
                      + " " + output_file
        status = subprocess.call(zip_command, shell=True)

    if arguments.get("-i"):
        # export data
        zip_command = "unzip -o user_instance.zip"
        status = subprocess.call(zip_command, shell=True)

        output_file = arguments["DATAFILE"]
        command = "mongoimport" \
                  + " --host " + database_host \
                  + " --port " + str(database_port) \
                  + " -d " + database_name \
                  + " -c " + table_name \
                  + " " + output_file
        status = subprocess.call(command, shell=True)
        if status != 0:
            print("export data form database error. exit, log in stdout.")
            exit()

    # TODO MORE CLEAN ACTIONS
