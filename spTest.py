from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys

print "Hello World"


driver = webdriver.Chrome()
driver.get("http://jnjsandbox5.service-now.com/iris_gl");
driver.implicitly_wait(20) # seconds

#elem = driver.find_element_by_name("q");
elem = driver.find_element_by_xpath("//*[@id='homepage-search']/div/div[1]/div[2]/form/div/input");

elem.clear()
elem.send_keys("new hire");
elem.send_keys(Keys.RETURN);
myResults = driver.find_element_by_xpath("//*[@id='xb218bc42db4e4bc4117c5d30cf96194a']/div");

# Assert the "New Hire" text is within the search results
theText = myResults.text;
import string
theText = filter(lambda x: x in string.printable, theText)
assert "New Hire" in theText;

# Assert the New Hire catalog item is within the search results
desiredLink = driver.find_element_by_xpath("//a[contains(@href,'?id=iris_cat_item&sys_id=3e94804b6f88ad041e02e3764b3ee4cf')]");
print(desiredLink.text);

driver.close();
