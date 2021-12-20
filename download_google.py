from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('--directory')
parser.add_argument('--max', type=int, default=200)
parser.add_argument('--prefix')
args = parser.parse_args()

if not args.directory:
    args.directory = 'google_%s' % args.query

google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,
                                    storage={'root_dir': args.directory})

try:
    google_crawler.crawl(keyword=args.query, offset=0, max_num=args.max,
                         date_min=None, date_max=None,
                         min_size=(200,200), max_size=None)
finally:
    if args.prefix is not None:
        print("adding prefix")
        import os
        import glob
        fs = glob.glob(os.path.join(args.directory, '*'))
        for fn in fs:
            os.rename(fn,
                      os.path.join(os.path.split(fn)[0], args.prefix + "_" + os.path.split(fn)[1]))


