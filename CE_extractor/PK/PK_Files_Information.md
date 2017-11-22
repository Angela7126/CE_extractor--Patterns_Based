# Explaining contents of Each File in ./PK

Each .pk file is a data file stored by pickle package.

```python
import pickle
import codecs   # codecs is a package to change the encoding way of a file.

fpath = ur"./"  # The file path where you want to store or reload your data.
# ---- Store data ----
fp = codecs.open(fpath, 'wb', 'utf8')
pickle.dump(result, fp)
fp.close()
# ---- Load data ----
fp = open(fpath, 'rb')
result = pickle.load(fp)
fp.close()
```



## PK files in the ./PK/CEPerDic directory

+ Each f00xx_CE.pk file stores the *CElink* objects extracted from the corresponding paper.

## PK files in the ./PK/TXT directory
+ Each f00xx.txt file store the *Paper* object constructed for the corresponding paper.

## PK files in the ./PK/DIC directory

### KGPaperList.pk
+ Store all the *Paper* objects build for each scientific papers in KG Corpus. (the KG corpus includes 39 scientific papers, labeled as f0001~f0039).
+ The definition of *Paper* class, please refer to **cmyPackage.py**.
+ The first element in KGPaperList.pk is the *Paper* object build for f0001; the second is build for f0002; and so on.
+ The building process please refer to the *FilePaser()* function in **cmyPreprocess.py**

### KGParseTreelist.pk
+ The Stanford-parser Tree list for the whole corpus, each element is the parser tree list for a paper.
+ The first element is the parser tree list for all sentences in f0001; the second is the list for f0002; and so on.
+ The storing process please see the *Build_w_pos_DIC()* function in  **cmyCountWF.py**.

### KGWPFdiclist.pk
+ Store the *WPF* objects list for the whole KG corpus，each element is a *WPF* object for a paper.
+ *WPF* class please refer to **cmyPackage.py**, WPF = Word tokens + POS tags + Frequency.
+ The building process please see the *Build_w_pos_DIC()* function in **cmyCountWF.py**.

### KGTotalWPFdic.pk
+ Build one *WPF* object for the whole KG corpus, to count the word frequency information on the whole corpus. 
+ The building process please see the *GetTotalWPFdic()* function in **cmyCountWF.py**.

### Patterns.pk
+ Store the causal *pattern* objects (*pattern* class in **cmyPackage.py**).
+ each pattern object corresponds to a manually written causal pattern in **./Corpus/causal_links.txt**

### mtRegExpList.pk
+ Store the regular expression lists build by main tokens in each pattern object to easily match sentences.
+ The building process please refer to *MainTokenRegExp()* in **cmyPatternMatching.py**

### KGCEList.pk
+ Store all the cause-effect links extracted from the KG corpus.
+ KGCEList.pk stores a list, which contains 39 elements. Each element corresponds to a paper.
+ The first element in KGCEList is the list of cause-effect links extracted from f0001; the second is the list extracted from f0002; and so on.
+ Each cause-effect is stored as a *CELink* object (please refer to the definition of CELink class in **cmyPackage.py**)

### KGFTextList.pk
+ Store the *FText* objects list for the whole corpus. (*FText* class please refer to **cmyPackage.py**)
+ Each element is a *FText* object constructed for storing the sentences in Abstract, Conclusion and CE links.
+ The building process please refer to the *GetWordDic()* function in **cmyWordsCompare.py**

### KGFWordDic.pk
+ Store the *FWordDic* objects list for the whole corpus. (*FWordDic* class please refer to **cmyPackage.py**)
+ Each element is a *FWordDic* object constructed for storing the words and their occurrence frequency in Abstract, Conculsion, and CE links.
+ The building process please refer to the *GetWordDic()* function in **cmyWordsCompare.py**

### KGFCoWord.pk
+ Store the *CoWords* objects list for the whole corpus (*CoWords* class please refer to **cmyPackage.pk**)
+ Each element is a *CoWords* objects constructed for storing the occurrence frequency of common words in Abstract, Conculsion, and CE links.
+ **The stopwords in StopW.pk has been removed**. The .txt version of stopwords please refer to **./Corpus./TXT/stopW.txt**
+ **Punction also has been removed**. The punctuations we removed are store in **Puncs.pk**, and all the punctuations please refer to *getStopWord()* function in **cmyToolkit.py**

### KGManCESeclst.pk
+ Store the distribution of cause-effect links on each sections in each paper.
+ Build a *ManCESec* object (see **cmyPackage.py**) for each paper, which stores the file label and the distribution list of cause-effect links on sections.
+ Each distribution object on sections is an instance of *CEonSec* class (see **cmyPackage.py**)

### KGPaperTextList_FurtherTest.pk
+ The *PaperTest* object list for the whole corpus. 
+ Each element is the *PaperTest* object constructed for drawing the **figure.xls** in ./XLS directory.

### KGCEPaperList.pk
+ Combine cause-effect links into each Paper object in KGPaperList.pk, to form the Paper1 object.
+ the definition of Paper1 class, please refer to cmyPackage.py
+ The combining process please refer to cmyAddCEid.py

## Other PK files in ./PK directory
+ Puncs.pk stores the punctuations we want to remove from the texts. All the punctuations please refer to *getStopWord()* function in **cmyToolkit.py**.
+ StopW.pk stores the stopwords we want to remove from the texts. All the stopwords please refer to ./Corpus/stopW.txt. The building process please refer to *getStopWord()* function in **cmyToolkit.py**.