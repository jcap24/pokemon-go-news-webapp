from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re


class PokebattlerScraper:
    """Scraper for Pokebattler raid counter data using Selenium."""

    BASE_URL = "https://www.pokebattler.com"
    RAIDS_URL = f"{BASE_URL}/raids"

    def __init__(self):
        """Initialize Selenium WebDriver."""
        self.driver = None

    def _init_driver(self):
        """Initialize Chrome WebDriver with headless options."""
        if self.driver:
            return

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        try:
            # Use webdriver-manager to automatically handle ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Chrome WebDriver initialized successfully")
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")
            raise

    def _close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape_raid_bosses(self):
        """Scrape list of current raid bosses from main raids page."""
        try:
            self._init_driver()

            print("Loading Pokebattler raids page...")
            self.driver.get(self.RAIDS_URL)

            # Wait for content to load (increase wait time for dynamic content)
            time.sleep(5)

            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            raid_bosses = []

            # Look for raid boss links - Pokebattler uses links to individual raid pages
            # Pattern: /raids/defenders/POKEMON_NAME.html or similar
            raid_links = soup.find_all('a', href=re.compile(r'/raids/(defenders/)?[A-Z_]+'))

            seen_names = set()

            for link in raid_links:
                try:
                    href = link.get('href', '')

                    # Skip navigation links and non-boss links
                    if any(skip in href.lower() for skip in ['pokebox', 'login', 'register', 'guide', 'article']):
                        continue

                    # Extract boss name from URL
                    # Format: /raids/defenders/POKEMON_NAME.html or /raids/POKEMON_NAME
                    name_match = re.search(r'/raids/(?:defenders/)?([A-Z_]+)', href)
                    if not name_match:
                        continue

                    boss_slug = name_match.group(1)
                    boss_name = self._normalize_pokemon_name(boss_slug.replace('_', ' '))

                    # Skip if already seen, invalid, or too short
                    if boss_name in seen_names or len(boss_name) < 3:
                        continue

                    seen_names.add(boss_name)

                    # Try to determine tier from context
                    tier = self._extract_tier_from_context(link)

                    raid_boss = {
                        'name': boss_name,
                        'tier': tier,
                        'url': f"{self.BASE_URL}{href}" if href.startswith('/') else href,
                        'is_active': True
                    }

                    raid_bosses.append(raid_boss)

                except Exception as e:
                    print(f"Error parsing boss link: {e}")
                    continue

            # Remove duplicates by name (keep first occurrence)
            unique_bosses = []
            seen = set()
            for boss in raid_bosses:
                if boss['name'] not in seen:
                    unique_bosses.append(boss)
                    seen.add(boss['name'])

            print(f"Pokebattler: Found {len(unique_bosses)} raid bosses")
            return unique_bosses[:50]  # Limit to 50 most relevant

        except Exception as e:
            print(f"Error scraping Pokebattler raid bosses: {e}")
            return []
        finally:
            self._close_driver()

    def scrape_boss_counters(self, boss_name):
        """Scrape counters for a specific raid boss."""
        try:
            self._init_driver()

            # Convert boss name to URL format
            boss_slug = boss_name.upper().replace(' ', '_').replace('-', '_')

            # Try multiple URL formats
            url_formats = [
                f"{self.BASE_URL}/raids/defenders/{boss_slug}.html",
                f"{self.BASE_URL}/raids/{boss_slug}",
                f"{self.BASE_URL}/raids/defenders/{boss_slug}"
            ]

            boss_info = {'name': boss_name}
            counters = []

            for boss_url in url_formats:
                try:
                    print(f"Trying URL: {boss_url}")
                    self.driver.get(boss_url)
                    time.sleep(4)  # Wait for dynamic content

                    # Check if page loaded successfully
                    if "404" not in self.driver.title.lower() and "not found" not in self.driver.page_source.lower()[:500]:
                        # Get page source
                        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

                        # Extract boss info
                        boss_info = self._extract_boss_info(soup, boss_name)

                        # Extract counters from the page
                        counters = self._extract_counters_from_page(soup)

                        if counters:  # If we found counters, stop trying URLs
                            break

                except Exception as e:
                    print(f"Error with URL {boss_url}: {e}")
                    continue

            print(f"Pokebattler: Found {len(counters)} counters for {boss_name}")

            return {
                'boss': boss_info,
                'counters': counters
            }

        except Exception as e:
            print(f"Error scraping counters for {boss_name}: {e}")
            return {
                'boss': {'name': boss_name},
                'counters': []
            }
        finally:
            self._close_driver()

    def scrape_all_raids_and_counters(self):
        """Main method: scrape all raid bosses and their counters."""
        print("Starting Pokebattler scraping with Selenium...")

        # Get all current raid bosses
        raid_bosses = self.scrape_raid_bosses()

        if not raid_bosses:
            print("No raid bosses found. Using fallback approach...")
            # Fallback: try common raid bosses
            raid_bosses = [
                {'name': 'Dialga', 'tier': '5', 'is_active': True},
                {'name': 'Palkia', 'tier': '5', 'is_active': True},
                {'name': 'Giratina', 'tier': '5', 'is_active': True},
                {'name': 'Regigigas', 'tier': '5', 'is_active': True},
            ]

        all_raid_data = []

        # Limit to 10 bosses to avoid long scraping times
        for idx, boss in enumerate(raid_bosses[:10]):
            try:
                print(f"Scraping {boss['name']} ({idx + 1}/{min(len(raid_bosses), 10)})...")

                # Get detailed counters for this boss
                boss_data = self.scrape_boss_counters(boss['name'])

                # Merge with basic boss info
                boss_data['boss'].update(boss)

                all_raid_data.append({
                    'boss_data': boss_data['boss'],
                    'counters': boss_data['counters']
                })

                # Rate limiting
                if idx < min(len(raid_bosses), 10) - 1:
                    time.sleep(2)

            except Exception as e:
                print(f"Error processing {boss['name']}: {e}")
                continue

        print(f"Pokebattler scraping complete: {len(all_raid_data)} raids processed")
        return all_raid_data

    def _extract_tier_from_context(self, link_element):
        """Try to extract tier from surrounding context."""
        # Look for tier indicators in parent elements
        parent = link_element.find_parent()
        if parent:
            text = parent.get_text().lower()
            if 'tier 5' in text or 'legendary' in text or 't5' in text:
                return '5'
            elif 'tier 3' in text or 't3' in text:
                return '3'
            elif 'tier 1' in text or 't1' in text:
                return '1'
            elif 'mega' in text:
                return 'Mega'
            elif 'shadow' in text and 'raid' in text:
                return 'Shadow'
        return 'Unknown'

    def _extract_boss_info(self, soup, boss_name):
        """Extract detailed boss information from boss page."""
        boss_info = {'name': boss_name}

        try:
            # Look for CP information in text
            page_text = soup.get_text()

            # Extract CP ranges - look for patterns like "CP 2217-2307" or "2217 - 2307"
            cp_patterns = [
                r'CP[:\s]+(\d+)[-\s]+(\d+)',
                r'(\d{4})\s*[-–]\s*(\d{4})',
            ]

            for pattern in cp_patterns:
                cp_matches = re.findall(pattern, page_text)
                if cp_matches:
                    boss_info['cp_min'] = int(cp_matches[0][0])
                    boss_info['cp_max'] = int(cp_matches[0][1])
                    if len(cp_matches) > 1:
                        boss_info['cp_boosted_min'] = int(cp_matches[1][0])
                        boss_info['cp_boosted_max'] = int(cp_matches[1][1])
                    break

            # Try to find type information
            type_keywords = ['Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison',
                           'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon',
                           'Dark', 'Steel', 'Fairy', 'Normal']

            found_types = []
            for keyword in type_keywords:
                # Look for type keywords in context
                if re.search(rf'\b{keyword}\stype\b', page_text, re.IGNORECASE) or \
                   re.search(rf'Type:\s*{keyword}', page_text, re.IGNORECASE):
                    if keyword not in found_types:
                        found_types.append(keyword)

            if found_types:
                boss_info['types'] = ','.join(found_types[:2])  # Limit to 2 types

            # Look for weakness information
            weakness_match = re.search(r'Weak(?:ness)?(?:es)?[:\s]+([A-Za-z\s,&]+)', page_text, re.IGNORECASE)
            if weakness_match:
                weakness_text = weakness_match.group(1)
                weaknesses = []
                for keyword in type_keywords:
                    if keyword in weakness_text:
                        weaknesses.append(keyword)
                if weaknesses:
                    boss_info['weaknesses'] = ','.join(weaknesses[:4])

        except Exception as e:
            print(f"Error extracting boss info: {e}")

        return boss_info

    def _extract_counters_from_page(self, soup):
        """Extract counter Pokemon from the page."""
        counters = []

        try:
            # Pokebattler typically shows counters in a structured format
            # Look for Pokemon names in the page

            # Common Pokemon names to look for (known good counters)
            known_pokemon = [
                'Mewtwo', 'Rayquaza', 'Dialga', 'Palkia', 'Groudon', 'Kyogre', 'Garchomp',
                'Salamence', 'Dragonite', 'Tyranitar', 'Metagross', 'Machamp', 'Lucario',
                'Conkeldurr', 'Terrakion', 'Reshiram', 'Zekrom', 'Excadrill', 'Rhyperior',
                'Rampardos', 'Mamoswine', 'Weavile', 'Gengar', 'Chandelure', 'Giratina',
                'Landorus', 'Thundurus', 'Tornadus', 'Electivire', 'Magnezone', 'Togekiss',
                'Gardevoir', 'Roserade', 'Venusaur', 'Charizard', 'Blastoise', 'Sceptile',
                'Swampert', 'Blaziken', 'Kyurem', 'Darkrai', 'Heatran', 'Latios', 'Latias',
                'Entei', 'Raikou', 'Suicune', 'Articuno', 'Zapdos', 'Moltres', 'Snorlax',
                'Gyarados', 'Vaporeon', 'Jolteon', 'Flareon', 'Espeon', 'Umbreon', 'Leafeon',
                'Glaceon', 'Sylveon', 'Luxray', 'Honchkrow', 'Tangrowth', 'Yanmega'
            ]

            page_text = soup.get_text()
            found_pokemon = []

            # Look for Pokemon in order (to preserve ranking)
            for pokemon in known_pokemon:
                if pokemon in page_text:
                    # Count how early it appears (rough ranking)
                    index = page_text.find(pokemon)
                    if index != -1:
                        found_pokemon.append((index, pokemon))

            # Sort by appearance order (earlier = better rank)
            found_pokemon.sort(key=lambda x: x[0])

            # Create counter entries
            for rank, (_, pokemon_name) in enumerate(found_pokemon[:20], 1):
                # Check for Shadow/Mega variants
                context_start = max(0, page_text.find(pokemon_name) - 50)
                context_end = min(len(page_text), page_text.find(pokemon_name) + 50)
                context = page_text[context_start:context_end].lower()

                counter = {
                    'rank': rank,
                    'pokemon_name': pokemon_name,
                    'is_shadow': 'shadow' in context,
                    'is_mega': 'mega' in context,
                    'is_legendary': pokemon_name in [
                        'Mewtwo', 'Rayquaza', 'Dialga', 'Palkia', 'Groudon', 'Kyogre',
                        'Reshiram', 'Zekrom', 'Giratina', 'Landorus', 'Thundurus', 'Tornadus',
                        'Kyurem', 'Darkrai', 'Heatran', 'Latios', 'Latias', 'Entei', 'Raikou',
                        'Suicune', 'Articuno', 'Zapdos', 'Moltres', 'Terrakion'
                    ]
                }
                counters.append(counter)

        except Exception as e:
            print(f"Error extracting counters: {e}")

        return counters

    def _normalize_pokemon_name(self, name):
        """Normalize Pokemon names."""
        # Remove extra whitespace
        name = ' '.join(name.split())

        # Handle common formatting
        name = name.replace('(Shadow)', '').replace('(Mega)', '')
        name = name.strip()

        # Capitalize properly
        if not name.isupper():
            name = ' '.join(word.capitalize() for word in name.split())

        return name
