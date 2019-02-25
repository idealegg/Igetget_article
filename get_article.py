#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os
import sys
import traceback
import requests
import json
import re
import chardet
import time


class __redirection__:
    def __init__(self, file):
        self.buff=""
        self.file=file
        self.__console__=sys.stdout
        self.fd=open(self.file, 'w')
        sys.stdout = self

    def write(self, output_stream):
        sys.__stdout__.write(output_stream)
        if output_stream:
          if type(output_stream) is not unicode:
            self.fd.write(output_stream.decode(chardet.detect(output_stream)['encoding']).encode('utf-8'))
          else:
            self.fd.write(output_stream.encode('utf-8'))

    def flush(self):
        sys.__stdout__.flush()
        self.fd.flush()

    def __del__(self):
        try:
          sys.stdout=self.__console__
          self.fd.close()
        except :
          pass


def GetSens2(out_dir, url):
  print "url: %s" % url
  title = url[url.rfind('/')+1:]
  author = ''
  try:
    if not os.path.isdir(out_dir):
      os.mkdir(out_dir)
    req = requests.get(url)
    #print req.content
    s = req.content[req.content.find(index_str) + len(index_str):]
    req.close()
    try:
      j1 = json.loads(s)
    except ValueError, e:
      res = re.search("Extra data: line 1 column\s*(\d+)", e.message)
      if res:
        j1 = json.loads(s[:int(res.group(1), 10)-1])
      else:
        raise
    except:
      raise
    contents = []
    if j1['page']['article_content'].has_key('title'):
      title = j1['page']['article_content']['title']
    if j1['page']['article_content'].has_key('author'):
      author = j1['page']['article_content']['author']['name']
    print title
    for content in j1['page']['article_content']['content']:
      if content['type'] == 'text':
        contents.extend(content['value'].replace('<p>', '').split('</p>'))
    fd = open(os.path.join(out_dir, "%s_%s.txt" % (title, author)), 'wb')
    fd.write("\n".join(contents).encode('utf8'))
    fd.close()
    return True
  except Exception, e:
    traceback.print_exc()
    print e.message
    print url
    return False


if __name__ == "__main__":
  __redirection__('out_%s.log' % time.strftime("%Y-%m-%d_%H%M%S"))
  index_str = 'window.__INITIAL_STATE__='
  url = 'https://m.igetget.com/share/course/article/article_id/%d'
  out_dir = "texts"
  done_file = 'done.txt'
  done_list = []
  if os.path.isfile(done_file):
    fd = open(done_file)
    done_list = [i[:-1] for i in fd]
    fd.close()
  fd = open(done_file, 'wb+')
  ids = range(61826, 68001)
  for id in ids:
    if str(id) not in done_list:
      if GetSens2(out_dir, url % id):
        fd.write("%d\n" % id)
        fd.flush()
  fd.close()