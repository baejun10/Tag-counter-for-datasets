import pandas as pd
import os
import glob
import argparse
import csv


def read_caption(cap_path):
    if os.path.isfile(cap_path):
        with open(cap_path, "rt", encoding='utf-8') as f:
            lines = csv.reader(f)
            for line in lines:
                if args.verbose:
                    print(line)
                return line


def process(tags, tags_table):
    for tag in tags:
        if (tags_table['tag'] == tag).any():
            tags_table.loc[tags_table['tag'] == tag,
                           'count'] = tags_table.loc[tags_table['tag'] == tag, 'count'] + 1
        else:
            tags_table.loc[len(tags_table)] = [tag, 1]
    # print(tags_table)


def save(df):
    filename = "tag_count.csv"
    path = args.dir
    if (args.output is not None):
        path = args.output
    save_path = os.path.join(path, filename)
    df.to_csv(save_path, mode='w')
    print(f'{filename} is saved at "{path}"')


def main():
    print('Start Process')
    if (args.recursive):
        cap_paths = glob.glob(os.path.join(
            args.dir, "**/*." + args.extension), recursive=True)
    else:
        cap_paths = glob.glob(os.path.join(args.dir, "*" + args.extension))

    assert len(cap_paths) > 0, 'file does not exist'

    tags_table = pd.DataFrame({'tag': [], 'count': []})
    tags_table['count'] = tags_table['count'].astype(int)

    for cap_path in cap_paths:
        if args.verbose:
            print(cap_path)
        process(read_caption(cap_path), tags_table)
    print(tags_table)
    save(tags_table)


################ start ###################
parser = argparse.ArgumentParser(description='Option Argparser')
parser.add_argument('--dir', type=str,
                    help='input and output directory')
parser.add_argument('--output', type=str,
                    help='set other tag_count file output directory(optional)')
parser.add_argument('--recursive', action='store_true',
                    help='enable recursive directory')
parser.add_argument('--extension', type=str, default="txt",
                    help='set file extension (default=txt)')
parser.add_argument('--verbose',  action='store_true',
                    help='verbose filename and tags')
args = parser.parse_args()
main()
