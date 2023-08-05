import names
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--gender", help="set mail or female")
args = parser.parse_args()

name = names.get_full_name(gender='mail')

print(name, len(name)-1)
