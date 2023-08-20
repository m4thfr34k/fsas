## 👋 hello

**Yet another implementation of a filesystem file size and search cli app.** I simply wanted to know where all of my storage had gone. The default explorer search was painfully slow so I took this as an opportunity to learn and create.

## 🔥 quickstart

usage: FSAS [-h] [-m MINIMUM] [-b BASE] [-f FILE]

File size and search.

options:  
-m, --minimum -
Minimum file size to include in results. Default (250 MBs)  
-b, --base - Base directory where search will begin.  
-f, --file - Output file for saving results.

```sh
fsas --help
fsas -m 300 -f file_results.csv
```
