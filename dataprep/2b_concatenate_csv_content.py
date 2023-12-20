import csv

def segment_content(content, segment_length=800, overlap=80):
    words = content.split()
    for i in range(0, len(words), segment_length - overlap):
        yield ' '.join(words[i:i + segment_length])

def process_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['URL', 'Content'])

        for row in reader:
            url = row['URL']
            last_section = url.rstrip('/').split('/')[-1]
            content = row['Content']
            for segment in segment_content(content):
                writer.writerow([url, f"{last_section} {segment}"])

input_csv = 'scraped_content.csv'  # Replace with your input file name
output_csv = 'concatenated_content.csv'  # The name of the new output CSV file

process_csv(input_csv, output_csv)

print("CSV processing complete.")
