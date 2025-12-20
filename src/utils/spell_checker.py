import logging
import re
from typing import Tuple, List

logger = logging.getLogger(__name__)

class QuerySpellChecker:
    """
    A utility class to check and correct spelling in user queries.
    Uses pyspellchecker if available.
    """
    
    def __init__(self):
        self.enabled = False
        try:
            from spellchecker import SpellChecker
            self.spell = SpellChecker()
            self.enabled = True
            logger.info("SpellChecker initialized successfully.")
        except ImportError:
            logger.warning("pyspellchecker not found. Spell checking is disabled. Please install it via 'pip install pyspellchecker'.")
            self.spell = None

    def correct_text(self, text: str) -> Tuple[str, bool, List[str]]:
        """
        Corrects the spelling of the given text.
        
        Args:
            text (str): The input text to check.
            
        Returns:
            Tuple[str, bool, List[str]]: A tuple containing:
                - The corrected text.
                - A boolean indicating if any corrections were made.
                - A list of corrected words (original -> corrected).
        """
        if not self.enabled or not text:
            return text, False, []

        # Simple tokenization (keeping it simple for now)
        # We want to preserve punctuation, so we might need a better tokenizer or regex
        # For now, let's just split by whitespace and strip punctuation for checking
        
        words = text.split()
        corrected_words = []
        corrections_made = []
        has_changes = False
        
        for word in words:
            # Strip punctuation for checking
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            if not clean_word or clean_word.isnumeric():
                corrected_words.append(word)
                continue
                
            # Check if the word is misspelled
            if clean_word.lower() not in self.spell:
                # Get the one `most likely` answer
                correction = self.spell.correction(clean_word)
                
                if correction and correction.lower() != clean_word.lower():
                    # Replace the clean word in the original word (preserving punctuation)
                    # This is a bit tricky, let's try a simple replacement
                    new_word = word.replace(clean_word, correction)
                    corrected_words.append(new_word)
                    corrections_made.append(f"{clean_word} -> {correction}")
                    has_changes = True
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
                
        corrected_text = " ".join(corrected_words)
        return corrected_text, has_changes, corrections_made

# Global instance
spell_checker = QuerySpellChecker()
