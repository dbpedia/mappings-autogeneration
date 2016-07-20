# mappings-autogeneration

### Template Mapping

Given a Wikipedia template, our goal is to map it to a DBpedia ontology class when possible. The approach is instance-based: exploit the Wikipedia pages (instances) already mapped with a DBpedia class and their cross language links to the pages that the template to be mapped. A simple method based on the frequencies of the resulting classes allows us to tune the tradeoff between precision and recall. 

![Alt](/Images/figure1.png)

The mapping algorithm is summaried in the above figure and implemented as follows:

- Given as input infobox taken from a version of Wikipedia in a specific language, we collect all the page that include this infobox.
- Use the cross-language links to retrieve the pages in the selected pivot languages, for which we know the DBpedia classes.
- Collect the DBpedia classes of these pages and count their number of occurrences.
- The input infobox is then mapped to the most frequent class. A parameter **L** between 0 and 1 is used to filter the class whose frequency is less than **L**. In addition, we ignore the infox whose occurrence **C** is too small, like less than **C** = 10.

### Use Information from Wikidata 

Quite a bit entities in wikidata has a DBpedia ontology types assigned already. In addition, we have links between wikidata and other languages. As a result, we can treat wikidata as a pivot language directly. The information from wikidata can be useful to improve the performance of our approach. 

### Class Assignment

DBpedia stores the cross-language information, but it's not used to map the infoboxes. For example, Clint Eastwood is classified as **Actor** in the French and as **Person** in the Italian one. As a result, we need to find a strategy to classify pages in all languages to the most specific class. The strategy is defined as follows:

- If the page belongs to more than one ontology class, the lowest common ancestor of these classes is assigned.
- In the above case, if the classes are connected in a chain of subclass of relations, we consider the most specific class.

### Source Code and Usage

The source codes are all stored in the **Code** directory.

- ```config.py``` defines the paths and parameters in the program. Modify it to fit your own environment if necessary.
- ```download.py``` can download the needed datasets for a specified language.
- ```parse.py``` transforms the given data into the entity matrix, given the target language and the pivot language, see **Example** for details.
- ```predict.py``` gives predicted mapping for the target language based on the given pivot languaes. With option "-e", it can also calculate the precision and recall of the target language based on the existing mapping on DBpedia.
- ```workflow.py``` combine all the above modules together. You can simply run this script to conduct the whole workflow including download, parse, predict and evaluate. 

### Example

After use ```parse.py```, we can get a matrix as follows for the given target language and pivot language:

template_zh | article_zh | template_en | article_en | class
:---------: | :--------: | :---------: | :--------: | :---:|
Authority_control | Slackware | Infobox_OS | Slackware | Software 
Authority_control | OpenSUSE | Authority_control | OpenSUSE | owl#Thing
Authority_control | FreeBSD | Infobox_OS | FreeBSD | Software

### Experiments

In the experiments, we exploits existing handcrafted mappings in six languages (English, Italian, German, Portuguese, Spanish, French). Experiments have benn carried out on 5 languages (Bulgarian, Czech, Indonesian, Dutch and Catalan).

Precision and recall values are calculated using existing mappings from DBpedia official mapping website as gold standard.

For Bulgarian, we have the following results (The results are stored in these files: [data_without_wikidata](/Plot/data_without_wikidata.csv) and [data_with_wikidata](/Plot/data_with_wikidata.csv))

![Alt](/Plot/figure1.png)

### Case Study

When **L** is 0.5, **C** is 10, there are five miss classified cases in Bulgarian:

label | predict | LCA
:---- | :------ | :--
Film  | Actor   | owl#Thing
Place | AdministrativeRegion | Place
Person | Writer | Person
Settlement | Village | Settlement
FormulaOneRacing | GrandPrix | owl#Thing

From which, we can find that there are 3 out of 5 cases that the predicted class is a subclass of the labeled class. In the current evaluation metric, we treat them as false positives which is not that accurate. As a result, we'd better propose a better evaluation metric.

### High-quality Output Mappings for Chinese

Setting **L** as 0.9 and **C** as 100, I get 501 mappings for Chinese. After manual checking, I filter out 456 high-quality mappings as output of the project, which can be found in [this file](/Output/predicted/zh.csv). 
