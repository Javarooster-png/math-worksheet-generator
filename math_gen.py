import random
from fpdf import FPDF
import argparse

class Worksheet(FPDF):
    def __init__(self, operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operator = operator

    def header(self):
        # Title and header section
        self.set_font("Arial", '', 12)
        self.cell(0, 10, 'Name: ________________________', ln=True, align='L')
        self.cell(0, 10, 'Date: _________________________', ln=True, align='L')
        self.ln(5)
        self.set_font("Arial", 'B', 18)
        title = "Subtraction" if self.operator == '-' else "Addition" if self.operator == '+' else "Division" if self.operator == '/' else "Multiplication"
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(5)
        self.set_line_width(0.5)
        self.line(10, 48, 200, 48)  # Correct placement of the line
        self.ln(10)

    def footer(self):
        # Footer section
        self.set_y(-15)
        self.set_font("Arial", 'I', 10)
        self.cell(0, 20, 'AJ Otto', 0, 0, 'C')

    def add_problem(self, top_num, bottom_num, x_offset, y_offset):
        if self.operator == '-' or '+' or 'x':
            if top_num < bottom_num:
                top_num, bottom_num = bottom_num, top_num
        #elif self.operator == '/':
            # Ensure that top_num is divisible by bottom_num with no remainder
            #top_num = bottom_num * random.randint(1, 10)

        self.set_xy(x_offset, y_offset)  # Set the position for the current problem

        problem_width = 25  # Width allocated for each problem
        
        # Top number
        self.set_font("Arial", '', 16)
        self.cell(problem_width, 10, f"{top_num}", align='R')
        self.ln(7)

        # Operator sign and bottom number, aligned properly
        self.set_x(x_offset)
        self.cell(5, 10, self.operator, align='L')
        self.cell(problem_width - 5, 10, f"{bottom_num}", align='R')
        self.ln(5)

        # Draw the line beneath the numbers
        self.set_x(x_offset)
        self.cell(problem_width, 5, '', align='R')
        self.line(x_offset, self.get_y() + 4, x_offset + problem_width, self.get_y() + 4)  # Lower the line slightly
        self.ln(15)  # Add space after the problem for clarity

    def add_problem_row(self, num_problems):
        start_x = self.get_x()
        start_y = self.get_y()
        
        for i in range(num_problems):
            x_offset = start_x + (i * 45)  # Adjust horizontal spacing
            bottom_num = random.randint(*bottom_range)
            top_num = random.randint(*top_range)
            #top_num = bottom_num * random.randint(1, 10)  # Ensure a perfect division
            self.add_problem(top_num, bottom_num, x_offset, start_y)
        
        self.set_y(start_y + 30)  # Move to the next row

# Customizable range for the numbers
top_range = (0, 10)  # Start from 1 to avoid division by zero
bottom_range = (0, 10)

def main():
    parser = argparse.ArgumentParser(description="Generate a worksheet.")
    parser.add_argument('--sub', action='store_true', help="Generate subtraction worksheet instead of multiplication.")
    parser.add_argument('--add', action='store_true', help="Generate addition worksheet instead of multiplication.")
    parser.add_argument('--div', action='store_true', help="Generate division worksheet instead of multiplication.")
    args = parser.parse_args()

    if args.sub:
        operator = '-'
    elif args.add:
        operator = '+'
    elif args.div:
        operator = '/'
    else:
        operator = 'x'

    # Generate and save five different worksheets
    for i in range(1, 6):  # Loop from 1 to 5
        pdf = Worksheet(operator)
        pdf.add_page()

        # Generate the worksheet in rows
        for _ in range(7):  # 7 rows
            pdf.add_problem_row(4)  # 4 problems per row

        # Save the PDF with a unique filename
        filename = f"{'subtraction' if operator == '-' else 'addition' if operator == '+' else 'division' if operator == '/' else 'multiplication'}_worksheet_{i}.pdf"
        pdf.output(filename)
        print(f"Saved: {filename}")

if __name__ == "__main__":
    main()
