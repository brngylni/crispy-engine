# Importing the necessary modules.
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys




# Creating the Linkedin Class
class LinkedIn:
    # Constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = "https://www.linkedin.com/login/"
        self.driver = webdriver.Chrome()
# Login operations.

    def login(self):
        self.driver.get(self.url)
        time.sleep(3)
        mail_field = self.driver.find_element_by_id("username")
        pass_field = self.driver.find_element_by_id("password")
        login_button = self.driver.find_element_by_css_selector("button[type=submit]")

        mail_field.send_keys(self.username)
        pass_field.send_keys(self.password)
        login_button.click()
        time.sleep(2)
# Connection Request Sending Operations.

    def sendConnectionRequest(self, url):
        self.driver.get(url)
        time.sleep(2)
        container = self.driver.find_element_by_class_name("pv-top-card")
        name = container.find_element_by_class_name("inline").text.split()[0]
        requestButton = container.find_element_by_css_selector("button")
        requestButton.click()
        time.sleep(1)
        addNoteDialog = self.driver.find_element_by_css_selector("div[role=dialog]")
        addNoteButton = addNoteDialog.find_element_by_class_name("mr1")
        addNoteButton.click()
        noteField = self.driver.find_element_by_id("custom-message")
        # You can change the request note from the line below.
        message = f"Hi {name}, it would be great to connect."
        noteField.send_keys(message)
        time.sleep(2)
        submitButton = self.driver.find_element_by_class_name("ml1")
        submitButton.click()

# Fetching Last Processed Connections.
    def fetchConnections(self, runtime):
        url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
        self.driver.get(url)
        time.sleep(2)
        messages = self.driver.find_element_by_class_name("msg-overlay-bubble-header")
        messages.click()
        connectionsContainer = self.driver.find_element_by_css_selector("div[role=main] ul")
        connections = connectionsContainer.find_elements_by_css_selector("li")
        array = []
        for connection in connections:
            array.append(connection.find_element_by_css_selector("a").get_attribute("href"))
        scroll = webdriver.ActionChains(self.driver)
        while True:
            try:
                scroll.key_up(Keys.SPACE).key_down(Keys.SPACE).perform()
                time.sleep(1)
                container = self.driver.find_element_by_class_name("artdeco-pagination")
                nextButton = container.find_element_by_class_name("artdeco-pagination__button--next")
                nextButton.click()
                time.sleep(5)
                pageConnections = self.driver.find_element_by_css_selector("div[role=main]").find_elements_by_css_selector("li")
                for connection in pageConnections:
                    array.append(connection.find_element_by_css_selector("a").get_attribute("href"))
                if len(array) >= int(runtime)*90:
                    break
            except NoSuchElementException:
                break

        return array
# Sending follow up message to accepted requests.

    def sendFollowUpMessage(self, url):
        self.driver.get(url)
        time.sleep(2)
        container = self.driver.find_element_by_class_name("pv-top-card")
        name = container.find_element_by_class_name("inline").text.split()[0]
        # You can change the follow up message from the line below.
        message = f"Hi {name}, thank you for connecting."
        sendMessageButton =  self.driver.find_element_by_class_name("message-anywhere-button")
        sendMessageButton.click()
        time.sleep(2)
        messageField = self.driver.find_element_by_css_selector("div[role=textbox] p")
        messageField.send_keys(message)
        time.sleep(1)
        submitMessageButton = self.driver.find_element_by_class_name("msg-form__send-button")
        submitMessageButton.click()
        time.sleep(1)
        closeConversationButton = self.driver.find_element_by_css_selector('button[data-control-name="overlay.close_conversation_window"]')
        closeConversationButton.click()
        time.sleep(1)
# Closing the browser.

    def closeBrowser(self):
        self.driver.close()
