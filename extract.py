import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

def get_url_list(url):
    # Initialize the driver
    driver = webdriver.Chrome()

    # Navigate to the webpage you want to scrape
    driver.get(url)

    # Find the element containing the URLs you want to scrape
    url_container = driver.find_element(By.XPATH, "//ul[contains(@class,'awsui_list-variant-expandable-link-group')]")

    # Get all the links within the container
    links = url_container.find_elements(By.TAG_NAME, "a")

    # Extract the URLs from the links and store them in a list
    url_list = []
    for link in links:
        url = link.get_attribute("href")
        url_list.append(url)

    # Close the browser window
    driver.quit()

     # Return the list of URLs
    return url_list


def is_pascal_case(s):
    if re.match('[A-Z]([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*', s):
        return True
    else:
        return False


def scrape_for_prefix_and_action(url, writer):
    # Send a GET request to the URL and get the HTML response
    response = requests.get(url)

    # Create a BeautifulSoup object from the HTML response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first paragraph element on the page
    paragraph = soup.find('p')

    # Get the text content of the paragraph
    paragraph_text = paragraph.get_text()

    # Find the index of the first occurrence of "(service prefix:"
    prefix_start_index = paragraph_text.find('(service prefix:')

    # Find the index of the end of the prefix
    prefix_end_index = paragraph_text.find(')', prefix_start_index)

    # Extract the prefix
    prefix = paragraph_text[prefix_start_index+len('(service prefix:'):prefix_end_index].strip()

    print(f'Service prefix: {prefix}')

    try:
        # Find the table element on the page
        table = soup.find('table')
        # Find the header row of the table
        header_row = table.find('tr')
            # Find the index of the "Actions" column
        header_cells = header_row.find_all('th')
        actions_column_index = None
        for i, cell in enumerate(header_cells):
            if cell.get_text() == 'Actions':
                actions_column_index = i
                break

        # Extract the actions from the table and append the service prefix to each action
        actions = []
        data_rows = table.find_all('tr')[1:]
        for row in data_rows:
            cells = row.find_all('td')
            if len(cells) > actions_column_index:
                action_cell = cells[actions_column_index]
                action_links = action_cell.find_all('a')
                for link in action_links:
                    action = link.get_text().strip()
                    if action != '' and is_pascal_case(str(action)):
                        actions.append(action)
        # Print the actions
        print('Actions:')
        for action in actions:
            print(action)
            writer.writerow([prefix, action, f'{prefix}:{action}'])
    except:
        print("No Table found for url: " + url)

    
if __name__ == "__main__":
    main_url="https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html"
    service_urls=get_url_list(main_url)
    # Open a file for writing
    with open('aws_actions.csv', 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Service Prefix', 'Action', 'Combined'])

        # Loop over the service URLs and scrape the actions
        for url in service_urls:
            scrape_for_prefix_and_action(url, writer)
