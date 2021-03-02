# pubmed_retrieval

This implementation of the Entrez module takes a desired time frame and retreives PMID, title, abstract, and publication date (month and year) of all records archived by PubMed over that period.  

## Description 
The implementation contains 3 functions:
1. The 'search' function retrieves PMIDs of records published during user's specified time frame (e.g.: the last 10 days)
2. The 'fetch_details' function retireves information (PMID, title, abstract, and publication date- month and year) for each PMID. It is possible to include search terms for more specific retrieval. In this implementation, the function only writes to file jounral articles in English with abstract text.  


## Run the Docker 
	
	

## Parameters:
reldate = limit your search to items with a publication date in the last n days 
retmax = maximum number of records allowed
datatype = determines the date field you wish to limit 

## Built With

* [Bio.Entrez](https://biopython.org/DIST/docs/api/Bio.Entrez-module.html)
* [Docker](https://www.docker.com/) - Docker Containers

## Authors

* **Austin Mckitrick - Javier Corvi ** 


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE](LICENSE.txt) file for details

## Funding

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No 751277

		
