import names
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-g", "--gender", help="set gender")
args = parser.parse_args()
if args.gender not in ['male', 'female']:
    print('wrong gender')
else:
    name = names.get_full_name(gender=args.gender)
    print(args.gender, name, len(name))