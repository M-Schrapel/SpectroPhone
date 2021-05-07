import csv

"""
    reads the CSV information from the given path
"""
def read_CSV (filepath):
    
    sequence = []
    with open(filepath, 'r') as csvFile:
        reader = csv.reader(csvFile, 'excel')
        for row in reader:
            sequence.append(row)
    return sequence

"""
    writes the given sequence as a CSV file to the given path
"""
def write_CSV (sequence, filepath):

    with open(filepath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, 'excel')
        for i in range(len(sequence)):
            writer.writerow(sequence[i])
            
"""
    writes the given image data as a CSV file to the given path
"""
def writeImageData (imageData, filepath):

    with open(filepath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, 'excel')
        writer.writerow(imageData)
    
