"""
Response formatting utilities for FAIR-Agent Web Application
"""

import re


class ResponseFormatter:
    """Utility class to format FAIR-Agent responses for web display"""
    
    @staticmethod
    def format_response_html(text: str) -> str:
        """
        Convert raw FAIR-Agent response text (Markdown) to clean HTML formatting with Times New Roman
        """
        if not text:
            return '<p style="font-family: \'Times New Roman\', Times, serif;">No response available</p>'
        
        # Clean up the text first
        formatted = text.strip()
        
        # 1. Handle Bold and Italic (Markdown)
        formatted = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', formatted)
        formatted = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', formatted)
        
        # Split into lines for processing
        lines = formatted.split('\n')
        html_lines = []
        
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                continue
            
            # 2. Handle Headers (##)
            if line.startswith('## '):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                
                header_text = line[3:].strip()
                # Special styling for Disclaimers
                if 'Disclaimer' in header_text or 'Notice' in header_text:
                     html_lines.append(f'<div style="border: 2px solid #000; padding: 10px; margin-top: 25px; margin-bottom: 15px; background-color: #fff8f8;">')
                     html_lines.append(f'<h3 style="font-family: \'Times New Roman\', Times, serif; margin: 0; color: #d32f2f; font-weight: bold;">{header_text}</h3>')
                     html_lines.append('</div>')
                else:
                    html_lines.append(f'<h3 style="font-family: \'Times New Roman\', Times, serif; margin-top: 25px; margin-bottom: 15px; color: #000; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px;">{header_text}</h3>')

            # 3. Handle Horizontal Rules
            elif line.startswith('---'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append('<hr style="border: 0; border-top: 1px solid #ccc; margin: 20px 0;">')

            # 4. Handle Lists
            elif line.startswith('- ') or line.startswith('• '):
                if not in_list:
                    html_lines.append('<ul style="font-family: \'Times New Roman\', Times, serif; margin-left: 20px;">')
                    in_list = True
                content = line[2:].strip() if line.startswith('- ') else line[2:].strip()
                html_lines.append(f'<li style="margin-bottom: 8px;">{content}</li>')

            # 5. Handle Key/Value pairs (e.g., "Step 1:")
            elif re.match(r'^Step \d+:', line) or line.startswith('Confidence Level:'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<p style="font-family: \'Times New Roman\', Times, serif; margin: 10px 0; font-weight: bold;">{line}</p>')

            # 6. Default Paragraphs
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<p style="font-family: \'Times New Roman\', Times, serif; margin-bottom: 10px; line-height: 1.6;">{line}</p>')
        
        if in_list:
            html_lines.append('</ul>')
            
        return '\n'.join(html_lines)
