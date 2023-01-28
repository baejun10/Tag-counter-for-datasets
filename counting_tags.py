import pandas as pd
import os
import glob
import argparse
import csv
import time
import multiprocessing as mp


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
        tag = tag.strip()
        ttag = (tags_table['tag'] == tag)
        if ttag.any():
            tt = tags_table.loc[ttag,'count']
            tt = tt + 1
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

def work(cap_paths, tags_table):
    if __name__ == '__main__':
        proc_num = args.processes
        p = mp.Pool(proc_num)
        for i in range (0,len(cap_paths),proc_num) :
            reader = p.map_async(read_caption,cap_paths[i:i+proc_num]) ## 코어개수 만큼 멀티프로세싱으로 파일 열고 태그 추출
            for tags in reader.get():
                process(tags,tags_table) #이부분은 공유 메모리 멀티프로세스 가능?
                if args.verbose:
                    print(tags)
        p.close()
        p.join()
    # for cap_path in cap_paths:
    #     if args.verbose:
    #         print(cap_path)
    #     process(read_caption(cap_paths), tags_table)
        
    

def main():
    if __name__ == '__main__':
        print('Start Process')
        start = time.time()
        if (args.recursive):
            cap_paths = glob.glob(os.path.join(
                args.dir, "**/*." + args.extension), recursive=True)
        else:
            cap_paths = glob.glob(os.path.join(args.dir, "*." + args.extension))
        assert len(cap_paths) > 0, 'file does not exist'

        tags_table = pd.DataFrame({'tag': [], 'count': []})
        tags_table['count'] = tags_table['count'].astype(int)

        work(cap_paths, tags_table)
        end = time.time()
        print(f'complete in {end - start:.3f} sec')
        print(f'Used {len(cap_paths)} caption files')
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
parser.add_argument('--processes',  type=int, default=1,
                    help='process amount to multiprocess for faster computing')
args = parser.parse_args()
main()
