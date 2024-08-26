import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set up logging
logging.basicConfig(filename=r'C:\Users\Sunny\OneDrive\Desktop\Projects\Glassdoorscrape.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Set up the Selenium WebDriver with headless option."""
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver

def get_job_details(job_detail_list):
    """
    Extract job details from a list of job HTML elements.

    Args:
        job_detail_list (list): List of job HTML elements.

    Returns:
        list: List of job details tuples.
    """
    data = []
    for job in job_detail_list:
        try:
            employer = job.find("span", "EmployerProfile_compactEmployerName__LE242").text
        except AttributeError:
            continue

        try:
            logo_link = job.find("img", "EmployerLogo_logo__qwcMW logo").get("src")
        except AttributeError:
            logo_link = ""

        try:
            rating = job.find("div", "EmployerProfile_ratingContainer__ul0Ef", "span").text
        except AttributeError:
            rating = ""

        try:
            job_title = job.find("a", "JobCard_jobTitle___7I6y").text
        except AttributeError:
            continue

        try:
            job_location = job.find("div", "JobCard_location__rCz3x").text
        except AttributeError:
            job_location = ""

        try:
            job_details = job.find("div", "JobCard_jobDescriptionSnippet__yWW8q")
            job_description = job_details.find_all("div")[0].text
        except AttributeError:
            job_description = ""

        try:
            job_details = job.find("div", "JobCard_jobDescriptionSnippet__yWW8q")
            job_skills = job_details.find_all("div")[1].text
        except AttributeError:
            job_skills = ""

        try:
            job_listing = job.find("div", "JobCard_listingAge__Ny_nG").text
        except AttributeError:
            job_listing = ""

        job_record = (
            job_title,
            employer,
            job_location,
            job_description,
            job_skills,
            job_listing,
            rating,
            logo_link,
        )
        data.append(job_record)
    return data

def scrape_glassdoor_jobs(product_name):
    """
    Scrape job listings from Glassdoor.

    Args:
        product_name (str): Product name to search for.

    Returns:
        pd.DataFrame: DataFrame of job listings.
    """    
    try:
        driver = setup_driver()

        # Format product name for URL
        product_name = product_name.replace(" ", "_")

        # Construct URL
        url = f"https://www.glassdoor.co.in/Job{product_name}-jobs-SRCH_FW0,14_KO15,25.htm"

        # Load webpage
        driver.get(url)

        # Explicit wait for page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".JobCard_jobTitle___7I6y"))
        )

        # Get page source after JS has loaded
        html = driver.page_source

        # Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        # Find job listings
        job_detail_list = soup.find_all("li", {"data-test": "jobListing"})

        # Extract job details
        job_data = get_job_details(job_detail_list)

        # Define column names
        column_names = [
            "job_title",
            "employer",
            "job_location",
            "job_description",
            "job_skills",
            "job_listing",
            "rating",
            "logo_link",
        ]

        # Create DataFrame
        job_df = pd.DataFrame(columns=column_names, data=job_data)

        return job_df
    except Exception as e:
        logging.error("An error occurred during scraping", exc_info=True)
    finally:
        driver.quit()

def main():
    product_name = "/work-from-home-accountant"
    job_df = scrape_glassdoor_jobs(product_name)
    job_df.to_csv(r"C:\Users\Sunny\OneDrive\Desktop\Projects\Glassdoor\accoutant_jobs.csv", index=False)
    logging.info("Job scraping completed successfully.")

if __name__ == "__main__":
    main()
