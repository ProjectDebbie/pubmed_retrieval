# pubmed_standardization

This library takes the PubMed information stored in a working directory and standarize the information in plain text.

## Description 

The input directory contains the PubMeds *.gz files, so the first task executed for the library is unzip the files.  

After unziped the files, the standardization begins,  the xml's PubMed that contains the articles are readed and generate for each article a PMIDXXX.txt.

This library can be use as a step of a pipeline with the objective of generates plain text of the PubMed articles.
 

The actual format is of the plain text files is:

year month
pmid
title
abstract

## Actual Version: 1.0, 2020-05-12
## [Changelog](https://github.com/ProjectDebbie/pubmed_standardization/blob/master/CHANGELOG) 
## Docker
debbieproject/pubmed_standardization

## Run the Docker 
	
	#To run the docker, just set the input_folder and the output
	docker run -v ${PWD}/pubmed:/in -v ${PWD}/standardization_output:/out pubmed_standardization:version python3 /app/pubmed_standardization.py -i /in -o /out

Parameters:
<p>
-i input folder. Will process subfolder also.
</p>
<p>
-o output folder.
</p>

## Built With

* [Docker](https://www.docker.com/) - Docker Containers

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ProjectDebbie/pubmed_standardization/releases). 

## Authors

* **Javier Corvi - Austin Mckitrick - Osnat Hakimi ** 


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE](LICENSE.txt) file for details
		
