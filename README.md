## Testing ServiceNow (Service Portal) with Selenium

Automated testing of searching a ServiceNow Service Portal.  Reads the results, verifies that the desired item is present.  Shows you how far down the list the result is.


Example of usage:

```

$ python spTest.py -h
usage: spTest.py [-h] [-v] [-r] [--message MESSAGE] [-p P] [-w W] [-s S]

Does search testing on Iris (ServiceNow) website

optional arguments:
  -h, --help         show this help message and exit
  -v                 verbose_mode
  -r                 print search results
  --message MESSAGE
  -p P               amount to pause selenium tester
  -w W               ServiceNow website to test against
  -s S               list of search terms to run (in CSV format with one
                     header row)
```