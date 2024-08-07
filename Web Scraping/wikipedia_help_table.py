import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_table_data(url):
    """Send a GET request to the URL and return the HTML response"""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text

def parse_table(html):
    """Parse the HTML using BeautifulSoup and return the table data"""
    soup = BeautifulSoup(html, "html.parser")
    caption = soup.find("caption", text=lambda text: text and text.strip() == "Overview of basic table markup")
    if caption:
        table_data = caption.find_parent("table", class_="wikitable")
        rows = table_data.find_all("tr")
        return [[cell.text.strip() for cell in row.find_all(["th", "td"])] for row in rows]
    return None

def convert_to_dataframe(table_data):
    """Convert the table data into a Pandas DataFrame"""
    df = pd.DataFrame(table_data)
    df.columns = df.iloc[0]
    return df[1:]

def save_to_csv(df, filename):
    """Save the DataFrame to a CSV file"""
    df.to_csv(filename, index=False)

def main():
    url = "https://en.wikipedia.org/wiki/Help:Table"
    html = get_table_data(url)
    table_data = parse_table(html)
    if table_data:
        df = convert_to_dataframe(table_data)
        save_to_csv(df, r"C:\Users\Sunny\OneDrive\Desktop\Projects\final_list.csv")
    else:
        print("Table data not found")

if __name__ == "__main__":
    main()
