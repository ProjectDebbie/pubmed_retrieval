from bio import Entrez

#### search function will retrieve PMIDs published during specified time 
# reldate = limit your search to only those items with a date within the last n days 
# retmax = max amount of results wanted
# datatype = determines which date field you wish to limit by, I have it set for one week now
def search(query):
    Entrez.email = 'amckitri@bsc.es'
    handle = Entrez.esearch(db='pubmed',  
                            retmax='100',
                            rettype="xml", retmode="text", 
                            term=query,
                            datetype='pdat',
                            reldate=7)
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
    abstract = ''
    for i in pmids:
         for pubmed_article in results['PubmedArticle']:
             pmid = int(str(pubmed_article['MedlineCitation']['PMID']))
             article = pubmed_article['MedlineCitation']['Article']
             try: year = pubmed_article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year']
             except KeyError: year='NA'
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
         return (str(year) + ' ' + str(month) + '\n' + str(pmid) + '\n' + str(title) + '\n' + str(abstract))

if __name__ == '__main__':
	#only restrictions are if its a journal article and in english
	#any more?
    results = search(('((("journal article"[Publication Type])) AND "english"[Language]'))
    id_list = results['IdList']
#    print(len(id_list))
    for i in id_list:
    	results = fetch_details(i)
    	filePath = '/Users/austinmckitrick/git/debbie/pubmed_retrieval/abstracts/%s.txt' % (i)
    	file = open(filePath, 'w')
    	file.write(results)


