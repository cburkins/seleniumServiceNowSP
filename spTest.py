
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

def vprint(print_me):

    if verbose:
        #print "%s" % print_me
        sys.stdout.write("%s" % print_me)

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

def findAllCatalogItems():

	# Purely additional info, search for all catalog items
	try: 
		xPathDesired = "//a[contains(@href, '?id=iris_cat_item')]"
		desiredList = driver.find_elements_by_xpath(xPathDesired);
	except:
		print "Failed to find list"
	else:
		count = 1;
		for count,element in enumerate(desiredList):
			print("   (%2d) %s" % (count+1, printable(element.text)));
			# vprint("        INNER: %s\n" % (printable(element.get_attribute('innerHTML'))))
			# vprint("        OUTER: %s\n" % (printable(element.get_attribute('outerHTML'))))
			vprint("        HREF:  %s\n" % (printable(element.get_attribute('href'))))

# ------------------------------------------------------------------------------

def searchInIrisServicePortal(websiteURL, search_string, catalogSysId, itemTitle):

	# Load the desired website
	driver.get(websiteURL);
	driver.implicitly_wait(10) # seconds


	# Wait for the search box to show up
	elem = driver.find_element_by_xpath("//*[@id='homepage-search']/div/div[1]/div[2]/form/div/input");

	# Type in the search string
	sys.stdout.write("Searching %-37s" % ("'" + search_string + "' :"))
	elem.clear()
	elem.send_keys(search_string);
	time.sleep(pauseDuration);
	elem.send_keys(Keys.RETURN);

	#lookForText();

	# Assert the New Hire catalog item is within the search results
	#desiredLink = driver.find_element_by_xpath("//a[contains(@href,'?id=iris_cat_item&sys_id=3e94804b6f88ad041e02e3764b3ee4cf')]");

	# Wait for search results
	wait = WebDriverWait(driver, 20)
	xPathDesired="//h4[contains(text(),'Search results for:')]"
	wait.until(EC.visibility_of_element_located((By.XPATH, xPathDesired)))
	time.sleep(pauseDuration);

	# Construct correct XPath to find the desired catalog item on the page
	catURL = '?id=iris_cat_item&sys_id=%s' % (catalogSysId)
	xPathDesired = "//a[contains(@href,'%s')]" % (catURL)

	# Attempting explict wait
	driver.implicitly_wait(0) # seconds
	wait = WebDriverWait(driver, 2)
	try:
		wait.until(EC.visibility_of_element_located((By.XPATH, xPathDesired)))
	except:
		print ("Failed (%s)" % (itemTitle));
	else:
		desiredLink = driver.find_element_by_xpath(xPathDesired);
		print("Found  (Catalog Item: %s)" % (printable(desiredLink.text)));
	vprint ("   Catalog URL = %s\n" % (catURL))
	vprint ("   xPath = %s\n" % (xPathDesired))

	# findAllCatalogItems();

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

# --------------------------- Main ---------------------------------------------
# ------------------------------------------------------------------------------


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
# websiteURL="http://jnjsandbox5.service-now.com/iris_gl"
# websiteURL="http://jnjtrain.service-now.com/iris_gl"
 
# Prints command-line params
vprint("\nGiven arguments: %s\n\n" % (sys.argv[1:]))
vprint("Interpreted arguments: (via argparse object)\n")
for cmdlineOption in (vars(args)):
	vprint ("   %s: %s\n" % (cmdlineOption, vars(args)[cmdlineOption]))
vprint("\n\n");

# Get the search terms
#searchListDefault = readDefaultSearchList();
searchList = readSearchConfig(searchConfigFile);

# Show the user all the parameters
print("\n");
print("%20s: %s" % ("Website URL", websiteURL));
print("%20s: %s" % ("configFile", searchConfigFile))
print("%20s: %s" % ("Pause Duration", pauseDuration))
print("%20s: %d" % ("Number of tests", len(searchList)))

print("\n\n");

# Verify that the user is ready ('y' is the only answer that will proceed)
response = raw_input("\nReady to go ? ")
if (response != 'y'):
	print ("\n*** Exiting ***\n\n");
	sys.exit();

# Open the browser
chrome_options = Options()
#chrome_options.add_argument("start-maximized")
#chrome_options.add_argument("headless")
# Option to supress errors such as "[8916:7132:1219/182838.145:ERROR:process_metrics.cc(105)] NOT IMPLEMENTED"
chrome_options.add_argument("--log-level=3")
print ("\n *** Opening browser ***\n")
driver = webdriver.Chrome(chrome_options=chrome_options)


# Pre-load a website to get past initial start-up erros
driver.get(websiteURL);

print ("\n\n *** Searching now (%s) ***\n\n" % (websiteURL))
#websiteURL="http://jnjprod.service-now.com/iris_gl"

# # Loop through all desired searches, and search for each
# for searchConfig in searchList:
# 	searchInIrisServicePortal(websiteURL, searchConfig[0], searchConfig[1], searchConfig[2]);


for row in searchList:
	# print ("term=%-20s sys_id=%-40s title=%s" % (row[0], row[1], row[2]))
	searchInIrisServicePortal(websiteURL, row[0], row[1], row[2]);
	


print "\n\nAll finished, closing the browser now..."
driver.close();


# ------------------------------------------------------------------------------
# ------------------------------ End -------------------------------------------
# ------------------------------------------------------------------------------


