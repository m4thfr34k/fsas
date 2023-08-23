## 👋 hello

**Yet another implementation of a filesystem file size and search cli app.** I simply wanted to know where all of my storage had gone. The default explorer search was painfully slow so I took this as an opportunity to learn and create.

## 🔥 quickstart

usage: FSAS [-h] [-b BASE] [-f FILE] {size,search} ...  
File size and search.

positional arguments:  
 {size,search}  
 **size** Returns list of files greater than a size set by the user.  
 **search** Returns list of files matching a pattern set by the user.

options:  
-m, --minimum -
Minimum file size to include in results. Default (250 MBs)  
-b, --base - Base directory where search will begin.  
-f, --file - Output file for saving results.

```sh
fsas --help
fsas size --help
fsas search --help
fsas -b "D:\" size -m 100
fsas -b "D:\" -f "results.csv" size -m 100
```
