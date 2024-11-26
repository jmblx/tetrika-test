from unittest.mock import patch
import pytest
import aiohttp
from bs4 import BeautifulSoup
from collections import Counter
from task2.solution.wiki_parsing import BeastsScraper, write_to_csv


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "letter, url, expected_counts, expected_continue_parsing, expected_num_categories",
    [
        ('К', "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from=Ка",
         Counter({'К': 200}), True, 200),
        ('A', "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from=A", Counter({'A': 200}),
         True, 200),
        ('И', "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from=A", Counter({'И': 0}),
         False, 0),
        ('К', "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from=Ию", Counter({'К': 196}),
         True, 196),
    ]
)
async def test_parse_beasts_names(letter, url, expected_counts, expected_continue_parsing, expected_num_categories):
    async with aiohttp.ClientSession() as session:
        scraper = BeastsScraper(session=session)
        html_content = await scraper.fetch(url)
        soup = BeautifulSoup(html_content, 'html.parser')

        letter_counts, continue_parsing, num_categories = scraper.parse_beasts_names(soup, letter)

        assert letter_counts == expected_counts
        assert continue_parsing == expected_continue_parsing
        assert num_categories == expected_num_categories


@pytest.mark.asyncio
async def test_parse_beasts_names_from_file():
    with open('task2/solution/tests/test.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    scraper = BeastsScraper(session=None)
    soup = BeautifulSoup(html_content, 'html.parser')

    letter_counts, continue_parsing, num_categories = scraper.parse_beasts_names(soup, 'Й')

    assert letter_counts == Counter({'Й': 4})
    assert num_categories == 4


@pytest.mark.asyncio
async def test_scrape_A():
    async with aiohttp.ClientSession() as session:
        scraper = BeastsScraper(session=session)

        alphabet = "A"

        result = await scraper.scrape(alphabet)

        assert result == Counter({'A': 3455})


def test_get_next_page_url():
    scraper = BeastsScraper(session=None)
    html_content = "<html><body><div id='mw-pages'><a href='/w/index.php?title=Категория:Животные_по_алфавиту&from=A'>Следующая страница</a></div></body></html>"
    soup = BeautifulSoup(html_content, 'html.parser')

    next_page_url = scraper.get_next_page_url(soup)
    assert next_page_url == "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from=A"


def test_write_to_csv():
    data = Counter({'А': 1286, 'Б': 256, 'В': 512})
    with patch('builtins.open', create=True) as mock_open:
        write_to_csv(data, 'test.csv')
        mock_open.assert_called_once_with('test.csv', mode='w', newline='', encoding='utf-8')
