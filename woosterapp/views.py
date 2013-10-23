from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings

from whoosh.index import open_dir
from whoosh.fields import Schema,TEXT,ID
from whoosh.qparser import QueryParser
from whoosh.query import Every
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

#use django settings for this. put in static files may be.
schema = Schema(path=ID(stored=True),filetype=TEXT(stored=True), uipath=TEXT, content=TEXT)
ix = open_dir(settings.INDEX_DIR+"/woosterapp",schema=schema)
ext_list = settings.EXT_LIST

def index(request):
    return render_to_response('woosterapp/index.html', 
                              {'ext_list':ext_list},
                              context_instance=RequestContext(request),)

def showfile(request, docnum):
    with ix.searcher() as searcher:
        alldocs = searcher.search(Every(), limit=None)
        with open(alldocs[int(docnum)]["path"]) as content_file:
            cont = content_file.read()
    return render_to_response('woosterapp/file.html', {
                                'filecontent': cont,
                                'query_term' : request.session['query_term'],
                                })
    #return HttpResponse("Here you are" + str(docnum))

def formResults(request):
    try:
        ext_list = ["cpp","h","hpp","txt","c"]  #TODO. take it from post values
        query_term = request.POST['query_term']
    except (KeyError):
        # Redisplay the poll voting form.
        return render_to_response('woosterapp/index.html', {
            'error_message': "You didn't specify a query.",
        }, )
    else:
        #return HttpResponseRedirect(reverse('woosterapp.views._results', args=(query_term,ext_list)))
        return HttpResponseRedirect(reverse('woosterapp.views.results', args=(query_term,)))

def results(request, query_term):
    return _results(request, query_term, ext_list)


def filteredresults(request, query_term, filetype):
    return _results(request, query_term, [filetype])

def _results(request, query_term, ext_list):
    request.session['query_term'] = query_term
    with ix.searcher() as searcher:
        #search file content
        query = QueryParser("content", ix.schema).parse(unicode(query_term))
        results_list = searcher.search(query, limit=None)
        if ext_list:
            print ext_list[0]
        print results_list.scored_length()

        response = render_to_response('woosterapp/results.html',
                                      {'results_list': results_list,
                                       'query_term': query_term,
                                       'filetypelist': ext_list
                                       },
                                      )
    return response