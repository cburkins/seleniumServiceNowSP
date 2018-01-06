## Testing ServiceNow (Service Portal) with Selenium

Automated testing of searching a ServiceNow Service Portal.  Reads the results, verifies that the desired item is present.  Shows you how far down the list the result is.


### Environment

This was developed on a Windows 10 machine using chrome.  No testing was done on other platforms/browsers yet

### Installation (for usage on the much better CygWin terminal/shell)

- Install Cygwin (choosing python 2.7)
- In .bashrc, explictly set your path to remove all Windows paths (e.g. /usr/bin; /usr/local/bin; ~/bin)
- Set your PYTHONPATH to /usr/lib/2.7

So, your ~/.bashrc should have this at the bottom:

```
# Set path for calling command-line executables/scripts
export PATH=/usr/bin:/usr/local/bin:~/bin
# Search path for importing python modules
export PYTHONPATH=/usr/lib/python2.7
```


- In Cygwin, install pip via "easy_install-2.7 pip"
- In Cygwin, install selenium via "pip install selenium"


### Installation (for usage on the boring and awful Windows prompt)

NOTE: You won't get color output for pass/fail, and copying from the Windows prompt is a bit painful

- Install Windows Python

(finish these instructions later)


### Usage (calling the program)


Example of usage:

```

[NA+CBURKIN@WLPF0SGDR4 seleniumServiceNowSP (master)]$ python spTest.py -h
usage: spTest.py [-h] [-v] [-r] [-p PAUSESECS] [-w WEBSITEURL] [-s INPUTFILE]
                 [-priority PRIORITYMATCH]

Does search testing on Iris (ServiceNow) website

optional arguments:
  -h, --help            show this help message and exit
  -v                    verbose_mode
  -r                    print detailed search results (10-15 rows of output
                        per search
  -p PAUSESECS          amount to pause selenium tester
  -w WEBSITEURL         ServiceNow website to test against
  -s INPUTFILE          list of search terms to run (in CSV format with one
                        header row)
  -priority PRIORITYMATCH
                        only runs tests which match this regular expression
                        (e.g. "P1" or "P1|P2")

```

### Usage (format of the input file)

The format of the input file (CSV), and assumes that first line is column headers.  

- Column1: sys_id of the item you'd like to find
- Column2: Priority indicator (e.g. P1, P2, P3, but can really be anything)
- Column3: Friendly name of the catalog/KB item (used when item can't be found) 
- Column4: text for the search field (this is what you'll really be search with)
- Column5: Comment (completely ignored for now, just handy for notes in the input file)

Example of intput file

```
Sys ID,Priority,SID/OG,Search Term,Comment
3e94804b6f88ad041e02e3764b3ee4cf,P1,"new hire, moves and transfers, employee/partner conversions",new hire,Comment
cb41e2e56f8329001e02e3764b3ee4c1,P2,Suspend IT services for long-term leave,leave,Comment
c21f80036f4865c038ef17831c3ee4b1,P1,Modify email/account name/change field/VIP status,change email address,Comment
c21f80036f4865c038ef17831c3ee4b1,P1,Modify email/account name/change field/VIP status,change account name,Comment
2ac07a2d4f2a0f04f23b11ff0310c7f1,P1,How to Use Outlook Email,email,Comment
```

### Screenshots

![alt text](screenshots/example-output-cygwin.png "Screenshot of colored output using cygwin")

