import urllib.request, urllib.error, urllib.parse
import json
import pandas
from urllib.parse import urlparse
import os
from tqdm import tqdm
import socket

def create_database(tumblr, nmax=None):
    NPOSTS = 20

    tags = []
    urls = []
    names = []

    start = 0

    pbar = tqdm()
    while True:
        url = "https://%s.tumblr.com/api/read/json?type=photo&num=%d&start=%d#_=_" % (tumblr, NPOSTS, start)
        pbar.write('asking new page %s' % url)
        try:
            response = urllib.request.urlopen(url, timeout=3).read()
            response = response.decode()
        except socket.timeout:
            pbar.write('timeout')
            break
        start += NPOSTS
        response = response.replace('var tumblr_api_read = ', '').replace(';\n', '')
        pbar.write('reading new page')
        r = json.loads(response)

        if len(r['posts']) == 0:
            break

        pbar.write('analyzing new page')
        for ipost in range(len(r['posts'])):
            url = r['posts'][ipost]['photo-url-400']
            ext = os.path.splitext(url)[1]
            if ext not in ['.jpg', '.JPG']:
                continue
            if 'tags' not in list(r['posts'][ipost].keys()):
                continue
            tags.append(r['posts'][ipost]['tags'])
            urls.append(url)
            name = urlparse(r['posts'][ipost]['photo-url-400']).path.split('/')[1]
            names.append(name)
            pbar.update(1)

        if nmax is not None and len(names) > nmax:
            break

    df = pandas.DataFrame({'uri': urls, 'tags': tags, 'image_id': names})
    df = df.set_index('image_id')
    df = df[~df.index.duplicated(keep='first')]

    print("dowloaded: %s" % len(df))
    
#    df.to_csv('output_tumblr_%s.csv' % tumblr)
    df.to_json('output_tumblr_%s.json' % tumblr)
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Download url of tumblr images')
    parser.add_argument('tumblr', help='the name of the tumblr')
    parser.add_argument('--max', type=int)
    args = parser.parse_args()
    create_database(args.tumblr, nmax=args.max)
