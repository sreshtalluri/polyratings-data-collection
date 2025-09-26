"""
PolyRatings Professor Data Fetcher
Fetches professor data from the API and saves to CSV
"""

import requests
import csv
import json
from datetime import datetime
import os

def create_data_directories():
    """Create necessary directories for organizing data"""
    directories = [
        'data',
        'data/main',
        'data/tracking'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
    
    return directories

def fetch_professor_data():
    """Fetch professor data from the PolyRatings API"""
    api_url = "https://api-prod.polyratings.org/professors.all"
    
    try:
        print("🔄 Fetching professor data from API...")
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        professors = data.get('result', {}).get('data', [])
        
        print(f"✅ Successfully fetched {len(professors)} professors")
        return professors
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return None

def save_to_csv(professors, filename="professors_data.csv"):
    """Save professor data to CSV file"""
    if not professors:
        print("❌ No professor data to save")
        return
    
    # Define CSV headers
    headers = [
        'id',
        'firstName', 
        'lastName',
        'fullName',
        'department',
        'numEvals',
        'overallRating',
        'materialClear',
        'studentDifficulties',
        'courses',
        'tags',
        'courses_count',
        'tags_count'
    ]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            for prof in professors:
                # Create full name
                full_name = f"{prof.get('firstName', '')} {prof.get('lastName', '')}".strip()
                
                # Process courses list
                courses = prof.get('courses', [])
                courses_str = '; '.join(courses) if courses else ''
                courses_count = len(courses)
                
                # Process tags
                tags = prof.get('tags', {})
                tags_str = '; '.join([f"{k}:{v}" for k, v in tags.items()]) if tags else ''
                tags_count = len(tags)
                
                # Create row data
                row = {
                    'id': prof.get('id', ''),
                    'firstName': prof.get('firstName', ''),
                    'lastName': prof.get('lastName', ''),
                    'fullName': full_name,
                    'department': prof.get('department', ''),
                    'numEvals': prof.get('numEvals', 0),
                    'overallRating': prof.get('overallRating', 0),
                    'materialClear': prof.get('materialClear', 0),
                    'studentDifficulties': prof.get('studentDifficulties', 0),
                    'courses': courses_str,
                    'tags': tags_str,
                    'courses_count': courses_count,
                    'tags_count': tags_count
                }
                
                writer.writerow(row)
        
        print(f"✅ Data saved to {filename}")
        print(f"📊 Total professors: {len(professors)}")
        
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")

def save_name_to_id_mapping(professors, filename="professor_name_to_id.csv"):
    """Save a simplified mapping of professor names to IDs"""
    if not professors:
        print("❌ No professor data to save")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['fullName', 'firstName', 'lastName', 'id', 'department', 'overallRating', 'numEvals'])
            
            for prof in professors:
                full_name = f"{prof.get('firstName', '')} {prof.get('lastName', '')}".strip()
                writer.writerow([
                    full_name,
                    prof.get('firstName', ''),
                    prof.get('lastName', ''),
                    prof.get('id', ''),
                    prof.get('department', ''),
                    prof.get('overallRating', 0),
                    prof.get('numEvals', 0)
                ])
        
        print(f"✅ Name-to-ID mapping saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error saving name mapping: {e}")

def save_department_summary(professors, filename="department_summary.csv"):
    """Save department-level summary statistics"""
    if not professors:
        print("❌ No professor data to save")
        return
    
    # Group by department
    dept_stats = {}
    
    for prof in professors:
        dept = prof.get('department', 'Unknown')
        if dept not in dept_stats:
            dept_stats[dept] = {
                'count': 0,
                'total_rating': 0,
                'total_evals': 0,
                'professors': []
            }
        
        dept_stats[dept]['count'] += 1
        dept_stats[dept]['total_rating'] += prof.get('overallRating', 0)
        dept_stats[dept]['total_evals'] += prof.get('numEvals', 0)
        dept_stats[dept]['professors'].append(prof.get('id', ''))
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['department', 'professor_count', 'avg_rating', 'total_evals', 'professor_ids'])
            
            for dept, stats in dept_stats.items():
                avg_rating = stats['total_rating'] / stats['count'] if stats['count'] > 0 else 0
                professor_ids = '; '.join(stats['professors'])
                
                writer.writerow([
                    dept,
                    stats['count'],
                    round(avg_rating, 2),
                    stats['total_evals'],
                    professor_ids
                ])
        
        print(f"✅ Department summary saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error saving department summary: {e}")

def main():
    """Main function to fetch and save professor data"""
    print("🚀 PolyRatings Professor Data Fetcher")
    print("=" * 50)
    
    # Create data directories
    create_data_directories()
    
    # Fetch data
    professors = fetch_professor_data()
    
    if professors:
        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save timestamped files to tracking folder
        print("\n📁 Saving timestamped files to data/tracking/...")
        save_to_csv(professors, f"data/tracking/professors_full_data_{timestamp}.csv")
        save_name_to_id_mapping(professors, f"data/tracking/professor_name_to_id_{timestamp}.csv")
        save_department_summary(professors, f"data/tracking/department_summary_{timestamp}.csv")
        
        # Save main files to data/main folder
        print("\n📁 Saving main files to data/main/...")
        save_to_csv(professors, "data/main/professors_data.csv")
        save_name_to_id_mapping(professors, "data/main/professor_name_to_id.csv")
        save_department_summary(professors, "data/main/department_summary.csv")
        
        print("\n📁 Files created:")
        print("  📂 data/main/")
        print("    • professors_data.csv - Full professor data")
        print("    • professor_name_to_id.csv - Name to ID mapping")
        print("    • department_summary.csv - Department statistics")
        print("  📂 data/tracking/")
        print(f"    • professors_full_data_{timestamp}.csv")
        print(f"    • professor_name_to_id_{timestamp}.csv")
        print(f"    • department_summary_{timestamp}.csv")
        
        # Show some sample data
        print(f"\n📊 Sample data (first 3 professors):")
        for i, prof in enumerate(professors[:3]):
            name = f"{prof.get('firstName', '')} {prof.get('lastName', '')}".strip()
            dept = prof.get('department', '')
            rating = prof.get('overallRating', 0)
            evals = prof.get('numEvals', 0)
            print(f"  {i+1}. {name} ({dept}) - Rating: {rating}, Evals: {evals}")
    
    else:
        print("❌ Failed to fetch professor data")

if __name__ == "__main__":
    main()
