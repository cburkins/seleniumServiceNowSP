from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.chrome.options import Options
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




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

def searchInIrisServicePortal(websiteURL, search_string, catalogSysId):

	# Load the desired website
	driver.get(websiteURL);
	driver.implicitly_wait(10) # seconds

	# Find the search box and type in the search string
	elem = driver.find_element_by_xpath("//*[@id='homepage-search']/div/div[1]/div[2]/form/div/input");
	sys.stdout.write("Searching %-20s" % ("'" + search_string + "' :"))
	elem.clear()
	elem.send_keys(search_string);
	elem.send_keys(Keys.RETURN);

	#lookForText();

	# Assert the New Hire catalog item is within the search results
	#desiredLink = driver.find_element_by_xpath("//a[contains(@href,'?id=iris_cat_item&sys_id=3e94804b6f88ad041e02e3764b3ee4cf')]");


	# Test for the desired catalog item, locating by xpath using ServiceNow sys_id within anchor tag
	catURL = '?id=iris_cat_item&sys_id=%s' % (catalogSysId)
	xPathDesired = "//a[contains(@href,'%s')]" % (catURL)
	try: 
		desiredLink = driver.find_element_by_xpath(xPathDesired);
		print("Found (Catalog Item: %s)" % (desiredLink.text));
	except:
		print "Failed"
	vprint ("   Catalog URL = %s\n" % (catURL))
	vprint ("   xPath = %s\n" % (xPathDesired))

	# Attempting explict wait
	driver.implicitly_wait(0) # seconds
	print "   Looking again"
	wait = WebDriverWait(driver, 2)
	try:
		wait.until(EC.visibility_of_element_located((By.XPATH, xPathDesired)))
	except:
		print ("      Failed again");
	else:
		print ("      Found again");
	# findAllCatalogItems();

# ------------------------------------------------------------------------------
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
 
# Test for verbose flag
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose_mode')
# Query for string 
parser.add_argument('--message',  default="Well, Hi there, Chad !")

# Get the object returned by parse_args
args = parser.parse_args()
verbose = args.verbose;
 
# Prints command-line params
vprint("\nGiven arguments: %s\n\n" % (sys.argv[1:]))
vprint("Interpreted arguments: (via argparse object)\n")
for cmdlineOption in (vars(args)):
	vprint ("   %s: %s\n" % (cmdlineOption, vars(args)[cmdlineOption]))
vprint("\n\n");


# Open the browser
chrome_options = Options()
#chrome_options.add_argument("start-maximized")
#chrome_options.add_argument("headless")
print ("\n *** Opening browser ***\n")
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver = webdriver.Chrome()

# Pre-load a website to get past initial start-up erros
driver.get("http://jnjsandbox5.service-now.com/iris_gl");



websiteURL="http://jnjsandbox5.service-now.com/iris_gl"
print ("\n\n *** Searching now (%s) ***\n\n" % (websiteURL))
#websiteURL="http://jnjprod.service-now.com/iris_gl"

# Define the list of searches (1st position is search team, 2nd position is desired catalog item)
searchList = [
	# Chad's test
	["new hire", "3e94804b6f88ad041e02e3764b3ee4cf"],
	["email", "abea375f75a20d0029e60de16298b1bb"],
	# # New Hire catalog item
	# ["new hire", "3e94804b6f88ad041e02e3764b3ee4cf"],
	# ["onboard", "3e94804b6f88ad041e02e3764b3ee4cf"],
	# ["onboarding", "3e94804b6f88ad041e02e3764b3ee4cf"],
	# ["new account", "3e94804b6f88ad041e02e3764b3ee4cf"],
	# ["laptop", "3e94804b6f88ad041e02e3764b3ee4cf"],
	# ["account", "3e94804b6f88ad041e02e3764b3ee4cf"],
	# # Access to Terminated or Departed associate's data
	# ["access data", "f7e870d61c9ee008cfc05fda97b0699e"],
	# ["terminated", "f7e870d61c9ee008cfc05fda97b0699e"],
	# # Reset Password for a business application (currently missing)
	["reset password", "6efb03b96f33118038ef17831c3ee468"],
	# ["password", "6efb03b96f33118038ef17831c3ee468"],
	# ["password reset", "6efb03b96f33118038ef17831c3ee468"]
]

# Loop through all desired searches, and search for each
for searchConfig in searchList:
	searchInIrisServicePortal(websiteURL, searchConfig[0], searchConfig[1]);

print "\n\nAll finished, closing the browser now..."
driver.close();
