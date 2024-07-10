import xml.etree.ElementTree as ET
import csv

# Define the XML file path
xml_file_path = 'test.qlp.sol'  # Replace with the actual path to your XML file
csv_file_path = 'solution.csv'  # Output CSV file path

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write the header row
    csvwriter.writerow(['Variable', 'Value'])
    
    # Iterate through each variable in the XML and write to the CSV
    for variable in root.find('variables'):
        name = variable.get('name')
        value = variable.get('value')
        csvwriter.writerow([name, value])

print(f"Data has been successfully written to {csv_file_path}")