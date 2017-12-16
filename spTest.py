from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.chrome.options import Options
import string

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

def searchInIrisServicePortal(websiteURL, search_string, catalogSysId):

	vprint ("Loading website\n")
	driver.get(websiteURL);
	driver.implicitly_wait(15) # seconds
	# Find the search box
	elem = driver.find_element_by_xpath("//*[@id='homepage-search']/div/div[1]/div[2]/form/div/input");

	outputString = "Searching '%s': " % (search_string)
	sys.stdout.write("%-25s" % (outputString))

	elem.clear()
	elem.send_keys(search_string);
	elem.send_keys(Keys.RETURN);

	#lookForText();

	# Assert the New Hire catalog item is within the search results
	#desiredLink = driver.find_element_by_xpath("//a[contains(@href,'?id=iris_cat_item&sys_id=3e94804b6f88ad041e02e3764b3ee4cf')]");

	catURL = '?id=iris_cat_item&sys_id=%s' % (catalogSysId)
	xPathDesired = "//a[contains(@href,'%s')]" % (catURL)

	try: 
		desiredLink = driver.find_element_by_xpath(xPathDesired);
		print("Found (%s)" % (desiredLink.text));
	except:
		print "Failed"


	# Try to find the whole list of catalog items
	try: 
		#xPathDesired = "//a[contains(@href,'?id=iris_cat_item')]"
		xPathDesired = "//a[contains(@href, '?id=iris_cat_item')]"
		desiredList = driver.find_elements_by_xpath(xPathDesired);
	except:
		print "Failed to find list"
	else:
		count = 1;
		for element in desiredList:
			print("   (%2d) --> %s" % (count, printable(element.text)));

			vprint("        INNER: %s\n" % (printable(element.get_attribute('innerHTML'))))
			vprint("        OUTER: %s\n" % (printable(element.get_attribute('outerHTML'))))
			vprint("        HREF:  %s\n" % (printable(element.get_attribute('href'))))
			vprint("        TEXT:  %s\n" % (printable(element.text)))
			count = count + 1;



	vprint ("   Catalog URL = %s\n" % (catURL))
	vprint ("   xPath = %s\n" % (xPathDesired))


# ------------------------------------------------------------------------------
# --------------------------- Main ---------------------------------------------
# ------------------------------------------------------------------------------

verbose = False;
chrome_options = Options()
chrome_options.add_argument("--dns-prefetch-disable")
print ("Opening browser")
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver = webdriver.Chrome()

# Pre-load a website
driver.get("http://jnjsandbox5.service-now.com/iris_gl");


print "\n\n\n\n";
websiteURL="http://jnjsandbox5.service-now.com/iris_gl"
#websiteURL="http://jnjprod.service-now.com/iris_gl"
searchInIrisServicePortal(websiteURL, "new hire", "3e94804b6f88ad041e02e3764b3ee4cf");
searchInIrisServicePortal(websiteURL, "email", "abea375f75a20d0029e60de16298b1bb");




print "\n\nAll finished, closing the browser now..."
driver.close();
