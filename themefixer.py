"""
1. Unpack given as argument zip from current directory to temporary folder
2. Open theme.xml inside temporary folder
3. Find "format" tag and change its value to 2.3.1.0.
4. Find "ratios" section and replace it to the end
5. Save xml
6. Pack whole folder back to new zip with postfix --fixed
7. Clean the tmp directory
"""
import argparse, zipfile, os, shutil
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description="Fix the 2.4.x ThemeEditor output themes problem. Just point to the broken archive")
parser.add_argument('theme_file', type=str, help="Theme filename like \'Theme.zip\'")
args = parser.parse_args()
#Checking .zip extensions is included in the arg. If it is then passing the string without it
THEME_ARCHIVE_NAME = args.theme_file if ".zip" not in args.theme_file else args.theme_file[:len(args.theme_file)-4]

#Unpack archive into temp directory
print("Unpacking and fixing...")
with zipfile.ZipFile(THEME_ARCHIVE_NAME+'.zip', 'r') as zip_ref:
    zip_ref.extractall('./'+THEME_ARCHIVE_NAME)

#Open and parse theme.xml
tree = ET.parse(THEME_ARCHIVE_NAME+'/theme.xml')
root = tree.getroot()
#Find and change the format
for tag in root:
    if tag.tag=='format':
        tag.text = '2.3.1.0'
        break
#Find and remove ratios and storing its value to the 'ratios' variable
for tag in root:
    if tag.tag=='ratios':
        ratios = tag
        root.remove(tag)
        break
#Appending 'ratios' to the end
root.append(ratios)
#Save the edited xml file
tree.write(THEME_ARCHIVE_NAME+'/theme.xml')

#Zip temp file into archive
length = len(THEME_ARCHIVE_NAME)
with zipfile.ZipFile(THEME_ARCHIVE_NAME+'_fixed.zip', 'w') as zip_ref:
    for root, dirs, files in os.walk(THEME_ARCHIVE_NAME):
        folder = root[length:]
        for file in files:
            zip_ref.write(os.path.join(root, file), os.path.join(folder, file))

#Remove the tmp directory
shutil.rmtree('./'+THEME_ARCHIVE_NAME)
