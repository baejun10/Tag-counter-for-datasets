import os
import argparse
import csv
import time
from collections import Counter
import multiprocessing as mp

def process_file(file_path):
    with open(file_path, "rt", encoding='utf-8') as f:
        lines = f.readlines()
        tags = [tag.strip() for line in lines for tag in line.split(',')]
        return Counter(tags)

def process_files(file_paths):
    tags = Counter()
    with mp.Pool(args.processes) as pool:
        for result in pool.imap_unordered(process_file, file_paths):
            tags += result
    return tags

def save(tags):
    filename = "tag_count.csv"
    path = args.dir
    if args.output is not None:
        path = args.output
    save_path = os.path.join(path, filename)
    with open(save_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['tag', 'count'])
        for tag, count in tags.items():
            writer.writerow([tag, count])
    print(f'{filename} is saved at "{path}"')

def main():
    print('Start Process')
    start = time.time()
    if args.recursive:
        file_paths = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk(args.dir) 
                      for filename in filenames if filename.endswith('.' + args.extension)]
    else:
        file_paths = [os.path.join(args.dir, filename) for filename in os.listdir(args.dir) 
                      if filename.endswith('.' + args.extension)]
    assert len(file_paths) > 0, 'file does not exist'
    tags = process_files(file_paths)
    end = time.time()
    print(f'complete in {end - start:.3f} sec')
    print(f'Used {len(file_paths)} caption files')
    print(tags)
    save(tags)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Option Argparser')
    parser.add_argument('--dir', type=str,
                        help='input and output directory')
    parser.add_argument('--output', type=str,
                        help='set other tag_count file output directory(optional)')
    parser.add_argument('--recursive', action='store_true',
                        help='enable recursive directory')
    parser.add_argument('--extension', type=str, default="txt",
                        help='set file extension (default=txt)')
    parser.add_argument('--processes',  type=int, default=1,
                        help='process amount to multiprocess for faster computing')
    args = parser.parse_args()
    main()
