
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.chrome.options import Options
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Leveraged this:   http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html
# ------------------------------------------------------------------------------
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
# ------------------------------------------------------------------------------

#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)
# ------------------------------------------------------------------------------
def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)
# ------------------------------------------------------------------------------
def getColorString(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                return(seq)
        else:
                return(text)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def vprint(print_me):

    if verbose:
        #print "%s" % print_me
        sys.stdout.write("%s" % print_me)
        sys.stdout.flush();

# ------------------------------------------------------------------------------
def printable(theString):
	return(filter(lambda x: x in string.printable, theString));

# ------------------------------------------------------------------------------

def lookForText(): 
	# Assert the "New Hire" text is within the search results
	import string
	myResults = driver.find_element_by_xpath("//*[@id='xb218bc42db4e4bc4117c5d30cf96194a']/div");
	theText = myResults.text;
	theText = filter(lambda x: x in string.printable, theText)
	assert "New Hire" in theText;


# ------------------------------------------------------------------------------

def printListXPath(xpathExpression, browser):

	xPathDesired = xpathExpression;
	try: 
		desiredList = browser.find_elements_by_xpath(xPathDesired);
	except:
		print "Failed to find list"
	else:
		for count,element in enumerate(desiredList):
			print("   (%2d) %s" % (count+1, printable(element.text)));
			# vprint("        INNER: %s\n" % (printable(element.get_attribute('innerHTML'))))
			# vprint("        OUTER: %s\n" % (printable(element.get_attribute('outerHTML'))))
			vprint("        HREF:  %s\n" % (printable(element.get_attribute('href'))))

# Create three new (simpler) functions.  1st argument is a complex XPath expression
# These three new functions take 1 argument rather than 2, and have that 1st argument (XPath) hard-coded
printCatalogResults = lambda browser: printListXPath("//a[contains(@href, '?id=iris_cat_item')]", browser)
printKnowledgeResults = lambda browser: printListXPath("//a[contains(@href, 'kb_article')]", browser)
printAllResults = lambda browser: printListXPath("//a[contains(@href, 'kb_article') or contains(@href, 'id=iris_cat_item')]", browser)

# ------------------------------------------------------------------------------
def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1
# ------------------------------------------------------------------------------

def findInElementList(xpathExpression, browser, sys_id):

	# XPath to find all catalog items in the search results
	# xPathDesired = "//a[contains(@href, '?id=iris_cat_item')]"
	# Xpath to find all knowledge articles in the search results
	# xPathDesired = "//a[contains(@href, 'kb_article')]"
	# XPath to find all the search result links (both articles and catalog items)
	xPathDesired = "//a[contains(@href, 'kb_article') or contains(@href, 'id=iris_cat_item')]"
	xPathDesired = xpathExpression

	try: 
		desiredList = WebDriverWait(browser, 2).until(lambda browser:browser.find_elements_by_xpath(xPathDesired))
	except:
		print "Failed to find list"
	else:
		listSys_Id = [];
		for count,element in enumerate(desiredList):
			vprint("   (%2d) %s\n" % (count+1, printable(element.text)));
			# vprint("        INNER: %s\n" % (printable(element.get_attribute('innerHTML'))))
			# vprint("        OUTER: %s\n" % (printable(element.get_attribute('outerHTML'))))
			vprint("        HREF:  %s\n" % (printable(element.get_attribute('href'))))
			listSys_Id.append(printable(element.get_attribute('href')))
		position = index_containing_substring(listSys_Id, sys_id)+1	
		vprint("   Position:%d" % (position))
		return [position, len(desiredList)]

# Create three new (simpler) functions.  1st argument is a complex XPath expression
# These three new functions take 2 arguments rather than 3, and have that 1st argument (XPath) hard-coded
positionInCatalogResults = lambda browser,catalogSysId: findInElementList("//a[contains(@href, '?id=iris_cat_item')]", browser, catalogSysId)
positionInKnowledgeResults = lambda browser,catalogSysId: findInElementList("//a[contains(@href, 'kb_article')]", browser, catalogSysId)
positionInAllResults = lambda browser,catalogSysId: findInElementList("//a[contains(@href, 'kb_article') or contains(@href, 'id=iris_cat_item')]", browser, catalogSysId)

# ------------------------------------------------------------------------------

def searchInIrisServicePortal(browser, currentCount, totalCount, websiteURL, search_string, catalogSysId, itemTitle):

	# Load the desired website
	browser.get(websiteURL);
	browser.implicitly_wait(10) # seconds


	# Wait for the search box to show up
	elem = browser.find_element_by_xpath("//*[@id='homepage-search']/div/div[1]/div[2]/form/div/input");

	# Type in the search string
	sys.stdout.write("(%03d/%03d) Searching %-37s" % (currentCount, totalCount, "'" + search_string + "' :"))
	sys.stdout.flush();
	elem.clear()
	elem.send_keys(search_string);
	time.sleep(pauseDuration);
	elem.send_keys(Keys.RETURN);

	#lookForText();

	# Assert the New Hire catalog item is within the search results
	#desiredLink = browser.find_element_by_xpath("//a[contains(@href,'?id=iris_cat_item&sys_id=3e94804b6f88ad041e02e3764b3ee4cf')]");

	# Explicity Wait for search results to show up on screen
	wait = WebDriverWait(browser, 20)
	xPathDesired="//h4[contains(text(),'Search results for:')]"
	wait.until(EC.visibility_of_element_located((By.XPATH, xPathDesired)))
	time.sleep(pauseDuration);

	# Explicitly wait until we find the specific search result we want
	# Construct correct XPath to find the desired catalog item on the page
	catURL = '?id=iris_cat_item&sys_id=%s' % (catalogSysId)
	xPathDesired = "//a[contains(@href,'%s')]" % (catURL)
	# Make sure that implicit wait is zero, else it seems to override the explict wait
	browser.implicitly_wait(0) # seconds
	# Set explicity wait for 2 seconds
	wait = WebDriverWait(browser, 2)
	try:
		wait.until(EC.visibility_of_element_located((By.XPATH, xPathDesired)))
	except:
		print ("%s                     (%s)" % (getColorString("FAILED", RED), itemTitle));
	else:
		desiredLink = browser.find_element_by_xpath(xPathDesired);
		[position, numResults] = positionInAllResults(browser, catalogSysId);
		print("%s  [position %2d of %2d] (Catalog Item: %s)" % (getColorString("Found", GREEN), position, numResults, printable(desiredLink.text)));
	vprint ("   Catalog URL = %s\n" % (catURL))
	vprint ("   xPath = %s\n" % (xPathDesired))

	if printSearchResults:
		printAllResults(browser);


# ------------------------------------------------------------------------------

def readSearchConfig(configFileName):

	# Read config file
	import csv
	searchList = [];
	with open(configFileName, 'rb') as csvfile:
		searchConfigFile = csv.reader(csvfile, delimiter=',', quotechar='"')
		# Skip the first line
		next(searchConfigFile, None);
		# Loop through all the remaining rows
		for row in searchConfigFile:
			# File is currently sys_id, title, search_term
			# Create a row where order search_term, sys_sid, title
			# search_term
			searchTerm = []
			searchTerm.append(row[2]);
			# sys_id
			searchTerm.append(row[0]);
			# title
			searchTerm.append(row[1]);

			if (len(searchTerm[1]) == 32):
				searchList.append(searchTerm);
			else:
				print("Skipping (no catalog sys_id given): %s" % (searchTerm[2]));

	return searchList


# ------------------------------------------------------------------------------

# this can be used for testing, in case you don't have an input file

def readDefaultSearchList():

	# Define the list of searches (1st position is search team, 2nd position is desired catalog item)
	searchListDefault = [
		# Chad's test
		["new hire", "3e94804b6f88ad041e02e3764b3ee4cf", "Placeholder title"],
		["email", "abea375f75a20d0029e60de16298b1bb", "Placeholder title"],

		# # New Hire catalog item
		["new hire", "3e94804b6f88ad041e02e3764b3ee4cf", "Placeholder title"],
		["onboard", "3e94804b6f88ad041e02e3764b3ee4cf", "Placeholder title"],
		["onboarding", "3e94804b6f88ad041e02e3764b3ee4cf", "Placeholder title"],
		["new account", "3e94804b6f88ad041e02e3764b3ee4cf", "Placeholder title"],
		["laptop", "3e94804b6f88ad041e02e3764b3ee4cf", "Placeholder title"],
		["account", "3e94804b6f88ad041e02e3764b3ee4cf", "Placeholder title"],
		# Access to Terminated or Departed associate's data
		["access data", "f7e870d61c9ee008cfc05fda97b0699e", "Placeholder title"],
		["terminated", "f7e870d61c9ee008cfc05fda97b0699e", "Placeholder title"],

		# Reset Password for a business application (currently missing)
		["reset password", "6efb03b96f33118038ef17831c3ee468", "Catalog Item: Reset Password for a business application"],
		["password", "6efb03b96f33118038ef17831c3ee468", "Catalog Item: Reset Password for a business application"],
		["password reset", "6efb03b96f33118038ef17831c3ee468", "Catalog Item: Reset Password for a business application"]
	]
	return searchListDefault

# ------------------------------------------------------------------------------

def getCommandLineArgs():

	verbose = False

	import getpass
	import argparse
	 
	# Parse command-line arguments (Create ArgumentParser object)
	# By default, program name (shown in 'help' function) will be the same as the name of this file
	# Program name either comes from sys.argv[0] (invocation of this program) or from prog= argument to ArgumentParser
	# epilog= argument will be display last in help usage (strips out newlines)
	parser = argparse.ArgumentParser(description='Does search testing on Iris (ServiceNow) website')
	 
	# Configure command-line flag for verbose output
	parser.add_argument('-v', dest='verbose', action='store_true', help='verbose_mode')
	# Configure command-line flag for results output
	parser.add_argument('-r', dest='results', action='store_true', help='print search results')
	# Configure command-line flag for a silly message, just so I remember how to do it 
	parser.add_argument('--message',  default="Well, Hi there, Chad !")
	# Configure command-line flag selecting a pause duration
	parser.add_argument('-p', type=int, help='amount to pause selenium tester', default=1)
	# Configure command-line flag selecting a website
	parser.add_argument('-w', default="http://jnjtrain.service-now.com/iris_gl", help='ServiceNow website to test against')
	# Configure command-line flag selecting a configuration file (for search terms)
	parser.add_argument('-s', default="SearchMonitoringCriteria2.csv", help='list of search terms to run (in CSV format with one header row)')

	# Get the object returned by parse_args
	args = parser.parse_args()
	verbose = args.verbose;
	pauseDuration = args.p;
	websiteURL = args.w;
	searchConfigFile = args.s;
	printSearchResults = args.results;
	# websiteURL="http://jnjsandbox5.service-now.com/iris_gl"
	# websiteURL="http://jnjtrain.service-now.com/iris_gl"
	 
	# Prints command-line params
	vprint("\nGiven arguments: %s\n\n" % (sys.argv[1:]))
	vprint("Interpreted arguments: (via argparse object)\n")
	for cmdlineOption in (vars(args)):
		vprint ("   %s: %s\n" % (cmdlineOption, vars(args)[cmdlineOption]))
	vprint("\n\n");

	return [verbose, printSearchResults, pauseDuration, websiteURL, searchConfigFile];

# ------------------------------------------------------------------------------

def printParams():
	print("\n");
	print("%20s: %s" % ("Website URL", websiteURL));
	print("%20s: %s" % ("configFile", searchConfigFile))
	print("%20s: %s" % ("Pause Duration", pauseDuration))
	print("%20s: %d" % ("Number of tests", len(searchList)))
	print("%20s: %s" % ("Print Search Results", printSearchResults))
	print("%20s: %s" % ("Verbose", verbose))
	print("\n\n");


# ------------------------------------------------------------------------------
def getConfirmation(theQuestion):
	response = raw_input(theQuestion)
	if (response != 'y'):
		print ("\n*** Exiting ***\n\n");
		sys.exit();

# ------------------------------------------------------------------------------

def openBrowser():
	chrome_options = Options()

	# I think  you can also use browser.maximize_window(), perhaps browser agnostic ?
	#chrome_options.add_argument("start-maximized")

	#chrome_options.add_argument("headless")
	# Option to supress errors such as "[8916:7132:1219/182838.145:ERROR:process_metrics.cc(105)] NOT IMPLEMENTED"
	chrome_options.add_argument("--log-level=3")
	print ("\n *** Opening browser ***\n")
	browser = webdriver.Chrome(chrome_options=chrome_options)
	return browser;


# ------------------------------------------------------------------------------

def closeBroswer(browser):
	print "\n\nAll finished, closing the browser now..."
	browser.close();

# ------------------------------------------------------------------------------
# --------------------------- Main ---------------------------------------------
# ------------------------------------------------------------------------------

# Get the command-line args that were passed in (as well as defaults for no args)
verbose = False;
[verbose, printSearchResults, pauseDuration, websiteURL, searchConfigFile] = getCommandLineArgs();

# Get the search terms
#searchListDefault = readDefaultSearchList();
searchList = readSearchConfig(searchConfigFile);

# Show the user all the parameters
printParams();

# If the user doesn't answer 'y', program will exit
getConfirmation("\nReady to go ? ");

# Open the browser
browser = openBrowser();

# Loop through all the desired tests, and call the test function
print ("\n\n *** Searching now (%s) ***\n\n" % (websiteURL))
for (count,row) in enumerate(searchList):
	# print ("term=%-20s sys_id=%-40s title=%s" % (row[0], row[1], row[2]))
	searchInIrisServicePortal(browser, count+1, len(searchList), websiteURL, row[0], row[1], row[2]);

closeBroswer(browser);

# ------------------------------------------------------------------------------
# ------------------------------ End -------------------------------------------
# ------------------------------------------------------------------------------
