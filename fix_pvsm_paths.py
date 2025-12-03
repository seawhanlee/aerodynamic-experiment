#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from pathlib import Path
import os
import sys

def find_project_root():
    """현재 스크립트의 위치에서 프로젝트 루트 찾기"""
    # 이 스크립트가 프로젝트 루트에 있다고 가정
    script_dir = Path(__file__).parent.resolve()
    return script_dir

# 프로젝트 루트를 동적으로 찾기
root_dir = find_project_root()

print(f"Project root: {root_dir}")
print(f"Platform: {sys.platform}")
print()

# 모든 .pvsm 파일 찾기
pvsm_files = list(root_dir.glob("**/*.pvsm"))

print(f"Total .pvsm files: {len(pvsm_files)}")

for pvsm_file in pvsm_files:
    try:
        # XML 파일 파싱
        tree = ET.parse(pvsm_file)
        root = tree.getroot()
        
        changed = False
        
        # 모든 Element 요소 찾기
        for elem in root.iter('Element'):
            if 'value' in elem.attrib:
                value = elem.attrib['value']
                # .vtu 파일이면 절대 경로로 변환
                if value.endswith('.vtu'):
                    # "./" 제거
                    if value.startswith('./'):
                        value = value[2:]
                    
                    # 상대 경로면 절대 경로로 변환
                    if not value.startswith('/') and not (len(value) > 1 and value[1] == ':'):  # Unix와 Windows 절대 경로 체크
                        vtu_path = pvsm_file.parent / value
                        vtu_path = vtu_path.resolve()  # 절대 경로로 변환
                        elem.attrib['value'] = str(vtu_path)
                        changed = True
        
        if changed:
            # XML 파일 저장
            tree.write(pvsm_file, encoding='utf-8', xml_declaration=True)
            print(f"✓ Fixed: {pvsm_file.relative_to(root_dir)}")
        else:
            print(f"  No changes: {pvsm_file.relative_to(root_dir)}")
    except Exception as e:
        print(f"✗ Error processing {pvsm_file.relative_to(root_dir)}: {e}")

print("Done!")
