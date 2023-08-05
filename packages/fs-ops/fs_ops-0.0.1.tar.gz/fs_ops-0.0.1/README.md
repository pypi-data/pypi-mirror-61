### fs_ops

Simple additional operations on file system.


```{python}
from fs_ops.csv import rows2csv

rows2csv({'a':10, 'b':20}.items())
```
'rows2csv' takes lists and puts them as rows to a csv

```{python}
from fs_ops.paths import find_suffixed_files

find_suffixed_files(paths=['/home/matteo/Projects/waters/data',
                           '/home/matteo/Projects/waters/data/T181207_07_stats.json'], 
                    file_patterns=['**/*_IA_workflow.xml'], 
                    extensions=['.xml','.json'])
```
'find_suffixed_files' recursively finds files with given suffixes within a set of paths.
If 'paths' point to files, then we filter those with given extensions.
If 'paths' point to folders, we recursively search inside each path for a given pattern.
Paths to files with extension in 'extensions' will not be filtered out.
Provided file paths are checked for existance.
