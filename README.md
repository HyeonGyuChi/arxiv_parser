# arxiv_parser

## function
### parsering for [arxiv_sanity](http://arxiv-sanity.com/toptwtr?timefilter=week)
1. parsing the rank of [hype month, hype week, recent month, recent week]
2. searching monitoring keyword from arxiv (from hype month, hype week, recent month, recent week)

## enviroments
- macOS Big Sur 11.5.2
- python 3.8.4
- requirements.txt


## args
```bash
- parser_type: str, default='hype-week', choices=['recent-week', 'recent-month', 'hype-week', 'hype-month', 'all'] # parsing type from arxiv_sanity, if all, it will process all of choices
- keywork: str # monitoring keyword (parsing from title, abstract of papers)
- head: int, default=15  # the number of parsing from top rank
```

## how to use
1. command
```bash
$ python3 parser.py --parser_type "all" --keyword "variationl" --head 15 # processing all
$ python3 parser.py --parser_type "hype-week" --keyword "variationl" --head 15 # processing separately
```
2. bash command file
just double click parser.command
    - before use, check absolute dir of parser.py
    - before use, check chmod 777 on parser.command

## results
```bash
/results
    /21-12-28 # automatic set to current date
        /top # top ranking, you can adjust to head
            hype-month_2021-12-28.csv
            hype-week_2021-12-28.csv
            recent-month_2021-12-28.csv
            recent-week_2021-12-28.csv
        /keword # monitoring keyword
            /variational
                hype-month_2021-12-28_variational.csv
                hype-week_2021-12-28_variational.csv
                recent-month_2021-12-28_variational.csv
                recent-week_2021-12-28_variational.csv
            ...
    ...
```
![how_to_use_shell_img](https://user-images.githubusercontent.com/79900862/147534015-85d6c118-df4b-4284-994a-6a061d841289.png)

## caution
1. Be careful with overwriting when saving results csv
2. If you request "get" to arxiv web page more than 100 times, the server may be down.
3. For searching monitoring keyword, it parses from 100 papers data.

## update log
### 21.12.28
1. init project, ver 1.0

### 21.12.29
1. add bash command file on mac (to use double click)
