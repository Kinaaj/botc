import csv
import os
import shutil
import re

def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def main():
    # Load role translations
    role_map = {} # normalized_name -> name_cz
    with open('Encyklopedie - Role.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            norm_eng = normalize(row['name_eng'])
            norm_kw = normalize(row['keyword'])
            role_map[norm_eng] = row['name_cz']
            role_map[norm_kw] = row['name_cz']

    # Load keyword mapping
    kw_map = {} # english_keyword -> (czech_translation, template_file)
    with open('reminder_keywords_mapping.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw_map[row['english_keyword'].lower()] = (row['czech_translation'], row['template_file'])

    sets = ['08_Experimental', '09_Experimental', '10_Experimental']
    
    for set_name in sets:
        icon_dir = f'Sets/{set_name}/ReminderIconPNG'
        output_dir = f'Sets/{set_name}/ReminderTokenLaser'
        
        if not os.path.exists(icon_dir):
            print(f"Directory {icon_dir} does not exist. Skipping.")
            continue
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        files = os.listdir(icon_dir)
        for filename in files:
            if not filename.endswith('.png'):
                continue
                
            basename = filename[:-4] # remove .png
            
            # Try to split basename into Role and Keyword
            # Since role names and keywords can vary, we try to find the longest role name match at the start
            found_role = None
            found_role_cz = None
            found_kw_eng = None
            
            # Sort roles by length descending to match longest first
            sorted_roles = sorted(role_map.keys(), key=len, reverse=True)
            
            low_basename = basename.lower()
            for role_norm in sorted_roles:
                if low_basename.startswith(role_norm):
                    found_role = role_norm
                    found_role_cz = role_map[role_norm]
                    found_kw_eng = basename[len(role_norm):]
                    # Check if the rest is actually a keyword or a number
                    break
            
            if not found_role:
                print(f"Could not find role for {filename}")
                continue

            # Handle keyword and numbers
            # Try full keyword match first
            full_kw_eng = found_kw_eng.lower()
            kw_data = kw_map.get(full_kw_eng)
            
            if kw_data:
                kw_cz, template = kw_data
                kw_pure = found_kw_eng
                kw_num = ''
            else:
                # Split into alpha and numeric
                kw_match = re.match(r'([a-zA-Z]+)([0-9]*)', found_kw_eng)
                if kw_match:
                    kw_pure = kw_match.group(1)
                    kw_num = kw_match.group(2)
                else:
                    kw_pure = found_kw_eng
                    kw_num = ''
                
                kw_data = kw_map.get(kw_pure.lower())
            
            if kw_data:
                kw_cz, template = kw_data
                if kw_cz.startswith('XXX'):
                    # Prompt says: XXX[RoleCzechName][KeywordEnglishName]ReminderTokenLaser.svg
                    new_filename = f"XXX{found_role_cz}{found_kw_eng}ReminderTokenLaser.svg"
                    template = "ReminderTokenLaser.svg"
                else:
                    new_filename = f"{found_role_cz}{kw_cz}{kw_num}ReminderTokenLaser.svg"
            else:
                # Fallback if keyword not in mapping
                print(f"Keyword '{found_kw_eng}' not found in mapping for {filename}. Using default.")
                new_filename = f"XXX{found_role_cz}{found_kw_eng}ReminderTokenLaser.svg"
                template = "ReminderTokenLaser.svg"

            src_template = f"Templates/ReminderTokenTemplates/{template}"
            dest_path = f"{output_dir}/{new_filename}"
            
            if os.path.exists(src_template):
                shutil.copy(src_template, dest_path)
                print(f"Generated: {dest_path}")
            else:
                print(f"Template {src_template} not found for {filename}")

if __name__ == "__main__":
    main()
