import os
import time
import json
import pandas as pd
import argparse
from glob import glob
import natsort

'''
## extract top rank of json_data(from arvix) (for test from .pickle file)
def extract_top(head=15):        
    import pickle

    json_path = os.path.join('/Users/hyeongyu/python_code/arxiv/arxiv_parser', 'parsing_sample_data.pickle')

    with open(json_path, 'rb') as f:
        json_data = pickle.load(f) # 단 한줄씩 읽어옴

    json_data = json.loads(json_data)

    no = []
    titles= []
    links= []
    authors= []

    for i, data in enumerate(json_data[:head]):
        # print(len(data)) # 14 | keys = {'abstract', 'authors', 'category', 'comment', 'img', 'in_library', 'link', 'num_discussion', 'originally_published_time', 'pid', 'published_time', 'rawpid', 'tags', 'title'}
        no.append(i+1)
        titles.append(data['title'].replace('\n ', ''))
        links.append(data['link'])
        authors.append(data['authors'][0])
    
    # list => df
    top_dict = {'no': no,
                'date': get_current_time()[0],
                'first_authors': authors,
                'title': titles,
                'link': links}

    print('\n\n=====\n\n')
    print(pd.DataFrame(top_dict))

    return pd.DataFrame(top_dict)
'''

def get_current_time():
    startTime = time.time()
    s_tm = time.localtime(startTime)

    return time.strftime('%Y-%m-%d', s_tm), time.strftime('%Y-%m-%d-%H:%M:%S', s_tm)

## set parser
def parse_opts():
    parser = argparse.ArgumentParser()

    parser.add_argument('--parser_type',
            default='hype-week',
            type=str,
            choices=['recent-week', 'recent-month', 'hype-week', 'hype-month'],
            help='parsing type from arxiv_sanity')

    parser.add_argument('--assets_root_dir',
            type=str,
            help='assets root dir')

    return parser

def statistic(path_list):

    statistic_df = pd.DataFrame([], columns=['no', 'date', 'title', 'link'])
    total_df = pd.DataFrame([], columns=['title', 'link'])

    # total_df['title'].value_counts(sort=True, ascending=False)

    link_table = {}

    # 1. make total df
    for path in path_list:
        assets_df = pd.read_csv(path)
        total_df = total_df.append(assets_df[['title', 'link']], ignore_index=True)

    # 2. update link table
    total_len = len(total_df)
    for i in range(0, len(total_df)):
        link_table[total_df.iloc[i]['title']] = total_df.iloc[i]['link']

    # 3. statistic df 
    statistic_df = total_df.groupby(['title']).size().reset_index().rename(columns={0:'count'})
    statistic_df = statistic_df.sort_values(by='count', ascending=False)

    statistic_df['link'] = 'None'

    for i in range(0, len(statistic_df)):
        title = statistic_df.iloc[i]['title']
        link = link_table[title]

        statistic_df.at[i, 'link']= link
    
    statistic_df = statistic_df.reset_index(drop=True)
    
    return statistic_df

def get_csv_assets(root_path, parser_type):
    target_dir = os.path.join(root_path, '*-*-*', 'top', '{}_*-*-*.csv'.format(parser_type)) # *-*-* : 2022-01-03",
    return natsort.natsorted(glob(target_dir))


if __name__ == "__main__":
    ### 0. init set up
    parser = parse_opts()
    args = parser.parse_args()

    top_assets_dir = args.assets_root_dir
    save_path = os.path.join(top_assets_dir, 'statistic-{}-{}.csv'.format(args.parser_type, get_current_time()[0]))

    # 1. get csv assets
    assets_paths = get_csv_assets(top_assets_dir, args.parser_type)
    # print(assets_paths)

    for path in assets_paths:
        print(path)

    # 2. statistic
    statistic_df = statistic(assets_paths)
    print(statistic_df)

    # 3. save
    statistic_df.to_csv(save_path)