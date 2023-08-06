![Python package](https://github.com/usajusaj/camembertpy/workflows/Python%20package/badge.svg)
![Python package build and publish](https://github.com/usajusaj/camembertpy/workflows/Python%20package%20build%20and%20publish/badge.svg)
# camembertpy

Cython wrapper for https://github.com/jts/bri with pysam integration.

# Installation
## From pip repository
```bash
pip install camembert-bri
```
## From source
### conda approach (recommended)
```bash
conda env create -f environment.yml
conda activate camembert
python setup.py install
```
### pip approach
```bash
# optional virtualenv:
virtualenv camembert
source camembert/bin/activate

# Installation
pip install -r requirements.txt
python setup.py install
```

# Examples
## API
### build read index
```python
from camembert import Bri
b = Bri(bam_file)
b.create()
```

### retrieve reads
```python
from camembert import Bri
b = Bri(bam_file)
b.load()
for read in b.get(read_name):
    print(read.to_string())  # read is of type pysam.AligmentSegment
```
## CLI
A command line interface is included and mimics the original bri CLI command. For usage, refer to
```bash
camembert --help
camembert <subcommand> --help
```

### build read index
```bash
camembert index bam_file.bam
```

### retrieve reads
```bash
camembert get bam_file.bam read_name
```
