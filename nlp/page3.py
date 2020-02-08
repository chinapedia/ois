# pip3 install --upgrade gensim
# wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
# extract GoogleNews-vectors-negative300.bin.gz
# https://code.visualstudio.com/docs/remote/ssh
# Install the Remote Development extension pack.
# https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh

"""
# wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
--2019-12-22 10:51:00--  https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
Resolving s3.amazonaws.com (s3.amazonaws.com)... 52.216.65.179
Connecting to s3.amazonaws.com (s3.amazonaws.com)|52.216.65.179|:443... connected.
HTTP request sent, awaiting response... 206 Partial Content
Length: 1647046227 (1.5G), 1647046092 (1.5G) remaining [application/x-gzip]
Saving to: ‘GoogleNews-vectors-negative300.bin.gz’

GoogleNews-vectors-negative300.bin.g 100%[=====================================================================>]   1.53G  8.32MB/s    in 4m 18s  

2019-12-22 10:55:19 (6.10 MB/s) - ‘GoogleNews-vectors-negative300.bin.gz’ saved [1647046227/1647046227]
"""

"""
extract () {
   if [ -f $1 ] ; then
       case $1 in
           *.tar.bz2)   tar xvjf $1    ;;
           *.tar.gz)    tar xvzf $1    ;;
           *.bz2)       bunzip2 $1     ;;
           *.rar)       unrar x $1       ;;
           *.gz)        gunzip $1      ;;
           *.tar)       tar xvf $1     ;;
           *.tbz2)      tar xvjf $1    ;;
           *.tgz)       tar xvzf $1    ;;
           *.zip)       unzip $1       ;;
           *.Z)         uncompress $1  ;;
           *.7z)        7z x $1        ;;
           *)           echo "don't know how to extract '$1'..." ;;
       esac
   else
       echo "'$1' is not a valid file!"
   fi
}
"""
import pprint
from gensim.test.utils import common_texts, get_tmpfile, datapath
from gensim.models import Word2Vec, KeyedVectors
import gensim.matutils

binPath = "/root/GoogleNews-vectors-negative300.bin"
binPath = "/Users/liruqi/GoogleNews-vectors-negative300.bin"
print(binPath)
# Gensim can load word vectors in the “word2vec C format”, as a KeyedVectors instance:
wv_from_bin = KeyedVectors.load_word2vec_format(datapath(binPath), binary=True)
v1 = wv_from_bin.wv['man']
v2 = wv_from_bin.wv['woman']
pprint.pprint(v1)
pprint.pprint(v2)
pprint.pprint(wv_from_bin.similarity('man','woman'))
pprint.pprint(wv_from_bin.distance('man','woman'))
pprint.pprint(1 - wv_from_bin.n_similarity(
    "National tragedy Trump begins border wall construction in Unesco reserve".split(" "),
    "Trump administration enters new phase for border wall sets ambitious timetable after securing land".split(" ")
    )
)

"""
# python3 page3.py
Traceback (most recent call last):
  File "page3.py", line 50, in <module>
    wv_from_bin = KeyedVectors.load_word2vec_format(datapath("/root/GoogleNews-vectors-negative300.bin"), binary=True)
  File "/usr/local/lib/python3.6/dist-packages/gensim/models/keyedvectors.py", line 1498, in load_word2vec_format
    limit=limit, datatype=datatype)
  File "/usr/local/lib/python3.6/dist-packages/gensim/models/utils_any2vec.py", line 349, in _load_word2vec_format
    result.vectors = zeros((vocab_size, vector_size), dtype=datatype)
MemoryError: Unable to allocate array with shape (3000000, 300) and data type float32
"""
