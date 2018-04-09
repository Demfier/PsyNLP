import argparse
from os import listdir
import psynlp.helpers.builtins as builtins

parser = argparse.ArgumentParser(
    description='Runs one of the pipeline scripts, for a given language and quality.')
parser.add_argument('-p', '--pipeline', default='deterministic',
                    help='Name of the pipeline file (Default: deterministic)')
parser.add_argument('-l', '--language', default='english',
                    help='Name of the language (Default: english)')
parser.add_argument('-q', '--quality', default='low',
                    help='Size of the training data (Default: low)')
parser.add_argument('-v', '--verbose', action="count", default=False, help='Prints verbose output if specified')
args = parser.parse_args()
builtins.init_verbose(args.verbose)

PIPELINES = [f.rstrip('.py') for f in listdir(
    'psynlp/pipelines') if f.endswith('.py')]
LANGUAGES = [f.split('-train-high')[0]
             for f in listdir('psynlp/data') if f.endswith('high')]
QUALITIES = ['low', 'medium', 'high']

if args.pipeline not in PIPELINES:
    print("Chosen pipeline ({}) is invalid. \n\nChoose one from {}.".format(
        args.pipeline, PIPELINES))
    exit()

if args.language not in LANGUAGES:
    print("Chosen language ({}) is invalid. \n\nChoose one from {}.".format(
        args.language, LANGUAGES))
    exit()

if args.quality not in QUALITIES:
    print("Chosen quality ({}) is invalid. \n\nChoose one from {}.".format(
        args.quality, QUALITIES))
    exit()

import importlib
pipeline = importlib.import_module("psynlp.pipelines.{}".format(args.pipeline))
pipeline.fetch_accuracy(language=args.language, quality=args.quality)
