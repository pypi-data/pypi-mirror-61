### Parse Waters files

# Installation:

Simple:
```{bash}
pip install git+https://github.com/MatteoLacki/waters
```

Devel:
```{bash}
git clone https://github.com/MatteoLacki/waters
cd waters
pip install -e .
```

On Windows, add PYTHONPATH to PATH to run scripts.
It makes sense to add '.py' to PATHEXT system variable (to run scripts without specifying the interpreter).

After first installation, run
```{batch}
create_waters_shortcuts.py
```
as this will create executables for SendTo explorer tool.


# Usage
From terminal, you can call this to translate things to csvs.

```{batch}
usage: iadbs2csv.py [-h] paths [paths ...]

Get information on iaDBs.

positional arguments:
  paths       Paths to outputs of the iaDBs. If
              directly. If supplied folders, th
              files ending with '_IA_workflow.x

optional arguments:
  -h, --help  show this help message and exit
```


From terminal, you can call this to get stats on IA_workflow.
```{batch}
usage: iadbs2stats.py [-h] iadbsxml [iadbsxml ...]

Get information on iaDBs.

positional arguments:
  iadbsxml    Paths to outputs of the iaDBs. If ending with '.xml',
              directly. If supplied folders, these will be searched
              files ending with '_IA_workflow.xml'.

optional arguments:
  -h, --help  show this help message and exit
```