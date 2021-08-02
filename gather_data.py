import csv
import os
from typing import Tuple

import bs4
import requests
# quandl
# "https://www.govtrack.us/congress/bills/116/hr221/summary"
# "https://www.govtrack.us/congress/bills/116/hr221"

NO_SUCH_BILL = "NO SUCH BILL"


def get_summary(bill_id: int) -> str:
    summary_url = f"https://www.govtrack.us/congress/bills/116/hr{bill_id}/summary"
    summary_html = requests.get(summary_url)
    if summary_html.status_code == 404:
        return NO_SUCH_BILL

    soup = bs4.BeautifulSoup(summary_html.text, 'html.parser')
    summary = soup.find("div", {"id": "libraryofcongress"})
    summary_parts = []
    if not hasattr(summary, "contents"):
        print()
    if len(summary.contents) < 4:
        if "No summary available." in summary.text:
            return "No summary available."
        print(summary.text)
        raise TypeError('uh oh')

    for element in summary.contents[3]:
        if "<script>" in str(element):
            continue
        if not hasattr(element, "text"):
            continue
        text = element.text
        if text.strip():
            summary_parts.append(text)
    return "\n".join(summary_parts)


def get_status(bill_id: int) -> str:
    status_url = f"https://www.govtrack.us/congress/bills/116/hr{bill_id}"
    status_html = requests.get(status_url)
    if status_html.status_code == 404:
        return NO_SUCH_BILL

    soup = bs4.BeautifulSoup(status_html.text, 'html.parser')
    # oh this is so fragile
    rows = soup.findAll("div", {"class": ["row"]})
    status = None
    for row in rows:
        status = row.findAll("div", {"class": ["col-sm-9", "col-md-10"]})
        if status:
            break
    if not status:
        raise TypeError("Can't find it")
    summary_parts = []
    if "Died in a previous Congress" in str(status[1].contents):
        return "Died in a previous Congress"
    if "incorporated" in str(status[1].contents):
        return "Incorporated into another bill"
    for element in status[1].contents:
        if "<script>" in str(element):
            continue
        if not hasattr(element, "text"):
            continue
        text = element.text
        if text.strip() and "—" in text:
            summary_parts.append(text.split("—")[0].strip())
    if not summary_parts:
        print("Uh oh")
        print(status[1].contents)
    return "\n".join(summary_parts)


def locate_file(file_name: str, executing_file: str) -> str:
    """
    Find file relative to a source file, e.g.
    locate("foo/bar.txt", __file__)

    Succeeds regardless to context of execution
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(executing_file)), file_name
    )
    return file_path


def load_all(start: int, end: int) -> Tuple[int, int]:
    file_name = locate_file("data2.csv", __file__)
    # os.remove(file_name)
    success = 0
    errors = 0
    with open(file_name, 'a', newline='') as csvfile:
        for bill_id in range(start, end):
            try:
                summary = get_summary(bill_id=bill_id)
                if summary == NO_SUCH_BILL:
                    continue
                status = get_status(bill_id=bill_id)
                writer = csv.writer(csvfile)
                writer.writerow([bill_id, status, summary])
                print(bill_id, "status", status, "summary",
                      summary.split("\n")[0][0:80] + "...")
                success += 1
            except Exception as ex:
                errors += 1
                print(ex)
    return success, errors


if __name__ == '__main__':
    # print(load_all(18,19))
    load_all(1, 1000)
