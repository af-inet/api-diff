#! /usr/bin/env python
#

import sys
import json
import requests

def diff(a, b):

    paths = []
    
    def _traverse(o1, o2, key=None, path=[]):
        
        # types dont match
        if key and (type(o1) is not type(o2)):
            if (o1 is None) or (o2 is None):
                paths.append("%-40s is sometimes missing" % ".".join(path))
            else:
                paths.append("%s can be '%s' or '%s'" % (".".join(path), type(o1).__name__, type(o2).__name__))
            return # don't traverse any further
        
        if type(o1) is list:
            _traverse(o1[0], o2[0]) # traverse the first item in each list

        elif type(o1) is dict:
            # traverse each key in a dictionary
            for k in o1:
                _traverse(o1.get(k, None), o2.get(k, None), key=k, path=path+[k])

        else:
            # these two leaves are the same
            pass

    _traverse(a, b)

    return paths

# diff every item in a list against every other item.
def diff_set(data):
    return (
        sorted(list(set([
            item
            for i in range(len(data))
                for j in range(i + 1, len(data))
                    for item in diff(data[i], data[j])
        ])))
    )

def print_list(title, strings):
    print(
        "{title}:\n{items}".format(
              title = title
            , items = "\n".join(map(lambda s: "\t" + s, strings))
        )
    )

def report(urls):

    print_list("urls", urls)

    data = \
        reduce( lambda a, b: (a + b)
                , map( lambda url: (requests.get(url).json()["data"])
                        , urls))

    print_list("diff", diff_set(data))

def main():
    
    report([
          "http://api.giphy.com/v1/gifs/search?q=cat&api_key=dc6zaTOxFJmzC"
        , "http://api.giphy.com/v1/gifs/search?q=dog&api_key=dc6zaTOxFJmzC"
        , "http://api.giphy.com/v1/gifs/search?q=meme&api_key=dc6zaTOxFJmzC&limit=10"
        , "http://api.giphy.com/v1/gifs/search?q=wtf&api_key=dc6zaTOxFJmzC&limit=10&offset=10"
        , "http://api.giphy.com/v1/gifs/search?q=sick&api_key=dc6zaTOxFJmzC&offset=10"
        ])

main()
