import requests
from bs4 import BeautifulSoup

from core.roman2int.arabic2litteral import convert_numbers_to_french
from core.roman2int.av_jc import replace_av_jc
from core.roman2int.roman2numerals import replace_roman_numerals
from core.roman2int.roman2ordinals import replace_roman_or_arabic_ordinals

MAX_WORDS_PER_SECTION = 4096

UNWANTED_CLASSES = ['infobox_v3', 'infobox', 'infobox--frwiki', 'noarchive', 'reference', 'mw-editsection',
                    'mw-file-description', 'references-small', 'reference-cadre', 'gallery', 'references',
                    'references-column-width', 'navbox-container', 'bandeau-portail', 'catlinks', 'autres-projets']

UNWANTED_IDS = ['Bibliographie', 'Liens_externes', 'Articles_et_autres_références',
                'Ouvrages_spécifiques_sur_la_période_thinite', "Ouvrages_généraux_sur_l'Égypte_antique",
                'Références', 'Notes', 'Notes_et_références']


def extract_text_from_url(url):
    """Extract text content from a webpage, returning each paragraph as a separate element"""
    # Add headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()

    # Remove unwanted sections by ID
    for unwanted_id in UNWANTED_IDS:
        element = soup.find(id=unwanted_id)
        if element:
            element.decompose()

    # Remove elements that contain any of the unwanted classes
    for element in soup.find_all():
        # Skip elements that don't have attributes (like text nodes)
        if not hasattr(element, 'attrs') or element.attrs is None:
            continue

        element_classes = element.get('class', [])
        if any(unwanted_class in element_classes for unwanted_class in UNWANTED_CLASSES):
            element.decompose()

    refs_to_remove = soup.find_all('a', title="Aide:Référence nécessaire")
    for ref in refs_to_remove:
        ref.decompose()

    # Find all <p> tags
    paragraphs = soup.find_all('p')

    sections = []

    for p in paragraphs:
        p_text = p.get_text().strip()
        if p_text:  # Only process non-empty paragraphs
            # Clean the paragraph text
            lines = (line.strip() for line in p_text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_p_text = ' '.join(chunk for chunk in chunks if chunk)

            # Count words and check limit
            p_word_count = len(clean_p_text.split())
            if p_word_count >= MAX_WORDS_PER_SECTION:
                raise ValueError(f"Paragraph exceeds {MAX_WORDS_PER_SECTION} words ({p_word_count} words)")

            clean_p_text = replace_roman_or_arabic_ordinals(clean_p_text)
            clean_p_text = replace_roman_numerals(clean_p_text)
            clean_p_text = replace_av_jc(clean_p_text)
            clean_p_text = convert_numbers_to_french(clean_p_text)
            sections.append(clean_p_text)

    return sections


def print_text_wrapped(text, max_width=120):
    words = text.split()
    current_line = ""

    for word in words:
        # Check if adding the next word would exceed the limit
        if len(current_line + " " + word) <= max_width:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            # Print the current line and start a new one
            if current_line:
                print(current_line)
            current_line = word

    # Print any remaining text
    if current_line:
        print(current_line)

    # Add a newline after each element
    print()


def main():
    # Get URL from user
    url = "https://fr.wikipedia.org/wiki/Moyen_Empire"

    print(f"\nProcessing URL: {url}")

    text = extract_text_from_url(url)

    for e in text:
        print_text_wrapped(e)


if __name__ == "__main__":
    main()
