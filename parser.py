import os
import time
import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import argparse

## set parser
def parse_opts():
    parser = argparse.ArgumentParser()

    parser.add_argument('--parser_type',
            default='hype-week',
            type=str,
            choices=['recent-week', 'recent-month', 'hype-week', 'hype-month', 'all'],
            help='parsing type from arxiv_sanity, if all, it will process all of choices')
    
    parser.add_argument('--keyword',
            type=str,
            help='monitoring keyword (parsing from title, abstract of papers)')
    
    parser.add_argument('--head',
            default=15,
            type=int,
            help='the number of parsing from top rank')


    return parser

## parsing from arvix web page
def parsing_arxiv(parser_type):

    url_table = {
        'recent-week': "http://arxiv-sanity.com/top?timefilter=week&vfilter=all",
        'recent-month': "http://arxiv-sanity.com/top?timefilter=month&vfilter=all",
        'hype-week': "http://arxiv-sanity.com/toptwtr?timefilter=week",
        'hype-month': "http://arxiv-sanity.com/toptwtr?timefilter=month",
    }

    page = requests.get(url_table[parser_type])
    soup = bs(page.text, "html.parser")

    script = soup.findAll('script')[6] # json data in </sciprts>

    s = script.string # convert str
    s = s.split('var papers = ')[1] # split 1
    s = s.split(';\n') # split 2
    s = s[0] # core data(str)
    # print(s)

    # str => json
    json_data = json.loads(s)

    return json_data # number of papers = 100


## extract top rank of json_data(from arvix)
def extract_top(json_data, head=15):        

    no = []
    titles= []
    links= []

    for i, data in enumerate(json_data[:head]):
        # print(len(data)) # 14 | keys = {'abstract', 'authors', 'category', 'comment', 'img', 'in_library', 'link', 'num_discussion', 'originally_published_time', 'pid', 'published_time', 'rawpid', 'tags', 'title'}
        no.append(i+1)
        titles.append(data['title'].replace('\n ', ''))
        links.append(data['link'])
    
    # list => df
    top_dict = {'no': no,
                'date': get_current_time()[0],
                'title': titles,
                'link': links}

    return pd.DataFrame(top_dict)

## searching monitoring keyword from title or abstract of 100 papers
def search_monitoring_papers(json_data, keyword):
    no = []
    titles = []
    abstrats = []
    links = []
    remarks = []

    for i, data in enumerate(json_data[:]): # number of papers = 100
        # print(len(data)) # 14 | keys = {'abstract', 'authors', 'category', 'comment', 'img', 'in_library', 'link', 'num_discussion', 'originally_published_time', 'pid', 'published_time', 'rawpid', 'tags', 'title'}
        abstrat = data['abstract'].replace('\n', '')
        title = data['title'].replace('\n ', '')
        
        abstrat_remark = keyword in abstrat.lower()
        title_remark = keyword in title.lower()

        if abstrat_remark or title_remark:
            no.append(i+1)
            abstrats.append(abstrat)
            titles.append(title)
            links.append(data['link'])
            remarks.append(','.join(['title', 'abstract'][i]for i, val in enumerate([abstrat_remark, title_remark]) if val))
    
    monitoring_dict = {
        'no': no,
        'date': get_current_time()[0],
        'keyword': keyword,
        'title': titles,
        'abstract': abstrats,
        'remark': remarks,
        'link': links,
    }

    return pd.DataFrame(monitoring_dict)

def get_current_time():
    startTime = time.time()
    s_tm = time.localtime(startTime)
    
    return time.strftime('%Y-%m-%d', s_tm), time.strftime('%Y-%m-%d-%H:%M:%S', s_tm)

if __name__ == "__main__":
    ### 0. init set up
    parser = parse_opts()
    args = parser.parse_args()

    save_dir = os.path.join('./results', get_current_time()[0])
    top_save_dir = os.path.join(save_dir, 'top')
    keyword_save_dir = os.path.join(save_dir, 'keyword', args.keyword)
    os.makedirs(top_save_dir, exist_ok=True)
    os.makedirs(keyword_save_dir, exist_ok=True)    
    
    if args.parser_type == 'all':
        parser_stack = ['recent-week', 'recent-month', 'hype-week', 'hype-month']
    else :
        parser_stack = [args.parser_type]

    for parser_type in parser_stack:
        # 1. parsing json data from web
        arxiv_json_data = parsing_arxiv(parser_type)
        
        # 2. extract top (title)
        top_df = extract_top(arxiv_json_data, args.head)

        # 3. parsing_arxiv
        print('\n\n==================== ARVIX TOP RESULTS \t\t | parser_type: {} ====================\n\n'.format(parser_type))
        print(top_df)
        top_df.to_csv(os.path.join(top_save_dir, '{}_{}.csv'.format(parser_type, get_current_time()[0])), index=False)
        print('===> SAVE DIR: {}'.format(os.path.abspath(top_save_dir)))

        # 4. searching monitoring
        print('\n\n==================== ARVIX MONITORING RESULTS \t | keyword: {} ====================\n\n'.format(args.keyword))
        monitoring_df = search_monitoring_papers(arxiv_json_data, args.keyword)
        print(monitoring_df)
        monitoring_df.to_csv(os.path.join(keyword_save_dir, '{}_{}_{}.csv'.format(parser_type, get_current_time()[0], args.keyword)), index=False)
        print('===> SAVE DIR: {}'.format(os.path.abspath(keyword_save_dir)))

    