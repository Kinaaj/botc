import os
import sys
import csv
import re

# Pomocná funkce pro vytvoření klíčového slova
# Převede na malá písmena a odstraní vše, co není znak a-z (včetně mezer)
def make_keyword(text):
    return re.sub(r'[^a-z]', '', text.lower())

def generate_tokens(set_num):
    template_path = 'Templates/RoleTokenLaserTemplate.svg'
    csv_path = 'Encyklopedie - Role.csv'
    sets_dir = 'Sets'

    # Find the full set directory name starting with the number
    try:
        set_name = next((d for d in os.listdir(sets_dir) if d.startswith(set_num + '_')), None)
    except FileNotFoundError:
        print(f"Error: {sets_dir} directory not found.")
        return

    if not set_name:
        print(f"Error: Set starting with '{set_num}_' not found in {sets_dir}.")
        return

    icon_dir = os.path.join(sets_dir, set_name, 'RoleIconPNG')
    output_dir = os.path.join(sets_dir, set_name, 'RoleTokenLaser')
    
    if not os.path.exists(icon_dir):
        print(f"Error: Icon directory {icon_dir} does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Load template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Load role mapping from CSV - NYNÍ POUŽÍVÁ KEYWORD
    role_mapping = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Přečte sloupec 'keyword' a pro jistotu ho prožene čistící funkcí
            csv_keyword = make_keyword(row['keyword'])
            cz_name = row['name_cz'].strip()
            # Do slovníku se nyní ukládá jako klíč očištěný tvar (např. 'imp')
            role_mapping[csv_keyword] = cz_name

    icons = [f for f in os.listdir(icon_dir) if f.endswith('.png')]
    count = 0
    skipped = 0
    
    for icon_file in icons:
        full_name_no_ext = os.path.splitext(icon_file)[0]
        
        # Extract base name and suffix (e.g., 'Imp0' -> 'Imp', '0')
        match = re.search(r'(\d+)$', full_name_no_ext)
        if match:
            eng_base_name = full_name_no_ext[:match.start()].strip()
            suffix = match.group(1)
        else:
            eng_base_name = full_name_no_ext.strip()
            suffix = ''
            
        # Očistíme název z ikony na náš formát keyword (např. 'Imp' -> 'imp')
        search_keyword = make_keyword(eng_base_name)
        cz_base_name = role_mapping.get(search_keyword)
        
        # Fallback for exact match if suffix parsing didn't match anything in CSV
        if not cz_base_name:
            fallback_keyword = make_keyword(full_name_no_ext)
            cz_base_name = role_mapping.get(fallback_keyword)
            if cz_base_name:
                suffix = ''

        if cz_base_name:
            # Construct filename: [CZ_NAME_NO_SPACES][SUFFIX]RoleTokenLaser.svg
            safe_cz_base = cz_base_name.replace(' ', '')
            filename = f'{safe_cz_base}{suffix}RoleTokenLaser.svg'
            output_path = os.path.join(output_dir, filename)

            # Skip if file already exists
            if os.path.exists(output_path):
                skipped += 1
                continue

            # Generate SVG content
            display_name = cz_base_name
            new_content = template_content.replace('Byrokrat', display_name)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
        else:
            # Upravený výpis varování pro lepší debugging
            print(f"Warning: No translation found for '{full_name_no_ext}', tried searching keyword '{search_keyword}'")

    print(f"Successfully generated {count} tokens, skipped {skipped} existing tokens in {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_role_tokens.py [SET_NUMBER] (e.g., 06)")
    else:
        generate_tokens(sys.argv[1])