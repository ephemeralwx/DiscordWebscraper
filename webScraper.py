import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
from datetime import datetime

class InternshipScraper:
    def __init__(self):
        self.internships = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Define categories with keywords for classification
        self.categories = {
            'Technology': ['tech', 'software', 'developer', 'data', 'IT', 'programming', 'computer', 'cyber', 'web', 'coding', 'AI', 'artificial intelligence', 'machine learning', 'engineering'],
            'Healthcare': ['health', 'medical', 'hospital', 'clinical', 'nursing', 'healthcare', 'pharma', 'biomedical', 'patient'],
            'Business': ['business', 'finance', 'accounting', 'marketing', 'sales', 'management', 'consulting', 'entrepreneur', 'analyst', 'operations'],
            'Science': ['science', 'research', 'laboratory', 'biology', 'chemistry', 'physics', 'environmental', 'researcher', 'scientist', 'lab'],
            'Arts & Media': ['art', 'design', 'media', 'journalism', 'writing', 'creative', 'film', 'music', 'graphic', 'photography', 'theatre', 'fashion'],
            'Education': ['education', 'teaching', 'tutor', 'school', 'academic', 'learning', 'instructor'],
            'Government & Law': ['government', 'policy', 'legal', 'law', 'justice', 'political', 'public service', 'nonprofit', 'advocacy'],
            'Engineering': ['engineering', 'mechanical', 'civil', 'electrical', 'aerospace', 'chemical', 'industrial', 'robotics'],
        }
    
    def scrape_indeed(self, num_pages=10):
        """Scrape Indeed for high school internships"""
        print("Scraping Indeed...")
        
        for page in range(num_pages):
            url = f"https://www.indeed.com/jobs?q=summer+internship+high+school&start={page * 10}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_=re.compile('job_'))
                
                for job in job_cards:
                    try:
                        title_elem = job.find('a', class_=re.compile('jcs-JobTitle'))
                        company_elem = job.find('span', class_='companyName')
                        location_elem = job.find('div', class_='companyLocation')
                        description_elem = job.find('div', class_='job-snippet')
                        
                        if title_elem and "intern" in title_elem.text.lower():
                            title = title_elem.text.strip()
                            company = company_elem.text.strip() if company_elem else "Not specified"
                            location = location_elem.text.strip() if location_elem else "Not specified"
                            description = description_elem.text.strip() if description_elem else "No description available"
                            
                            job_url = "https://www.indeed.com" + title_elem['href'] if title_elem.has_attr('href') else "No link available"
                            
                            self.internships.append({
                                'title': title,
                                'company': company,
                                'location': location,
                                'description': description,
                                'url': job_url,
                                'source': 'Indeed'
                            })
                    except Exception as e:
                        print(f"Error parsing Indeed job: {e}")
                
                # Don't overload the server with requests
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Failed to retrieve Indeed page {page+1}: {response.status_code}")
    
    def scrape_linkedin(self, num_pages=10):
        """Scrape LinkedIn for high school internships"""
        print("Scraping LinkedIn...")
        
        for page in range(num_pages):
            url = f"https://www.linkedin.com/jobs/search/?keywords=summer%20internship%20high%20school&start={page * 25}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')
                
                for job in job_cards:
                    try:
                        title_elem = job.find('h3', class_='base-search-card__title')
                        company_elem = job.find('h4', class_='base-search-card__subtitle')
                        location_elem = job.find('span', class_='job-search-card__location')
                        link_elem = job.find('a', class_='base-card__full-link')
                        
                        if title_elem and ("intern" in title_elem.text.lower() or "internship" in title_elem.text.lower()):
                            title = title_elem.text.strip()
                            company = company_elem.text.strip() if company_elem else "Not specified"
                            location = location_elem.text.strip() if location_elem else "Not specified"
                            job_url = link_elem['href'] if link_elem and link_elem.has_attr('href') else "No link available"
                            
                            self.internships.append({
                                'title': title,
                                'company': company,
                                'location': location,
                                'description': "See link for details",
                                'url': job_url,
                                'source': 'LinkedIn'
                            })
                    except Exception as e:
                        print(f"Error parsing LinkedIn job: {e}")
                
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Failed to retrieve LinkedIn page {page+1}: {response.status_code}")
    
    def scrape_chegg(self, num_pages=5):
        """Scrape Chegg Internships for high school opportunities"""
        print("Scraping Chegg Internships...")
        
        for page in range(1, num_pages + 1):
            url = f"https://www.internships.com/high-school?page={page}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='internship-row')
                
                for job in job_cards:
                    try:
                        title_elem = job.find('h2', class_='internship-title')
                        company_elem = job.find('div', class_='company-name')
                        location_elem = job.find('span', class_='location')
                        description_elem = job.find('div', class_='description')
                        link_elem = job.find('a', class_='title-link')
                        
                        if title_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip() if company_elem else "Not specified"
                            location = location_elem.text.strip() if location_elem else "Not specified"
                            description = description_elem.text.strip() if description_elem else "No description available"
                            job_url = "https://www.internships.com" + link_elem['href'] if link_elem and link_elem.has_attr('href') else "No link available"
                            
                            self.internships.append({
                                'title': title,
                                'company': company,
                                'location': location,
                                'description': description,
                                'url': job_url,
                                'source': 'Chegg Internships'
                            })
                    except Exception as e:
                        print(f"Error parsing Chegg job: {e}")
                
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Failed to retrieve Chegg page {page}: {response.status_code}")
                
    def scrape_wayup(self, num_pages=5):
        """Scrape WayUp for high school internships"""
        print("Scraping WayUp...")
        
        for page in range(1, num_pages + 1):
            url = f"https://www.wayup.com/s/internships/high-school/{page}/"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job-card')
                
                for job in job_cards:
                    try:
                        title_elem = job.find('h2', class_='job-title')
                        company_elem = job.find('div', class_='company-name')
                        location_elem = job.find('div', class_='job-location')
                        link_elem = job.find('a', class_='job-link')
                        
                        if title_elem and ("intern" in title_elem.text.lower() or "internship" in title_elem.text.lower()):
                            title = title_elem.text.strip()
                            company = company_elem.text.strip() if company_elem else "Not specified"
                            location = location_elem.text.strip() if location_elem else "Not specified"
                            job_url = "https://www.wayup.com" + link_elem['href'] if link_elem and link_elem.has_attr('href') else "No link available"
                            
                            self.internships.append({
                                'title': title,
                                'company': company,
                                'location': location,
                                'description': "See link for details",
                                'url': job_url,
                                'source': 'WayUp'
                            })
                    except Exception as e:
                        print(f"Error parsing WayUp job: {e}")
                
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Failed to retrieve WayUp page {page}: {response.status_code}")
    
    def scrape_lumiere(self, num_pages=5):
        """Scrape Lumiere for high school internships"""
        print("Scraping Lumiere...")
        
        for page in range(1, num_pages + 1):
            url = f"https://www.lumiereducation.com/programs/page/{page}/?category=internships"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                program_cards = soup.find_all('div', class_='program-card')
                
                for program in program_cards:
                    try:
                        title_elem = program.find('h3', class_='program-title')
                        details_elem = program.find('div', class_='program-details')
                        link_elem = program.find('a')
                        
                        if title_elem and 'intern' in title_elem.text.lower():
                            title = title_elem.text.strip()
                            details = details_elem.text.strip() if details_elem else "See link for details"
                            job_url = link_elem['href'] if link_elem and link_elem.has_attr('href') else "No link available"
                            
                            self.internships.append({
                                'title': title,
                                'company': 'Lumiere Education',
                                'location': 'Various/Remote',
                                'description': details,
                                'url': job_url,
                                'source': 'Lumiere'
                            })
                    except Exception as e:
                        print(f"Error parsing Lumiere program: {e}")
                
                time.sleep(random.uniform(2, 4))
            else:
                print(f"Failed to retrieve Lumiere page {page}: {response.status_code}")
    
    def scrape_findecs(self, num_pages=5):
        """Scrape FindECs for high school internships"""
        print("Scraping FindECs...")
        
        for page in range(1, num_pages + 1):
            url = f"https://www.findecs.org/opportunities/page/{page}/?type=internship"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                opportunity_cards = soup.find_all('div', class_='opportunity-card')
                
                for opportunity in opportunity_cards:
                    try:
                        title_elem = opportunity.find('h2', class_='opportunity-title')
                        org_elem = opportunity.find('div', class_='organization')
                        location_elem = opportunity.find('div', class_='location')
                        link_elem = opportunity.find('a', class_='opportunity-link')
                        
                        if title_elem:
                            title = title_elem.text.strip()
                            organization = org_elem.text.strip() if org_elem else "Not specified"
                            location = location_elem.text.strip() if location_elem else "Not specified"
                            job_url = link_elem['href'] if link_elem and link_elem.has_attr('href') else "No link available"
                            
                            self.internships.append({
                                'title': title,
                                'company': organization,
                                'location': location,
                                'description': "See link for details",
                                'url': job_url,
                                'source': 'FindECs'
                            })
                    except Exception as e:
                        print(f"Error parsing FindECs opportunity: {e}")
                
                time.sleep(random.uniform(2, 4))
            else:
                print(f"Failed to retrieve FindECs page {page}: {response.status_code}")
    
    def scrape_internship_finder(self, num_pages=5):
        """Scrape InternshipFinder for high school internships"""
        print("Scraping InternshipFinder...")
        
        for page in range(1, num_pages + 1):
            url = f"https://www.internshipfinder.com/high-school-internships/?page={page}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                internship_listings = soup.find_all('div', class_='listing-card')
                
                for listing in internship_listings:
                    try:
                        title_elem = listing.find('h3', class_='listing-title')
                        company_elem = listing.find('div', class_='company-name')
                        location_elem = listing.find('div', class_='location')
                        description_elem = listing.find('div', class_='description-preview')
                        link_elem = listing.find('a', class_='listing-link')
                        
                        if title_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip() if company_elem else "Not specified"
                            location = location_elem.text.strip() if location_elem else "Not specified"
                            description = description_elem.text.strip() if description_elem else "No description available"
                            job_url = link_elem['href'] if link_elem and link_elem.has_attr('href') else "No link available"
                            
                            self.internships.append({
                                'title': title,
                                'company': company,
                                'location': location,
                                'description': description,
                                'url': job_url,
                                'source': 'InternshipFinder'
                            })
                    except Exception as e:
                        print(f"Error parsing InternshipFinder listing: {e}")
                
                time.sleep(random.uniform(2, 4))
            else:
                print(f"Failed to retrieve InternshipFinder page {page}: {response.status_code}")
                
    def categorize_internships(self):
        """Categorize internships based on title and description keywords"""
        for internship in self.internships:
            internship_text = f"{internship['title']} {internship['description']}".lower()
            
            # Default category
            category = 'Other'
            
            # Check for keywords in each category
            for cat_name, keywords in self.categories.items():
                if any(keyword.lower() in internship_text for keyword in keywords):
                    category = cat_name
                    break
            
            # Add category to the internship data
            internship['category'] = category
                
    def run_scraper(self, target_count=100):
        """Run all scrapers until we get the target number of internships"""
        self.scrape_indeed(8)
        
        if len(self.internships) < target_count:
            self.scrape_linkedin(8)
            
        if len(self.internships) < target_count:
            self.scrape_chegg(4)
            
        if len(self.internships) < target_count:
            self.scrape_wayup(4)
            
        if len(self.internships) < target_count:
            self.scrape_lumiere(3)
            
        if len(self.internships) < target_count:
            self.scrape_findecs(3)
            
        if len(self.internships) < target_count:
            self.scrape_internship_finder(3)
            
        # Remove duplicates based on title and company
        unique_internships = []
        seen = set()
        
        for internship in self.internships:
            key = (internship['title'], internship['company'])
            if key not in seen:
                seen.add(key)
                unique_internships.append(internship)
        
        self.internships = unique_internships[:target_count]
        
        # Categorize internships
        self.categorize_internships()
        
        return self.internships
    
    def save_to_csv(self, filename=None):
        """Save internships to a CSV file"""
        if not filename:
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"high_school_internships_{current_date}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'company', 'location', 'description', 'url', 'source', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for internship in self.internships:
                writer.writerow(internship)
        
        print(f"Saved {len(self.internships)} internships to {filename}")
    
    def save_categorized_csv(self):
        """Save internships to multiple CSV files by category"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Group internships by category
        categorized = {}
        for internship in self.internships:
            category = internship['category']
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(internship)
        
        # Save a file for each category
        for category, internships in categorized.items():
            filename = f"internships_{category.lower().replace(' & ', '_').replace(' ', '_')}_{current_date}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['title', 'company', 'location', 'description', 'url', 'source', 'category']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for internship in internships:
                    writer.writerow(internship)
            
            print(f"Saved {len(internships)} {category} internships to {filename}")
        
    def print_internships(self):
        """Print internships to console"""
        for i, internship in enumerate(self.internships, 1):
            print(f"\n--- Internship #{i} ---")
            print(f"Title: {internship['title']}")
            print(f"Company: {internship['company']}")
            print(f"Location: {internship['location']}")
            print(f"Category: {internship['category']}")
            print(f"Source: {internship['source']}")
            print(f"URL: {internship['url']}")
            print("-" * 50)
            
    def print_by_category(self):
        """Print summary of internships by category"""
        # Group and count internships by category
        category_counts = {}
        for internship in self.internships:
            category = internship['category']
            if category not in category_counts:
                category_counts[category] = 0
            category_counts[category] += 1
        
        # Print summary
        print("\n=== Internships by Category ===")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{category}: {count} internships")
        print("=" * 30)

# Run the scraper
if __name__ == "__main__":
    scraper = InternshipScraper()
    internships = scraper.run_scraper(target_count=100)
    
    # Save all internships to a single CSV
    scraper.save_to_csv()
    
    # Save internships by category to separate CSVs
    scraper.save_categorized_csv()
    
    print(f"\nFound {len(internships)} high school summer internship opportunities.")
    
    # Print summary by category
    scraper.print_by_category()
    
    # Print a preview from each category
    print("\n=== Preview of Internships by Category ===")
    
    # Group internships by category
    by_category = {}
    for internship in internships:
        category = internship['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(internship)
    
    # Print previews for each category
    for category, category_internships in sorted(by_category.items()):
        print(f"\n--- {category} Internships ---")
        preview_count = min(3, len(category_internships))
        for i in range(preview_count):
            internship = category_internships[i]
            print(f"{i+1}. {internship['title']} at {internship['company']} ({internship['location']})")
            print(f"   Source: {internship['source']} | URL: {internship['url']}")
        
        # Show how many more are available in this category
        if len(category_internships) > 3:
            print(f"   ... and {len(category_internships) - 3} more {category} internships")
    
    print("\nAll internships have been saved to CSV files by category.")