from Bio import Entrez
import argparse
import os
import sys
import xml.etree.ElementTree as ET
import codecs
import urllib
#### search function will retrieve PMIDs published during specified time 
# reldate = limit your search to only those items with a date within the last n days 
# retmax = max amount of results wanted
# datatype = determines which date field you wish to limit by, I have it set for one week now
query = "((((((((Biomedical and dental materials[MeSH Terms]) OR (Prostheses and implants[MeSH Terms])) OR (Materials testing[MeSH Terms])) OR (Tissue engineering[MeSH Terms])) OR (Tissue scaffolds[MeSH Terms])) OR (Equipment safety[MeSH Terms])) OR (Medical device recalls[MeSH Terms])) OR (Biomaterials)) OR (Cell scaffolds)"
#query_timed = '((((((((Biomedical and dental materials[MeSH Terms]) OR (Prostheses and implants[MeSH Terms])) OR (Materials testing[MeSH Terms])) OR (Tissue engineering[MeSH Terms])) OR (Tissue scaffolds[MeSH Terms])) OR (Equipment safety[MeSH Terms])) OR (Medical device recalls[MeSH Terms])) OR (Biomaterials)) OR (Cell scaffolds) AND "last 2 months" [crdt]'
api_key="1cab2a4456d4e64e48a7c83a9cc9c101dc09"
const_no_abstract = 0
def remove_invalid_characters(text):
    text = text.replace("\n"," ").replace("\t"," ").replace("\r"," ")    
    return text

def readTitle(title_xml):
    if(title_xml!=None):
        title=''.join(title_xml.itertext())
        return title
    return ''

def readAbstract(abstract_xml):
    abstract = []
    for abstractText in abstract_xml.findall("AbstractText"):
        abstract.append("".join(abstractText.itertext()))
    abstract = " ".join(abstract)  
    return abstract

def search_query(query,reldate):
    Entrez.email = 'email@bsc.es'
    if (reldate is not None):
        handle = Entrez.esearch(db='pubmed',  
                                rettype="xml", 
                                retmode="text", 
                                term=query,
                                usehistory="y",
                                reldate=reldate)
    else:
        handle = Entrez.esearch(db='pubmed',  
                                rettype="xml", 
                                retmode="text", 
                                term=query,
                                usehistory="y")
    results = Entrez.read(handle)
    return results

#### fetch_details function will retireve information for each PMID it receives
# retrieves year, title, abstract text as of now
def fetch_details(webenv, querykey, retstart, retmax, outputfolder, ids_list, registry_file, reldate):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    if (reldate is not None):
        values = {'db':'pubmed', 'rettype':'xml', 'retmode':'xml', 'WebEnv':webenv, 'query_key':querykey, 'retstart':retstart, 'retmax':retmax, 'reldate':reldate}
    else:
        values = {'db':'pubmed', 'rettype':'xml', 'retmode':'xml', 'WebEnv':webenv, 'query_key':querykey, 'retstart':retstart, 'retmax':retmax}
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        rpub = response.read()
        xmlResp = rpub.decode("utf-8") 
        docXml = ET.fromstring(xmlResp)
        with open(registry_file,'a') as list_files_standardized:
            for article in docXml.findall("PubmedArticle"):
                try:
                    year = "0000"
                    month = ''
                    title = ''
                    pmid = article.find("MedlineCitation").find("PMID").text
                    if(pmid+'.txt' not in ids_list):
                        article_xml = article.find("MedlineCitation").find("Article")
                        try: 
                            year = article_xml.find('Journal').find('JournalIssue').find('PubDate').find('Year').text
                        except Exception: 
                            try: 
                                medline_date = article_xml.find('Journal').find('JournalIssue').find('PubDate').find('MedlineDate').text
                                year = medline_date[0:4]
                            except Exception: 
                                print("Error with year:  " + pmid)  
                                year ='0000'
                        try: month = article_xml.find('Journal').find('JournalIssue').find('PubDate').find('Month').text
                        except Exception: 
                            try: 
                                medline_date = article_xml.find('Journal').find('JournalIssue').find('PubDate').find('MedlineDate').text
                                month = medline_date[5:]
                            except Exception:  
                                month =''
                        abstract_xml = article_xml.find("Abstract")
                        if(abstract_xml is not None):
                            abstract = readAbstract(abstract_xml)
                            title = readTitle(article_xml.find('ArticleTitle'))
                            if(abstract!=''):
                                with codecs.open(outputfolder+"/"+  pmid + '.txt', 'w',encoding='utf8') as txt_file:
                                    txt_file.write(remove_invalid_characters(title) + '\n' + remove_invalid_characters(abstract) + '\n')
                                    txt_file.flush()
                                    txt_file.close() 
                                with codecs.open(outputfolder+"/"+  pmid + '.meta', 'w',encoding='utf8') as txt_file:
                                    txt_file.write(str(year) + ' ' + str(month) + '\n')
                                    txt_file.flush()
                                    txt_file.close() 
                                    list_files_standardized.write(pmid + '.txt'+"\n")
                                    list_files_standardized.flush()
                                    
                        #else:
                            #print("Error with pmid no abstract:  " + pmid)      
                except Exception as inst:
                    print("Error with pmid: " + pmid)
    
if __name__ == '__main__':
    #add -term parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', help= 'Pubmed query to retrieve abstracts')
    parser.add_argument('-o', help= 'Path to folder of output folder')
    parser.add_argument('-r', help= 'Registry file to set the processed abstracts')
    parser.add_argument('-d', help= 'reldate, Only abstract in the previous reldate will be retrieved, if not this will be a baseline (all time) abstracts search ')
    
    
    #if term given, use term in search
    #if no term given, return only journal articles in english
    args = parser.parse_args()
        #create output folder if not exist
    if (args.o == None):
        print("Please set the output folder")
        sys.exit(1)
    if not os.path.exists(args.o):
        os.makedirs(args.o)
    if (args.q is not None):
        term_search = args.q
        print('Searching in pubmed query:' + term_search)
    else:
        print('Warning: Default Query will be used: ' + query)
        term_search = query
    if (args.r is None):
        print("Please set the registry file to set the processed abstracts")
        sys.exit(1)
    
    reldate=None
    if(args.d is not None):
        reldate=args.d
        print ("Only abstract in the previous " + reldate + " days added to Entrez will be returned in the search.")
    else:
        print ("No reldate is assigned, this will be a baseline (all time) abstracts search")
        
    print ("The registry file to review the updated abstracts is : " + args.r)
    print ("Warning: Take into account that this file contains the already past execution processed files.")
    
    ids_list=[]
    if(os.path.isfile(args.r)):
        with open(args.r,'r') as ids:
            for line in ids:
                ids_list.append(line.replace("\n",""))
        ids.close()
    retstart = 0
    retmax = 10000
    results = search_query(term_search,reldate)
    webenv=results["WebEnv"]
    querykey=results["QueryKey"]
    count = int(results['Count'])
    print ("Total abstracts in search query: " + str(count))
    search_while=True  
    first_time = True
    counter=1
    while (retstart < count):
        print ("Search from  " + str(retstart) +  " to " + str(retstart + retmax))
        subfolder = args.o
        #just in case there were more than 10000, the folder split starts 
        if(count>10000):
            subfolder = args.o + "/abstracts_"+ str(counter)
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)
        results = fetch_details(webenv, querykey, retstart, retmax, subfolder, ids_list, args.r, reldate)
        retstart=retstart+retmax
        counter = counter + 1
    print("Finish process")
    
