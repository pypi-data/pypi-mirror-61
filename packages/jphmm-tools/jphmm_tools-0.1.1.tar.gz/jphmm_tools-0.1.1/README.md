# jpHMM tools

__jphmm_tools__ provides methods for extracting information 
from [jpHMM](http://jphmm.gobics.de) [[Schulz *et al.* NAR 2012]](https://academic.oup.com/nar/article/40/W1/W193/1073895) output.

It implements tool for
* converting [Los Alamos](https://www.hiv.lanl.gov/content/sequence/HIV/mainpage.html) alignment file
into a reference file suitable for jpHMM:
```bash
jphmm_ref -h
```
* aligning sequences based on the jpHMM output:
```bash
jphmm_align -h
```
* extracting sequence subtype information from the jpHMM output:
```bash
jphmm_subtype -h
```
