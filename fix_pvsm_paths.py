#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from pathlib import Path
import os
import sys

def find_project_root():
    """Find project root relative to this script"""
    script_dir = Path(__file__).parent.resolve()
    return script_dir

def fix_paths():
    root_dir = find_project_root()
    print(f"Project root: {root_dir}")
    
    # Find all .pvsm files
    pvsm_files = list(root_dir.glob("**/*.pvsm"))
    print(f"Found {len(pvsm_files)} .pvsm files.")

    for pvsm_file in pvsm_files:
        try:
            tree = ET.parse(pvsm_file)
            root = tree.getroot()
            changed = False
            
            pvsm_dir = pvsm_file.parent

            # Iterate over all Element tags
            for elem in root.iter('Element'):
                if 'value' in elem.attrib:
                    value = elem.attrib['value']
                    # We are looking for .vtu paths
                    if value.endswith('.vtu'):
                        # Check if we can make it relative to the pvsm file
                        filename = os.path.basename(value)
                        
                        # Check if the file exists in the same directory as the pvsm file
                        local_vtu = pvsm_dir / filename
                        
                        if local_vtu.exists():
                            # If the file exists locally, use the relative path (just filename)
                            if value != filename:
                                print(f"  Fixing path in {pvsm_file.name}:")
                                print(f"    Old: {value}")
                                print(f"    New: {filename}")
                                elem.attrib['value'] = filename
                                changed = True
                        else:
                            # If not found locally, warn the user (optional)
                            # print(f"  Warning: Referenced file {filename} not found in {pvsm_dir}")
                            pass

            if changed:
                tree.write(pvsm_file, encoding='utf-8', xml_declaration=True)
                print(f"✓ Saved updates to: {pvsm_file.relative_to(root_dir)}")
            else:
                print(f"  No changes needed for: {pvsm_file.relative_to(root_dir)}")

        except Exception as e:
            print(f"✗ Error processing {pvsm_file.name}: {e}")

if __name__ == "__main__":
    fix_paths()
