from bio import Entrez
import argparse
import os

#### search function will retrieve PMIDs published during specified time 
# reldate = limit your search to only those items with a date within the last n days 
# retmax = max amount of results wanted
# datatype = determines which date field you wish to limit by, I have it set for one week now
def search(query):
    Entrez.email = 'amckitri@bsc.es'
    handle = Entrez.esearch(db='pubmed',  
                            retmax='1100',
                            rettype="xml", retmode="text", 
                            term=query)
                            # ,
                            # datetype='pdat',
                            # reldate=7)
    results = Entrez.read(handle)
    return results
#### fetch_details function will retireve information for each PMID it receives
# retrieves year, title, abstract text as of now
def fetch_details(id_list):
    pmids = id_list
    Entrez.email = 'amckitri@bsc.es'
    handle = Entrez.efetch(db='pubmed',
                           rettype='xml',
                           id=pmids, retmode="text")
    results = Entrez.read(handle)
    #pubmed has one book record that is still returned given the journal articles search restriction....i don't know why
    abstract = ''
    year = "NA"
    month = ''
    title = ''
    pmid = ''
    for i in pmids:
        for pubmed_article in results['PubmedArticle']:
            pmid = int(str(pubmed_article['MedlineCitation']['PMID']))
            article = pubmed_article['MedlineCitation']['Article']
            try: year = pubmed_article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year']
            except KeyError: year ='NA'
            try: month = pubmed_article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Month']
            except KeyError: month=''
            title = article['ArticleTitle']
            if 'Abstract' in article:
                 if len(article['Abstract']['AbstractText']) == 1:
                     abstract = str(article['Abstract']['AbstractText'][0])
                 if len(article['Abstract']['AbstractText']) == 2:
                     abstract = str(article['Abstract']['AbstractText'][0]) + " " + str(article['Abstract']['AbstractText'][1])
                 if len(article['Abstract']['AbstractText']) == 3:
                     abstract = str(article['Abstract']['AbstractText'][0]) + " " + str(article['Abstract']['AbstractText'][1]) + " " + str(article['Abstract']['AbstractText'][2])
                 if len(article['Abstract']['AbstractText']) == 4:
                     abstract = str(article['Abstract']['AbstractText'][0]) + " " + str(article['Abstract']['AbstractText'][1]) + " " + str(article['Abstract']['AbstractText'][2]) + " " + str(article['Abstract']['AbstractText'][3])
                 if len(article['Abstract']['AbstractText']) == 5:
                     abstract = str(article['Abstract']['AbstractText'][0]) + " " + str(article['Abstract']['AbstractText'][1]) + " " + str(article['Abstract']['AbstractText'][2]) + " " + str(article['Abstract']['AbstractText'][3]) + " " + str(article['Abstract']['AbstractText'][4])
                 if len(article['Abstract']['AbstractText']) == 6:
                     abstract = str(article['Abstract']['AbstractText'][0]) + " " + str(article['Abstract']['AbstractText'][1]) + " " + str(article['Abstract']['AbstractText'][2]) + " " + str(article['Abstract']['AbstractText'][3]) + " " + str(article['Abstract']['AbstractText'][4]) + " " + str(article['Abstract']['AbstractText'][5])
                 if len(article['Abstract']['AbstractText']) == 7:
                     abstract = str(article['Abstract']['AbstractText'][0]) + " " + str(article['Abstract']['AbstractText'][1]) + " " + str(article['Abstract']['AbstractText'][2]) + " " + str(article['Abstract']['AbstractText'][3]) + " " + str(article['Abstract']['AbstractText'][4]) + " " + str(article['Abstract']['AbstractText'][5]) + " " + str(article['Abstract']['AbstractText'][6])
            else:
                 pass
        else:
            pass
#only return records with abstract text
        if len(abstract) != 0:
            return str(str(year) + ' ' + str(month) + '\n' + str(pmid) + '\n' + str(title) + '\n' + str(abstract))
if __name__ == '__main__':
    #add -term parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('-term', help= 'enter desired seach term, use '' around term')
    parser.add_argument('-OR', action='store_true', help= 'adds OR specification to term search')
    parser.add_argument('-AND', action='store_true', help= 'adds AND specification to term search')
    parser.add_argument('-term2', help= 'enter desired seach term, use '' around term')
    parser.add_argument('-o', help= 'paste path to folder of output folder')
    #if term given, use term in search
    #if no term given, return only journal articles in english
    args = parser.parse_args()
        #create output folder if not exist
    if not os.path.exists(args.o):
        os.makedirs(args.o)
    if (args.term == None):
        term_search = str('(("journal article"[Publication Type]) AND "english"[Language]) NOT "review"[Publication Type]')
        print('Finding...PubMed Journal Articles in English')
    elif (args.OR == True):
        term_search = str('(((("journal article"[Publication Type]) AND "english"[Language]) AND' + " " + args.term + '[Text Word]) OR' + " " + args.term2 + '[Text Word]) NOT "review"[Publication Type]')
        print('Finding...PubMed Journal Articles in English containing'+ " " + args.term + " OR " + args.term2)
    elif (args.AND == True):
        term_search = str('(((("journal article"[Publication Type]) AND "english"[Language]) AND' + " " + args.term + '[Text Word]) AND' + " " + args.term2 + '[Text Word]) NOT "review"[Publication Type]')
        print('Finding...PubMed Journal Articles in English containing'+ " " + args.term + " AND " + args.term2)
    elif (args.term !=None):
        term_search = str('(("journal article"[Publication Type]) AND "english"[Language]) AND' + " " + args.term + '[Text Word]')
        print('Finding...PubMed Journal Articles in English containing'+ " " + args.term)
    else:
        raise KeyError('Your search is incomplete. Please make sure your arguments are correct. See README for examples.')
    # str('(("journal article"[Publication Type]) AND "english"[Language]) AND' + " " + args.term + '[Text Word]')
    # term_search = str('(((("journal article"[Publication Type]) AND "english"[Language]) AND polydioxanone[Text Word]) OR PDSII[Text Word]) NOT "review"[Publication Type]')
    results = search(term_search)
    id_list = results['IdList']
    counter = 0
    for i in id_list:
        results = fetch_details(i)
#only write files with those records with abstract text
        if results != None:
            counter += 1
            filePath = args.o+"/"+'%s.txt' % (i)
            file = open(filePath, 'w')
            file.write(results)
    print('Search Complete!\nNumber of results found:', counter)