from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
import pymupdf as fitz
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import re
from model_inference import Inference
from fs import open_fs
import os
import socket

class Parser:
	def __init__(self, filestream):
		self.filestream = filestream
		self.vendor = None
		self.issue_date = None
		self.items = [] 
		self.total = None
		self.due_date = None 
		self.painted_string = None
		self.prompt = None
		self.page_height = None
		self.page_width = None
		self.response = None
		self.text_df = None
		self.llm = Inference("unsloth/llama-3-8b-Instruct-bnb-4bit")

	def extract_text_pdf(self):
		doc = fitz.open(stream=self.filestream, filetype='pdf')
		self.page_width = doc[0].rect.width
		self.page_height = doc[0].rect.height
		list_of_elements = []
		for page_number, page in enumerate(doc):
			text_instances = page.get_text("dict")['blocks']
			for block in text_instances:
				block_data = {
					'page_number': page_number + 1,
					'bbox': block['bbox'],  # Bounding box of the block
					'block_type': block['type'],  # Type of the block (e.g., text, image)
				}

				if block['type'] == 0:  # type 0 is text
					block_data['lines'] = []
					for line in block['lines']:
						line_data = {
							'bbox': line['bbox'],
							'spans': []
						}
						for span in line['spans']:
							span_data = {
								'text': span['text']
							}
							line_data['spans'].append(span_data)
						list_of_elements.append((line['bbox'], span_data['text']))
				
		texts = pd.DataFrame(list_of_elements, columns=['bbox', 'text'])
		return texts

	def normalize_bbox(self, df, page_width):
		df['x0'], df['x1'], df['y0'], df['y1'] = df['y1'], df['y0'], df['x1'], df['x0']
		df['x0'], df['x1'] = page_width - df['x0'], page_width - df['x1']
		return df

	def paint_image_string(self, df):
		painted_String = ''
		current_line_elems = []
		df.sort_values(by=['y1', 'x0'], inplace=True)
		df['separate'] = False
		avg_line_height = 2.5
		for index, row in df.iterrows():
			if not current_line_elems:
				current_line_elems.append(row)
			else:
				if row['y0'] - current_line_elems[-1]['y0'] < avg_line_height and row['x0'] != current_line_elems[-1]['x0']:
					row['separate'] = True
					current_line_elems.append(row)
				else:
					current_line_elems = sorted(current_line_elems, key=lambda x: x['x0'])
					for elem in current_line_elems:
						if elem['separate']:
							painted_String += '\t'
						painted_String += elem['text'] + '- '
					painted_String += '\n'
					current_line_elems = [row]

		return painted_String

	def extract_response(self):
		# extract the response from the model
		pass

	def parse(self):
		text_df = self.extract_text_pdf()
		# extract the details from the invoice
		page_width = self.page_width
		page_height = self.page_height

		text_df['x0'] = text_df['bbox'].apply(lambda x: x[0])
		text_df['y0'] = text_df['bbox'].apply(lambda x: x[1])
		text_df['x1'] = text_df['bbox'].apply(lambda x: x[2])
		text_df['y1'] = text_df['bbox'].apply(lambda x: x[3])

		if page_width > page_height:
			text_df = self.normalize_bbox(text_df, page_width)
		self.text_df = text_df
		painted_string = self.paint_image_string(text_df)
		self.painted_string = painted_string
		
		# TODO - uncomment the following line
		# self.response = self.llama.inference(self.prompt_template_invoice(painted_string))
		return(self.painted_string)


	def export_csv(self):
		# export the details in csv format
		pass
		
	def prompt_template_invoice(self, painted_string):
		question_prompt = (
			"""Invoice Data Extraction Instructions:
			Context:
			You will receive text extracted from a PDF invoice in ROMANIAN. This text attempts to retain the original document's alignment as closely as possible, helping you visualize the original PDF for better understanding of data organization and alignment. 
			
			Instruction:
			Your task is to extract key information from the invoice text and structure it into a JSON format, as shown in the example response below:

			EXAMPLE JSON RESPONSE:
			{
				"beneficiary": "S.C. Exemplu S.R.L.",
				"supplier": "S.C. Furnizor S.R.L.",
				"supplier_fiscal_code": "12345678",
				"phone": "0123456789",
				"email": "furnizor@examplesrl.com",
				"iban": "RO01EXMP1234567890123456",
				"bank": "Banca Exemplu",
				"invoice_number": "FV3838",
				"issuance_date": "01.01.2022",
				"due_date": "20.02.2022",
				"total": "95.00 RON",
				"products": [
					{
						"name": "Surub 5 Inch",
						"quantity": 10,
						"unit_price": 5.00,
						"currency": "RON",
						"unit_of_measure": "BUC",
						"total_value": 50.00
					},
					{
						"name": "Teava PPR - Diametru 4",
						"quantity": 15,
						"unit_price": 3.00,
						"currency": "RON",
						"unit_of_measure": "M",
						"total_value": 45.00
					}
				]
			}

			Ensure your JSON response is valid and adheres strictly to the format above. Do not include any additional details, notes, information or text.

			Extracted Text from the PDF Invoice (formatted as close to the original alignment as possible):
			"""
		)
		return question_prompt + painted_string

	
	# def extrage_date_factura(self):
	# 		# Dicționar pentru a stoca datele extrase
	# 	keys = set('Beneficiar', 'Furnizor', 'Cod fiscal furnizor', 'Sediul furnizor', 'Telefon', 'E-mail', 'IBAN', 'Banca', 'Număr factură', 'Data emiterii', 'Data scadenței', 'Total')
	# 	lines = self.painted_string.split('\n')
	# 	document = {}
	# 	produse = []
	# 	for i in range(len(lines)):
	# 		if 'produse' in lines[i].lower():
	# 			j = i + 1
	# 			while next((key for key in keys if key.lower() in lines[j].lower()), None) is None and j < len(lines):
	# 				produse.append(lines[j])
	# 				j += 1
	# 			if j == len(lines):
	# 				break
	# 		else:
	# 			if next((key for key in keys if key.lower() in lines[i].lower()), None):
	# 				for key in keys:
	# 					if key.lower() in lines[i].lower():
	# 						document[key] = lines[i].split(': ')[1]
		
	# 	document['produse'] = produse
	# 	return document
	def parse_invoice_details(self, invoice_string):
    # Define patterns for each field to be extracted
		patterns = {
			'Beneficiar': re.compile(r"beneficiar: ([^\n]+)", re.I),
			'Furnizor': re.compile(r"furnizor: ([^\n]+)", re.I),
			'Cod fiscal furnizor': re.compile(r"cod fiscal furnizor: (\d+)", re.I),
			'Sediul furnizor': re.compile(r"sediul furnizor: ([^\n]+)", re.I),
			'Telefon': re.compile(r"telefon: ([^\n]+)", re.I),
			'E-mail': re.compile(r"e-mail: ([^\n]+)", re.I),
			'IBAN': re.compile(r"IBAN: ([^\n]+)", re.I),
			'Banca': re.compile(r"banca: ([^\n]+)", re.I),
			'Număr factură': re.compile(r"(număr factură|nr factură|număr factura|nr factura): ([^\n]+)", re.I),
			'Data emiterii': re.compile(r"data emiterii: ([^\n]+)", re.I),
			'Data scadenței': re.compile(r"data scadenței: ([^\n]+)", re.I),
			'Total': re.compile(r"total: ([^\n]+)", re.I)
		}

		document = {}
		# Extract data using regular expressions
		for field, pattern in patterns.items():
			match = re.search(pattern, invoice_string)
			if match:
				document[field] = match.group(1).strip()
			else:
				document[field] = None  # Assign None if no data found

		# Extracting product list
		product_pattern = re.compile(r"(.+?) \| (\d+) \| (\d+\.?\d*)( \| (\w+))?( \| (\w+))?( \| \d+\.?\d*)?", re.I)
		products = re.findall(product_pattern, invoice_string)
		product_list = []
		for prod in products:
			product_details = {
				'Product Name': prod[0],
				'Quantity': prod[1],
				'Unit price': prod[2],
				'Unit of measure': prod[3],
				'Currency': prod[4],
				'Total Value': prod[5]
			}
			product_list.append(product_details)

		document['Lista de produse'] = product_list

		return document


 	# TODO - uncomment the following line
	# print(parser.response)
	# print(parser.parse_invoice_details(parser.response))
 

filepaths = [file for file in os.listdir('/home/oda/consite/consite_server/src/invoice_parser/tests/inputs') if file.endswith('.pdf')]

# parser = Parser(filestream=open('/home/oda/consite/consite_server/src/invoice_parser/FacturaFV3838-Tibrea_Dan.pdf', 'rb').read())
# parser.parse()

# with open("tests/output.txt", "w") as f:
# 	for file in filepaths:
# 		parser = Parser(filestream=open(f'/home/oda/consite/consite_server/src/invoice_parser/tests/inputs/{file}', 'rb').read())
# 		parser.parse()
# 		f.write("-----------------------------------------------\n")
# 		f.write(f"File: {file}\n\n")
# 		f.write(f"Extracted Text:\n\n{parser.painted_string}\n\n\n\n")
# 		f.write(f"LLAMA Inference:\n\n{parser.response}\n\n\n\n")
# 		f.write(f"Extracted Invoice Details:\n\n{parser.parse_invoice_details(parser.response)}\n\n\n\n")
# 		f.write("-----------------------------------------------\n")
		
import fitz
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional

class RobustPDFParser:
    def __init__(self, filestream, debug_mode: bool = False):
        self.filestream = filestream
        self.debug_mode = debug_mode
        self.page_width = 0
        self.page_height = 0
        self.text_df = None
        self.painted_string = ""
        
    def extract_text_pdf(self) -> pd.DataFrame:
        """
        Extract text elements from PDF with improved error handling and validation.
        """
        try:
            doc = fitz.open(stream=self.filestream, filetype='pdf')
            self.page_width = doc[0].rect.width
            self.page_height = doc[0].rect.height
            list_of_elements = []
            
            for page_number, page in enumerate(doc):
                # Get rotation angle and adjust coordinates if needed
                rotation = page.rotation
                text_instances = page.get_text("dict", flags=fitz.TEXTFLAGS_WORDS)['blocks']
                
                for block in text_instances:
                    if block['type'] == 0:  # text block
                        for line in block['lines']:
                            line_bbox = line['bbox']
                            
                            # Handle text orientation
                            if rotation in (90, 270):
                                line_bbox = self._rotate_bbox(line_bbox, rotation)
                            
                            for span in line['spans']:
                                # Filter out empty or whitespace-only text
                                if span['text'].strip():
                                    # Store additional metadata for better processing
                                    list_of_elements.append({
                                        'bbox': line_bbox,
                                        'text': span['text'].strip(),
                                        'font': span.get('font', ''),
                                        'size': span.get('size', 0),
                                        'page': page_number + 1
                                    })
            
            if not list_of_elements:
                raise ValueError("No text elements found in the PDF")
                
            return pd.DataFrame(list_of_elements)
            
        except Exception as e:
            if self.debug_mode:
                print(f"Error in extract_text_pdf: {str(e)}")
            raise
    
    def _rotate_bbox(self, bbox: Tuple[float, float, float, float], rotation: int) -> Tuple[float, float, float, float]:
        """Handle rotated PDF pages by transforming coordinates."""
        x0, y0, x1, y1 = bbox
        if rotation == 90:
            return (y0, -x1, y1, -x0)
        elif rotation == 270:
            return (-y1, x0, -y0, x1)
        return bbox
    
    def normalize_bbox(self, df: pd.DataFrame, page_width: float) -> pd.DataFrame:
        """Normalize bounding boxes with improved handling of different orientations."""
        df = df.copy()
        
        # Calculate text direction heuristic
        text_direction = self._detect_text_direction(df)
        
        if text_direction == 'vertical':
            df['x0'], df['x1'], df['y0'], df['y1'] = df['y1'], df['y0'], df['x1'], df['x0']
            df['x0'], df['x1'] = page_width - df['x0'], page_width - df['x1']
        
        # Ensure coordinates are in correct order
        df[['x0', 'x1']] = np.sort(df[['x0', 'x1']].values, axis=1)
        df[['y0', 'y1']] = np.sort(df[['y0', 'y1']].values, axis=1)
        
        return df
    
    def _detect_text_direction(self, df: pd.DataFrame) -> str:
        """
        Detect if text is primarily horizontal or vertical based on bbox distributions.
        """
        x_spread = df['x1'] - df['x0']
        y_spread = df['y1'] - df['y0']
        
        return 'vertical' if y_spread.mean() < x_spread.mean() else 'horizontal'
    
    def paint_image_string(self, df: pd.DataFrame) -> str:
        """
        Create aligned string representation with improved spacing and alignment.
        """
        painted_string = ''
        current_line_elems = []
        
        # Sort by vertical position first, then horizontal
        df = df.sort_values(by=['y1', 'x0'])
        
        # Calculate dynamic line height based on font sizes
        if 'size' in df.columns:
            avg_line_height = df['size'].mean() * 1.2
        else:
            avg_line_height = (df['y1'] - df['y0']).mean() * 1.2
        
        # Track last position for better spacing
        last_y = None
        last_x = None
        
        for _, row in df.iterrows():
            if not current_line_elems:
                current_line_elems.append(row)
                last_y = row['y0']
                last_x = row['x0']
                continue
                
            # Detect if we're on a new line
            new_line = abs(row['y0'] - last_y) > avg_line_height
            
            if new_line:
                # Process the current line
                current_line_elems = sorted(current_line_elems, key=lambda x: x['x0'])
                
                # Add appropriate spacing between elements
                for elem in current_line_elems:
                    if last_x is not None:
                        space_needed = int((elem['x0'] - last_x) / 10)  # Approximate spaces needed
                        painted_string += ' ' * max(1, space_needed)
                    
                    painted_string += elem['text']
                    last_x = elem['x1']
                
                painted_string += '\n'
                current_line_elems = [row]
                last_y = row['y0']
                last_x = row['x0']
            else:
                # Add to current line with proper spacing
                space_needed = int((row['x0'] - last_x) / 10)
                if space_needed > 1:
                    row['separate'] = True
                current_line_elems.append(row)
                last_x = row['x1']
        
        # Process the last line
        if current_line_elems:
            current_line_elems = sorted(current_line_elems, key=lambda x: x['x0'])
            for elem in current_line_elems:
                if elem.get('separate', False):
                    painted_string += '\t'
                painted_string += elem['text'] + ' '
        
        return painted_string.strip()
    
    def parse(self) -> str:
        """
        Main parsing function with improved error handling and validation.
        """
        try:
            text_df = self.extract_text_pdf()
            
            # Extract bbox coordinates
            for coord in ['x0', 'y0', 'x1', 'y1']:
                text_df[coord] = text_df['bbox'].apply(lambda x: x['x0', 'y0', 'x1', 'y1'].index(coord))
            
            # Normalize coordinates if needed
            if self.page_width > self.page_height:
                text_df = self.normalize_bbox(text_df, self.page_width)
            
            self.text_df = text_df
            self.painted_string = self.paint_image_string(text_df)
            
            return self.painted_string
            
        except Exception as e:
            if self.debug_mode:
                print(f"Error in parse: {str(e)}")
            raise

with open("test.txt", "w") as f:
	parser = Parser(filestream=open('/home/oda/consite/consite_server/src/invoice_parser/tests/inputs/anconi m.pdf', 'rb').read())
	parser.parse()
	f.write("-----------------------------------------------\n")
	f.write(f"Extracted Text:\n\n{parser.painted_string}\n\n\n\n")
	# write text df to file
	f.write("-----------------------------------------------\n")
	f.write("Text Dataframe\n")
	parser.text_df.to_csv(f, index=False)


	## crete a robust parser
	robust_parser = RobustPDFParser(filestream=open('/home/oda/consite/consite_server/src/invoice_parser/tests/inputs/anconi m.pdf', 'rb').read())
	robust_parser.parse()
	f.write("-----------------------------------------------\n")
	
	f.write(f"Extracted Text:\n\n{robust_parser.painted_string}\n\n\n\n")
	
	# write text df to file
	f.write(f"robust_parser Text Dataframe: \n ")
	robust_parser.text_df.to_csv(f, index=False)