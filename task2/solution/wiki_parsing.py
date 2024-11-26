from collections import Counter

import asyncio
import csv

import aiohttp
from bs4 import BeautifulSoup



class BeastsScraper:
    def __init__(self, session: aiohttp.ClientSession):
        self.base_url = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from="
        self.session = session

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

    def parse_beasts_names(self, soup: BeautifulSoup, current_letter: str) -> tuple[Counter, bool, int]:
        current_letter = current_letter.upper()

        pages_div = soup.find("div", id="mw-pages")
        if not pages_div:
            return Counter(), False, 0

        li_elements = pages_div.select('.mw-category li')
        if not li_elements:
            return Counter(), False, 0

        relevant_elements = [li for li in li_elements if li.get_text().strip()[0].upper() == current_letter]
        beasts_first_letters = [li.get_text().strip()[0].upper() for li in relevant_elements]

        letter_counts = Counter(beasts_first_letters)
        num_categories = len(relevant_elements)

        continue_parsing = num_categories > 0
        return letter_counts, continue_parsing, num_categories

    def get_next_page_url(self, soup: BeautifulSoup) -> str | None:
        base_url = "https://ru.wikipedia.org"
        next_page_link = soup.find('a', string="Следующая страница")
        if next_page_link:
            link = next_page_link.get('href')
            return f"{base_url}{link}"
        return None

    async def process_letter(self, letter: str) -> Counter:
        counts = Counter()
        url = f"{self.base_url}{letter}"
        while True:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "lxml")

            beasts_counts, continue_parsing, num_categories = self.parse_beasts_names(soup, letter)
            counts.update(beasts_counts)

            if not continue_parsing:
                break

            next_page_url = self.get_next_page_url(soup)
            if not next_page_url:
                break

            url = next_page_url

        return counts

    async def scrape(self, alphabet: str) -> Counter:
        tasks = []
        for letter in alphabet:
            tasks.append(self.process_letter(letter))

        all_counts_list = await asyncio.gather(*tasks)

        total_counts = Counter()
        for counts in all_counts_list:
            total_counts.update(counts)

        return total_counts

    async def main(self, alphabet: str) -> Counter:
        return await self.scrape(alphabet)


def write_to_csv(data: dict[str, int], filename: str) -> None:
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for letter in sorted(data.keys()):
            writer.writerow([letter, data[letter]])


async def main() -> dict[str, int]:
    async with aiohttp.ClientSession() as session:
        scraper = BeastsScraper(session)
        counts = await scraper.main(alphabet)
        return counts


if __name__ == "__main__":
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counts = asyncio.run(main())
    write_to_csv(counts, "beasts.csv")
