[![Build Status](https://travis-ci.org/adbailey4/python_utils.svg?branch=master)](https://travis-ci.org/adbailey4/python_utils)

# python_utils
General python functions and classes which could be used across multiple projects.

## Installation
* `pip install py3helpers`
**Note**: The default project does not install pysam, biopython and mappy because they are fairly large dependencies. However, if you want to use the seq_tools module you need to install via
 
* `pip install py3helpers[seq_tools]`
#### Install From Source  
```
git clone https://github.com/adbailey4/python_utils 
cd python_utils  
pip install -e.[seq_tools]
python setup.py test
```

## Releases 

### 0.3.1
* Added `merge_methyl_bed_files.py` and `methyl_bed_kmer_analysis.py` to bin. 
* May end up removing these files so I am not going to update pip version 0.3.2
 
### 0.3.6
* Added a few more helper functions and fixed the extras_require issue in `setup.py`

