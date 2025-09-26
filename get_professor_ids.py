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
    """Save professor data to CSV file (overwrites existing file)"""
    if not professors:
        print("❌ No professor data to save")
        return False
    
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
        return True
        
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")
        return False

def save_name_to_id_mapping(professors, filename="professor_name_to_id.csv"):
    """Save a simplified mapping of professor names to IDs (overwrites existing file)"""
    if not professors:
        print("❌ No professor data to save")
        return False
    
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
        return True
        
    except Exception as e:
        print(f"❌ Error saving name mapping: {e}")
        return False

def fetch_detailed_professor_data(professor_id):
    """Fetch detailed professor data including reviews from the PolyRatings API"""
    api_url = f"https://api-prod.polyratings.org/professors.get?input=%7B%22id%22%3A%22{professor_id}%22%7D"
    
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        professor_data = data.get('result', {}).get('data', {})
        
        return professor_data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching detailed data for professor {professor_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON for professor {professor_id}: {e}")
        return None

def save_detailed_professor_reviews(professors, main_filename="data/main/professor_detailed_reviews.csv", tracking_filename=None):
    """Save detailed professor reviews to CSV files (tracking first, then main for safety)"""
    if not professors:
        print("❌ No professor data to save")
        return False
    
    # Define CSV headers for detailed reviews
    headers = [
        'professor_id',
        'professor_name',
        'professor_department',
        'course_code',
        'review_id',
        'grade',
        'grade_level',
        'course_type',
        'overall_rating',
        'presents_material_clearly',
        'recognizes_student_difficulties',
        'rating_text',
        'post_date'
    ]
    
    # First, save to tracking file
    tracking_success = False
    if tracking_filename:
        try:
            print(f"🔄 Saving to tracking file: {tracking_filename}")
            with open(tracking_filename, 'w', newline='', encoding='utf-8') as tracking_file:
                tracking_writer = csv.DictWriter(tracking_file, fieldnames=headers)
                tracking_writer.writeheader()
                
                total_reviews = 0
                
                for prof in professors:
                    prof_id = prof.get('id', '')
                    prof_name = f"{prof.get('firstName', '')} {prof.get('lastName', '')}".strip()
                    prof_dept = prof.get('department', '')
                    
                    print(f"🔄 Fetching detailed data for {prof_name}...")
                    
                    # Fetch detailed data for this professor
                    detailed_data = fetch_detailed_professor_data(prof_id)
                    
                    if detailed_data and 'reviews' in detailed_data:
                        reviews = detailed_data.get('reviews', {})
                        
                        # Process reviews for each course
                        for course_code, course_reviews in reviews.items():
                            if isinstance(course_reviews, list):
                                for review in course_reviews:
                                    # Create row data for each review
                                    row = {
                                        'professor_id': prof_id,
                                        'professor_name': prof_name,
                                        'professor_department': prof_dept,
                                        'course_code': course_code,
                                        'review_id': review.get('id', ''),
                                        'grade': review.get('grade', ''),
                                        'grade_level': review.get('gradeLevel', ''),
                                        'course_type': review.get('courseType', ''),
                                        'overall_rating': review.get('overallRating', 0),
                                        'presents_material_clearly': review.get('presentsMaterialClearly', 0),
                                        'recognizes_student_difficulties': review.get('recognizesStudentDifficulties', 0),
                                        'rating_text': review.get('rating', ''),
                                        'post_date': review.get('postDate', '')
                                    }
                                    
                                    tracking_writer.writerow(row)
                                    total_reviews += 1
                    
                    # Add a small delay to be respectful to the API
                    import time
                    time.sleep(0.1)
                
                print(f"✅ Tracking file saved successfully: {tracking_filename}")
                print(f"📊 Total reviews collected: {total_reviews}")
                tracking_success = True
                
        except Exception as e:
            print(f"❌ Error saving to tracking file: {e}")
            return False
    
    # Only update main file if tracking was successful
    if tracking_success and main_filename:
        try:
            print(f"🔄 Copying tracking data to main file: {main_filename}")
            import shutil
            shutil.copy2(tracking_filename, main_filename)
            print(f"✅ Main file updated successfully: {main_filename}")
            return True
        except Exception as e:
            print(f"❌ Error copying to main file: {e}")
            print("⚠️  Tracking file is safe, but main file update failed")
            return False
    
    return tracking_success

def save_department_summary(professors, filename="department_summary.csv"):
    """Save department-level summary statistics (overwrites existing file)"""
    if not professors:
        print("❌ No professor data to save")
        return False
    
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
        return True
        
    except Exception as e:
        print(f"❌ Error saving department summary: {e}")
        return False

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
        
        # Save timestamped files to tracking folder first (safe approach)
        print("\n📁 Saving timestamped files to data/tracking/...")
        tracking_success = True
        
        # Save basic data to tracking
        if not save_to_csv(professors, f"data/tracking/professors_full_data_{timestamp}.csv"):
            tracking_success = False
        if not save_name_to_id_mapping(professors, f"data/tracking/professor_name_to_id_{timestamp}.csv"):
            tracking_success = False
        if not save_department_summary(professors, f"data/tracking/department_summary_{timestamp}.csv"):
            tracking_success = False
        
        # Fetch and save detailed professor reviews to tracking
        print("\n📁 Fetching detailed professor reviews...")
        print("⚠️  This may take a while as we fetch individual professor data...")
        detailed_success = save_detailed_professor_reviews(
            professors, 
            main_filename=None,  # Don't update main yet
            tracking_filename=f"data/tracking/professor_detailed_reviews_{timestamp}.csv"
        )
        
        # Only update main files if tracking was successful
        if tracking_success and detailed_success:
            print("\n📁 Updating main files from successful tracking data...")
            import shutil
            
            # Copy tracking files to main (safe copy operation)
            try:
                shutil.copy2(f"data/tracking/professors_full_data_{timestamp}.csv", "data/main/professors_data.csv")
                shutil.copy2(f"data/tracking/professor_name_to_id_{timestamp}.csv", "data/main/professor_name_to_id.csv")
                shutil.copy2(f"data/tracking/department_summary_{timestamp}.csv", "data/main/department_summary.csv")
                shutil.copy2(f"data/tracking/professor_detailed_reviews_{timestamp}.csv", "data/main/professor_detailed_reviews.csv")
                print("✅ All main files updated successfully from tracking data")
            except Exception as e:
                print(f"❌ Error copying tracking files to main: {e}")
                print("⚠️  Tracking files are safe, but main files may be outdated")
        else:
            print("⚠️  Skipping main file updates due to tracking failures")
        
        print("\n📁 Files created:")
        print("  📂 data/main/")
        print("    • professors_data.csv - Full professor data")
        print("    • professor_name_to_id.csv - Name to ID mapping")
        print("    • department_summary.csv - Department statistics")
        print("    • professor_detailed_reviews.csv - Detailed student reviews")
        print("  📂 data/tracking/")
        print(f"    • professors_full_data_{timestamp}.csv")
        print(f"    • professor_name_to_id_{timestamp}.csv")
        print(f"    • department_summary_{timestamp}.csv")
        print(f"    • professor_detailed_reviews_{timestamp}.csv")
        
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
