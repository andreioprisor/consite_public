import fitz
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from model_inference import Inference
import os
from collections import defaultdict

class Parser:
    def __init__(self, filestream, debug_mode: bool = False):
        self.filestream = filestream
        self.debug_mode = debug_mode
        self.page_width = 0
        self.page_height = 0
        self.page_dfs = []
        self.painted_string = ""
        self.response = ""
        self.llm = "unsloth/llama-3-8b-Instruct-bnb-4bit"
        
    def extract_text_pdf(self) -> pd.DataFrame:
        """
        Extract text elements from PDF with multi-page support.
        Returns a DataFrame with text elements and their coordinates
        For multiple pages, elements will be concatenated vertically with padding.
        """
        try:
            doc = fitz.open(stream=self.filestream, filetype='pdf')
            # Store dimensions of first page as reference
            self.page_width = doc[0].rect.width
            self.page_height = doc[0].rect.height
            
            all_elements = []
            y_offset = 0  # Offset for concatenating pages vertically
            
            for page_number, page in enumerate(doc):
                # Get rotation angle and adjust coordinates if needed
                rotation = page.rotation
                text_instances = page.get_text("dict", flags=fitz.TEXTFLAGS_WORDS)['blocks']
                
                for block in text_instances:
                    if block['type'] == 0:  # text block
                        for line in block['lines']:
                            line_bbox = list(line['bbox'])  # Convert to list for modification
                            
                            # Apply y-offset for current page
                            line_bbox[1] += y_offset  # y0
                            line_bbox[3] += y_offset  # y1
                            
                            # Handle text orientation
                            if rotation in (90, 270):
                                line_bbox = self._rotate_bbox(tuple(line_bbox), rotation)
                            
                            for span in line['spans']:
                                # Filter out empty or whitespace-only text
                                if span['text'].strip():
                                    # Store additional metadata for better processing
                                    all_elements.append({
                                        'bbox': line_bbox,
                                        'text': span['text'].strip(),
                                        'font': span.get('font', ''),
                                        'size': span.get('size', 0),
                                        'page': page_number + 1
                                    })
                
                # Update y_offset for next page
                # Add some padding between pages
                y_offset += page.rect.height + 20  # 20 points padding between pages
            
            if not all_elements:
                raise ValueError("No text elements found in the PDF")
                
            return pd.DataFrame(all_elements)
            
        except Exception as e:
            if self.debug_mode:
                print(f"Error in extract_text_pdf: {str(e)}")
            raise
        finally:
            if 'doc' in locals():
                doc.close()
    
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
    
    def _detect_table_structure(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect table-like structures in the document based on spatial analysis.
        Returns DataFrame with additional column indicating table membership.
        """
        df = df.copy()
        df['table_id'] = -1  # -1 means not part of a table
        
        # Group elements by page
        for page_num, page_df in df.groupby('page'):
            current_table_id = 0
            
            # Sort by vertical position
            page_df = page_df.sort_values('y0')
            
            # Find aligned columns (elements with similar x coordinates)
            x_starts = page_df['x0'].values
            x_ends = page_df['x1'].values
            
            # Tolerance for considering coordinates aligned
            x_tolerance = (df['x1'] - df['x0']).mean() * 0.1
            
            # Find vertical alignments
            vertical_alignments = defaultdict(list)
            for i, (x0, x1) in enumerate(zip(x_starts, x_ends)):
                for j, (other_x0, other_x1) in enumerate(zip(x_starts, x_ends)):
                    if i != j:
                        # Check if elements are vertically aligned
                        if (abs(x0 - other_x0) < x_tolerance or 
                            abs(x1 - other_x1) < x_tolerance):
                            vertical_alignments[i].append(j)
            
            # Find groups of aligned elements that might form tables
            processed = set()
            for i in range(len(page_df)):
                if i in processed:
                    continue
                    
                if len(vertical_alignments[i]) >= 2:  # At least 3 aligned elements
                    # Find y-coordinates that might represent rows
                    aligned_indices = {i} | set(vertical_alignments[i])
                    aligned_rows = defaultdict(list)
                    
                    for idx in aligned_indices:
                        y_coord = page_df.iloc[idx]['y0']
                        aligned_rows[round(y_coord, 1)].append(idx)
                    
                    # If we have multiple rows with aligned elements, mark as table
                    if len(aligned_rows) >= 2:
                        for row_indices in aligned_rows.values():
                            for idx in row_indices:
                                df.loc[page_df.iloc[idx].name, 'table_id'] = current_table_id
                                processed.add(idx)
                        current_table_id += 1
        
        return df


    def paint_image_string(self, df: pd.DataFrame) -> str:
        """
        Create aligned string representation with spacing and alignment.
        Handles multiple pages with clear separation.
        """
        painted_string = ''
        current_line_elems = []
        
        # Sort by vertical position first, then horizontal
        df = df.sort_values(by=['y1', 'x0'])
        
        # Calculate dynamic line height based on font sizes
        if 'size' in df.columns and not df['size'].isna().all():
            avg_line_height = df['size'].mean() * 1.2
        else:
            avg_line_height = (df['y1'] - df['y0']).mean() * 1.2
        
        # Track last position and page for better spacing
        last_y = None
        last_x = None
        current_page = None
        
        for _, row in df.iterrows():
            # Check if we're starting a new page
            if current_page is not None and row['page'] != current_page:
                # Process any remaining elements from the previous page
                if current_line_elems:
                    current_line_elems = sorted(current_line_elems, key=lambda x: x['x0'])
                    for elem in current_line_elems:
                        if elem.get('separate', False):
                            painted_string += '\t'
                        if elem['table_id'] != -1:
                            elem['text'] = '| ' + elem['text'] + ' |'
                            print(elem['text'])
                        painted_string += elem['text']
                    
                    painted_string += '\n'
                    current_line_elems = []
                
                # Add page separator
                painted_string += '\n' + '-' * 80 + f'\nPage {row["page"]}\n' + '-' * 80 + '\n\n'
                last_y = None
                last_x = None
            
            current_page = row['page']
            
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
                        painted_string += '| ' + ' ' * max(1, space_needed)
                    
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

    def prompt_template_invoice(self, painted_string):
        question_prompt = f"""You are a specialized invoice parser. Extract the following information from the provided invoice text into a JSON format. Parse numbers with Romanian decimal format (using comma as decimal separator).
            Required fields to extract:

            Beneficiary (Cumparator)
            Supplier (Furnizor)
            Supplier fiscal code (C.I.F. from supplier section)
            Phone number if present (not mandatory)
            Email if present (not mandatory)
            IBAN (look for the beneficiary's IBAN, usually after "Cont:" or "Contul:")
            Bank name (look for beneficiary's bank)
            Invoice number (look for "Nr." followed by digits)
            Issuance date (Data or Data facturii)
            Due date if present (Data scadenta, not mandatory)
            Total amount (look for "TOTAL LIVRAT:" or final sum)
            Total with TVA (same as total if no separate amount shown)
            Products list containing:

            Product name (from a column like "Denumire and may span multiple lines)")
            Quantity (usually from Cant./Cantitate colum or similar)
            Unit price (usually from Pret unitar column or similar)
            Currency (RON by default if not specified)
            Unit of measure (usually from U.M. column)
            Total Value of Unit price x Quantity for this product(usually from Valoare or Pret column)
            TVA amount (TVA column)

            Return the data in the following JSON structure:
            {{
            "beneficiary": string,
            "supplier": string,
            "supplier_fiscal_code": string,
            "phone": string or null,
            "email": string or null,
            "iban": string,
            "bank": string,
            "invoice_number": string,
            "issuance_date": string,
            "due_date": string or null,
            "total": string,
            "total_with_tva": string,
            "products": [
            {{
            "name": string,
            "quantity": number,
            "unit_price": number,
            "currency": string,
            "unit_of_measure": string,
            "total_value": string,
            "tva": string
            }}
            ]
            }}
            Important parsing rules:

            Keep number formats as they appear in the invoice (with comma as decimal separator)
            Include currency (RON) in total amounts
            For products, convert quantities and unit prices to numbers
            If a field is not found in the invoice, set it to null
            Remove any extra whitespace from extracted values

            Extract the information from the following invoice text:
            {self.painted_string}
            OUTPUT JUST THE JSON RESPONSE, NOTHING ELSE.
            JSON Response:
            """
        
        return question_prompt



    def inference(self):
        llm = Inference(self.llm)
        prompt = self.prompt_template_invoice(self.painted_string)
        response = llm.inference(prompt, self.painted_string)
        return response

    def parse(self) -> str:
        """
        Main parsing function with improved error handling and validation.
        """
        try:
            text_df = self.extract_text_pdf()
            
            # Extract bbox coordinates
            text_df['x0'] = text_df['bbox'].apply(lambda x: x[0])
            text_df['y0'] = text_df['bbox'].apply(lambda x: x[1])
            text_df['x1'] = text_df['bbox'].apply(lambda x: x[2])
            text_df['y1'] = text_df['bbox'].apply(lambda x: x[3])
            
            # Normalize coordinates if needed
            if self.page_width > self.page_height:
                text_df = self.normalize_bbox(text_df, self.page_width)

            # Detect table-like structures
            text_df = self._detect_table_structure(text_df)
            
            
            self.text_df = text_df
            self.painted_string = self.paint_image_string(text_df)
            
            self.response = self.inference()
            
        except Exception as e:
            if self.debug_mode:
                print(f"Error in parse: {str(e)}")
            raise
        
# Output to claude_output.txt

# invoices_directory = 'tests/inputs_public/'
# output_file = 'parser_output.txt'

# with open(output_file, "w") as f:
#     for file in os.listdir(invoices_directory):
#         parser = RobustPDFParser(filestream=open(invoices_directory + file, 'rb').read())
#         parser.parse()
#         f.write("-----------------------------------------------\n")
#         # f.write(f"File: {file}\n")
#         f.write(f"Extracted Text:\n\n{parser.painted_string}\n\n\n\n")
#         f.write("-----------------------------------------------\n")
#         f.write("Generated Response:\n\n")
#         f.write(parser.response)
        
#         # write text df to file