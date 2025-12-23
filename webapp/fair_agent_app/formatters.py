"""
Response formatting utilities for FAIR-Agent Web Application
"""

import re


class ResponseFormatter:
    """Utility class to format FAIR-Agent responses for web display"""
    
    @staticmethod
    def format_response_html(text: str) -> str:
        """
        Convert raw FAIR-Agent response text (Markdown) to clean HTML formatting
        """
        if not text:
            return '<p>No response available</p>'
        
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
                     html_lines.append(f'<div style="border: 1px solid #d32f2f; padding: 15px; margin-top: 25px; margin-bottom: 15px; background-color: rgba(211, 47, 47, 0.1); border-radius: 4px;">')
                     html_lines.append(f'<h4 style="margin: 0 0 10px 0; color: #ff6b6b; font-weight: bold; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 0.5px;">{header_text}</h4>')
                     html_lines.append('</div>')
                else:
                    html_lines.append(f'<h3 style="margin-top: 25px; margin-bottom: 15px; color: #FFFFFF; font-weight: 600; border-bottom: 1px solid #333; padding-bottom: 10px;">{header_text}</h3>')

            # 3. Handle Horizontal Rules
            elif line.startswith('---'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append('<hr style="border: 0; border-top: 1px solid #333; margin: 20px 0;">')

            # 4. Handle Lists
            elif line.startswith('- ') or line.startswith('• '):
                if not in_list:
                    html_lines.append('<ul style="margin-left: 20px; color: #CCCCCC;">')
                    in_list = True
                content = line[2:].strip() if line.startswith('- ') else line[2:].strip()
                html_lines.append(f'<li style="margin-bottom: 8px;">{content}</li>')

            # 5. Handle Key/Value pairs (e.g., "Step 1:")
            elif re.match(r'^Step \d+:', line) or line.startswith('Confidence Level:'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<p style="margin: 15px 0 5px 0; font-weight: bold; color: #FFFFFF;">{line}</p>')

            # 6. Default Paragraphs
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<p style="margin-bottom: 10px; line-height: 1.6; color: #E0E0E0;">{line}</p>')
        
        if in_list:
            html_lines.append('</ul>')
            
        return '\n'.join(html_lines)
