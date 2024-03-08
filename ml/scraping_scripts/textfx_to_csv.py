import csv

def process_section(lines):
    """Processes a section of data from the text file"""
    section = None
    input_text = None
    outputs = []
    flag = False

    for line in lines:
        line = line.strip()

        if flag:
            input_text = line

        if line.startswith("======="):
            section = line.strip("=").strip()
        elif line.startswith("INPUT:"):
            flag = True
            continue
        elif line.startswith("•"):
            outputs.append(line[1:].strip())

        flag = False

    return section, input_text, outputs


def main():
    """Reads the text file and creates the CSV"""
    with open('outputs.txt', 'r') as infile, \
         open('output.csv', 'w', newline='') as outfile:

        writer = csv.DictWriter(outfile, fieldnames=['input', 'output'])
        writer.writeheader()

        prev_input = None

        lines = []
        for line in infile:
            if line.strip():  # If the line is not empty
                lines.append(line)
            else:  # If line is empty, we've reached the end of a section
                if lines:  # Process only if we have collected some lines
                    section, input_text, outputs = process_section(lines)

                    if not input_text:
                        input_text = prev_input
                    prev_input = input_text

                    for output in outputs:
                        writer.writerow({'input': input_text, 'output': output})
                    lines = []  # Reset lines for the next section


if __name__ == "__main__":
    main()
