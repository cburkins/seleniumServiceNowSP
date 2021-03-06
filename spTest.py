
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.chrome.options import Options
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
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
def truncateAddEllipse(inputString, desiredLength):
	if (len(inputString) > (desiredLength-3)):
		return inputString[:desiredLength-3] + "..."
	else:
		return inputString
# ------------------------------------------------------------------------------
def getResultType(element):
	if ('id=iris_cat_item' in element.get_attribute('href')):
		return "Catalog"
	elif ('kb_article' in element.get_attribute('href')):
		return getColorString("Article",CYAN);
	else:
		return "Unknown Type"
# ------------------------------------------------------------------------------

def searchInIrisServicePortal(browser, currentCount, totalCount, websiteURL, search_string, sys_id, itemTitle, testPriority, priorityMatch):

	# Type in the search string
	#sys.stdout.write("(%03d/%03d) Searching %-37s" % (currentCount, totalCount, "'" + search_string + "' :"))
	sys.stdout.write("(%03d/%03d) %-40s  Search:%-37s %s " % (currentCount, totalCount, truncateAddEllipse(itemTitle,40), "'" + search_string + "'", testPriority))
	sys.stdout.flush();


	# Helps to skip any line items in the input file which have an empty search_string
	if not search_string:
		testPriority = "Er"	

	if (re.match(priorityMatch, testPriority) and (testPriority != "Er")):

		# Load the desired website
		browser.get(websiteURL);
		browser.implicitly_wait(30) # seconds

		# Wait for the search box to show up
		elem = browser.find_element_by_xpath("//*[@id='homepage-search']/div/div[1]/div[2]/form/div/input");


		# Type desired search into the search field
		elem.clear()
		elem.send_keys(search_string);
		time.sleep(pauseDuration);
		elem.send_keys(Keys.RETURN);


		# Assert the New Hire catalog item is within the search results
		#desiredLink = browser.find_element_by_xpath("//a[contains(@href,'?id=iris_cat_item&sys_id=3e94804b6f88ad041e02e3764b3ee4cf')]");

		# Explicity Wait for search results to show up on screen
		wait = WebDriverWait(browser, 20)
		xPathDesired="//h4[contains(text(),'Search results for:')]"
		#wait.until(EC.visibility_of_element_located((By.XPATH, xPathDesired)))
		wait.until(EC.presence_of_element_located((By.XPATH, xPathDesired)))
		time.sleep(pauseDuration);

		# Explicitly wait until we find the specific search result we want
		# Construct correct XPath to find the desired catalog item on the page
		xPathDesired = "//a[contains(@href,'%s')]" % (sys_id)
		cssDesired = "a[href*='%s']" % (sys_id)

		# Make sure that implicit wait is zero, else it seems to override the explict wait
		browser.implicitly_wait(0) # seconds
		# Set explicity wait for 2 seconds
		wait = WebDriverWait(browser, 2)
		try:
			#wait.until(EC.visibility_of_element_located((By.XPATH, xPathDesired)))
			wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cssDesired)))
		except Exception as e: 
			print ("%s                (UserTxt: %s)" % (getColorString("FAIL", RED), truncateAddEllipse(itemTitle,30)));
			#print (e.__doc__);
			#print (e.message);
		else:
			desiredLink = browser.find_element_by_xpath(xPathDesired);
			[position, numResults] = positionInAllResults(browser, sys_id);
			resultType = getResultType(desiredLink);
			urlTitle = truncateAddEllipse(printable(desiredLink.text),30)
			print("%s [pos %2d of %2d] (%s: %s)" % (getColorString("Pass", GREEN), position, numResults, resultType, urlTitle));
		vprint ("   xPath = %s\n" % (xPathDesired))

	else:
		print("Skip");

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

			# Joe's contribution for handling ASPAC character sets in the input file
			# UTF-8 is backwards compatible with ASCII
			row = [x.decode('utf-8') for x in row]

			vprint("Reading line: %s" % (row))
			# File is currently sys_id, title, search_term
			# Create a row where order search_term, sys_sid, title
			# search_term
			searchTerm = []
			# search_term is 4th column
			searchTerm.append(row[3]);
			# sys_id is 1st column
			searchTerm.append(row[0]);
			# title is 3rd column
			searchTerm.append(row[2]);
			# priority is 2nd column
			searchTerm.append(row[1]);

			if (len(searchTerm[1]) == 32):
				searchList.append(searchTerm);
			else:
				searchTerm[3] = "Er"
				searchList.append(searchTerm);
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
	# If the nargs keyword argument is not provided, the number of arguments consumed is determined by the action.
	#    store_true: 
	# epilog= argument will be display last in help usage (strips out newlines)
	parser = argparse.ArgumentParser(description='Does search testing on Iris (ServiceNow) website')
	 
	# Configure command-line flag for verbose output
	parser.add_argument('-v', dest='verbose', action='store_true', help='verbose_mode')
	# Configure command-line flag for results output
	parser.add_argument('-r', dest='results', action='store_true', help='print detailed search results (10-15 rows of output per search')
	# Configure command-line flag selecting a pause duration
	parser.add_argument('-p', type=int, dest="pauseSecs", help='amount to pause selenium tester', default=1)
	# Configure command-line flag selecting a website
	parser.add_argument('-w', type=str, dest="websiteURL", action="store", default="http://jnjtrain.service-now.com/iris_gl", help='ServiceNow website to test against')


	# Configure command-line flag selecting a browser
	parser.add_argument('-b', type=str, dest="desiredBrowser", action="store", default="chrome", help='browser (chrome|firefox|edge|IE11)')


	# Configure command-line flag selecting a configuration file (for search terms)
	parser.add_argument('-s', type=str, dest="inputFile", default="SearchMonitoringCriteria2.csv", help='list of search terms to run (in CSV format with one header row)')
	# Configure command-line flag providing a priority match string (e.g. P1)
	parser.add_argument('-priority', type=str, dest="priorityMatch", help='only runs tests which match this regular expression (e.g. "P1" or "P1|P2")', default=".*")

	# Get the object returned by parse_args
	args = parser.parse_args()
	verbose = args.verbose;
	pauseDuration = args.pauseSecs;
	websiteURL = args.websiteURL;
	searchConfigFile = args.inputFile;
	printSearchResults = args.results;
	priorityMatch = args.priorityMatch;
	desiredBrowser = args.desiredBrowser;
	# websiteURL="http://jnjsandbox5.service-now.com/iris_gl"
	# websiteURL="http://jnjtrain.service-now.com/iris_gl"
	 
	# Prints command-line params
	vprint("\nGiven arguments: %s\n\n" % (sys.argv[1:]))
	vprint("Interpreted arguments: (via argparse object)\n")
	for cmdlineOption in (vars(args)):
		vprint ("   %s: %s\n" % (cmdlineOption, vars(args)[cmdlineOption]))
	vprint("\n\n");

	return [verbose, desiredBrowser, printSearchResults, pauseDuration, websiteURL, searchConfigFile, priorityMatch];

# ------------------------------------------------------------------------------

def printParams():
	print("\n");
	print("%20s: %s" % ("Website URL", websiteURL));
	print("%20s: %s" % ("browser", desiredBrowser))
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

def openBrowserChrome():
	chrome_options = Options()

	# I think  you can also use browser.maximize_window(), perhaps browser agnostic ?
	#chrome_options.add_argument("start-maximized")

	#chrome_options.add_argument("headless")
	# Option to supress errors such as "[8916:7132:1219/182838.145:ERROR:process_metrics.cc(105)] NOT IMPLEMENTED"
	chrome_options.add_argument("--log-level=3")
	print ("\n *** Opening Chrome browser ***\n")
	browser = webdriver.Chrome(chrome_options=chrome_options)
	return browser;

# ------------------------------------------------------------------------------

def openBrowserEdge():

	print ("\n *** Opening Edge browser ***\n")
	browser = webdriver.Edge()
	return browser;


# ------------------------------------------------------------------------------

def openBrowserIE11():

	print ("\n *** Opening IE11 browser ***\n")

	# This requires IEDriverServer.exe to be in your OS execution path
	# This can be downloaded from https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver
	# Docs suggest using 32-bit version of IEDriverServer.exe even if your IE11 is 64-bit
	# 64-bit version seems to input characters to browser VERY slowly
	browser = webdriver.Ie()
	return browser;

# ------------------------------------------------------------------------------

def openBrowserFirefox():

	print ("\n *** Opening Firefox browser ***\n")
	browser = webdriver.Firefox()
	return browser;


# ------------------------------------------------------------------------------

def closeBroswer(browser):
	print "\n\nAll finished, closing the browser now..."
	browser.close();

# ------------------------------------------------------------------------------

def printWarning():
	print ("#########################################################################")
	print ("#########################################################################")
	print ("You are 100% responsible for all the actions taken in this script")
	print ("If you're about to run this in PRODUCTION and you have ADMIN privs,")
	print ("please MAKE SURE you understand this code, and the actions it takes")
	print ("You're about to make hundreds or thousands of clicks in the browser,")
	print ("And it will happen so fast you'll barely be able to see it")
	print ("Please be VERY CAREFUL before clicking go")
	print ("#########################################################################")
	print ("#########################################################################")
# ------------------------------------------------------------------------------
# --------------------------- Main ---------------------------------------------
# ------------------------------------------------------------------------------

# Get the command-line args that were passed in (as well as defaults for no args)
verbose = False;
[verbose, desiredBrowser, printSearchResults, pauseDuration, websiteURL, searchConfigFile, priorityMatch] = getCommandLineArgs();

# Get the search terms
#searchListDefault = readDefaultSearchList();
searchList = readSearchConfig(searchConfigFile);

# Show the user all the parameters
printParams();

printWarning();

# If the user doesn't answer 'y', program will exit
getConfirmation("\nReady to go ? ");

# Open the browser
if (desiredBrowser == "chrome"):
	browser = openBrowserChrome();
elif (desiredBrowser == "edge"):
	browser = openBrowserEdge();
elif (desiredBrowser == "IE11"):
	browser = openBrowserIE11();
elif (desiredBrowser == "firefox"):
	browser = openBrowserFirefox();
else:
	print ("\n\n   Error: Browser name %s is not valid\n\n\n" % desiredBrowser);
	sys.exit();

# Loop through all the desired tests, and call the test function
print ("\n\n *** Searching now (%s) ***\n\n" % (websiteURL))
for (count,row) in enumerate(searchList):
	searchInIrisServicePortal(browser, count+1, len(searchList), websiteURL, row[0], row[1], row[2], row[3], priorityMatch);

closeBroswer(browser);

# ------------------------------------------------------------------------------
# ------------------------------ End -------------------------------------------
# ------------------------------------------------------------------------------
