codesearch
==========

Can be used to index any set of files and then search for keywords over the network. Useful where grep is too slow to be used.

This is a small project I took up to index up my entire codebase and another set of files which I need to search very frequently(using grep is painfully slow at that scale) and then serve the search results through a webpage using Django.

To use it, first create the index using the file createIndex.py. After that results can be served through a webserver.
