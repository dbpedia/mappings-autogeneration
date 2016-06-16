# mappings-autogeneration

### Template Mapping

Given a Wikipedia template, our goal is to map it to a DBpedia ontology class when possible. The approach is instance-based: exploit the Wikipedia pages (instances) already mapped with a DBpedia class and their cross language links to the pages that the template to be mapped. A simple method based on the frequencies of the resulting classes allows us to tune the tradeoff between precision and recall. 

![Alt](/Images/figure1.png)

The mapping algorithm is summaried in the above figure and implemented as follows:

- Given as input infobox taken from a version of Wikipedia in a specific language, we collect all the page that include this infobox.
- Use the cross-language links to retrieve the pages in the selected pivot languages, for which we know the DBpedia classes.
- Collect the DBpedia classes of these pages and count their number of occurrences.
- The input infobox is then mapped to the most frequent class. A parameter between 0 and 1 is used to filter the class whose frequency is less than the parameter. In addition, we ignore the infox whose occurrence is too small, like less than 10.

### Source Code and Usage

The source codes are all stored in the **Code** directory.

- ```config.py``` defines the paths and parameters in the program. Modify it to fit your own environment if necessary.
- ```download.py``` can download the needed datasets for a specified language.
- ```parse.py``` transforms the given data into the entity matrix, given the target language and the pivot language, see **Example** for details.
- ```evaluate.py``` gives the precision and recall of a target language based on the given pivot languages.

### Example

After use ```parse.py```, we can get a matrix as follows for the given target language and pivot language:

|template_zh|article_zh |template_en|article_en|class|
|-:|-:|-:|-:|-:|
||||||
||||||
||||||

### Experiments
