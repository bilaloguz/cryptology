"""
Advanced letter combination strategies for polygraphic ciphers.

This module provides sophisticated letter combination strategies that handle
different languages, alphabet sizes, and edge cases for polygraphic ciphers.
"""

import re
from typing import Dict, List, Tuple, Optional, Callable
from enum import Enum


class CombinationStrategy(Enum):
    """Different strategies for combining letters."""
    PRESERVE_BASE = "preserve_base"  # Keep base letters, remove diacritics
    PRESERVE_DIACRITIC = "preserve_diacritic"  # Keep diacritics, remove base
    SMART_COMBINE = "smart_combine"  # Intelligent combination based on frequency
    CUSTOM = "custom"  # User-defined combination rules


class LetterCombinationEngine:
    """Advanced letter combination engine for polygraphic ciphers."""
    
    def __init__(self):
        self.language_rules = self._initialize_language_rules()
        self.frequency_data = self._initialize_frequency_data()
    
    def _initialize_language_rules(self) -> Dict[str, Dict[str, str]]:
        """Initialize language-specific combination rules."""
        return {
            "english": {
                "combinations": {
                    'j': 'i', 'J': 'I'  # I=J combination for 5x5 squares
                },
                "priority": "preserve_base",
                "target_size": 25  # For 5x5 square
            },
            "turkish": {
                "combinations": {
                    'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
                    'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U',
                    'j': 'i', 'J': 'I'  # I=J combination like English
                },
                "priority": "preserve_base",
                "target_size": 25  # For 5x5 square
            }
        }
    
    def _initialize_frequency_data(self) -> Dict[str, Dict[str, float]]:
        """Initialize letter frequency data for smart combination."""
        return {
            "english": {
                'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75,
                's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
                'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97,
                'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
                'q': 0.10, 'z': 0.07
            },
            "turkish": {
                'a': 11.92, 'e': 8.91, 'i': 8.60, 'r': 7.36, 'n': 7.23, 'l': 6.06,
                'd': 4.98, 'k': 4.83, 'ı': 4.82, 'y': 3.33, 's': 2.95, 'b': 2.84,
                'z': 1.48, 'ç': 1.15, 'g': 1.13, 'ğ': 1.12, 'ş': 0.88, 'ö': 0.78,
                'ü': 0.68, 'c': 0.60, 'f': 0.44, 'h': 0.35, 'j': 0.01, 'p': 0.01,
                'q': 0.01, 'v': 0.01, 'w': 0.01, 'x': 0.01
            }
        }
    
    def detect_language(self, alphabet: str) -> str:
        """Detect the language of an alphabet with improved accuracy."""
        alphabet_lower = alphabet.lower()
        
        # Check for specific language indicators - ENGLISH and TURKISH ONLY
        language_indicators = {
            "turkish": ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü'],
            "english": []  # English has no special characters
        }
        
        for language, indicators in language_indicators.items():
            if indicators and any(char in alphabet_lower for char in indicators):
                return language
        
        # Check alphabet length and common patterns
        if len(alphabet) == 26 and all(char in 'abcdefghijklmnopqrstuvwxyz' for char in alphabet_lower):
            return "english"
        
        return "unknown"
    
    def combine_letters(self, alphabet: str, strategy: CombinationStrategy = CombinationStrategy.SMART_COMBINE,
                       target_size: Optional[int] = None, custom_rules: Optional[Dict[str, str]] = None) -> str:
        """
        Combine letters using the specified strategy.
        
        Args:
            alphabet: Input alphabet
            strategy: Combination strategy to use
            target_size: Target alphabet size (default: auto-detect)
            custom_rules: Custom combination rules
            
        Returns:
            Combined alphabet
        """
        if strategy == CombinationStrategy.CUSTOM and custom_rules:
            return self._apply_custom_rules(alphabet, custom_rules)
        
        language = self.detect_language(alphabet)
        
        if language in self.language_rules:
            rules = self.language_rules[language]
            if target_size is None:
                target_size = rules.get("target_size", 25)
            
            if strategy == CombinationStrategy.SMART_COMBINE:
                return self._smart_combine(alphabet, language, target_size)
            else:
                return self._apply_language_rules(alphabet, rules, strategy)
        else:
            return self._generic_combine(alphabet, target_size or 25)
    
    def _smart_combine(self, alphabet: str, language: str, target_size: int) -> str:
        """Smart combination based on letter frequency and language rules."""
        if language not in self.frequency_data:
            return self._apply_language_rules(alphabet, self.language_rules.get(language, {}), CombinationStrategy.PRESERVE_BASE)
        
        # Get frequency data
        frequencies = self.frequency_data[language]
        
        # Apply language-specific combinations first
        rules = self.language_rules[language]
        combined = self._apply_combinations(alphabet, rules["combinations"])
        
        # If still too long, remove least frequent letters
        if len(combined) > target_size:
            # Create frequency map for remaining letters
            letter_freq = {}
            for char in combined:
                char_lower = char.lower()
                if char_lower in frequencies:
                    letter_freq[char] = frequencies[char_lower]
                else:
                    letter_freq[char] = 0.0  # Unknown letters get lowest priority
            
            # Sort by frequency (descending) and keep top letters
            sorted_letters = sorted(letter_freq.items(), key=lambda x: x[1], reverse=True)
            combined = ''.join([char for char, _ in sorted_letters[:target_size]])
        
        return combined
    
    def _apply_language_rules(self, alphabet: str, rules: Dict, strategy: CombinationStrategy) -> str:
        """Apply language-specific combination rules."""
        combinations = rules.get("combinations", {})
        combined = self._apply_combinations(alphabet, combinations)
        
        # Remove duplicates while preserving order
        return self._remove_duplicates(combined)
    
    def _apply_combinations(self, alphabet: str, combinations: Dict[str, str]) -> str:
        """Apply letter combinations."""
        result = alphabet
        for original, replacement in combinations.items():
            result = result.replace(original, replacement)
        return result
    
    def _remove_duplicates(self, alphabet: str) -> str:
        """Remove duplicate characters while preserving order."""
        seen = set()
        unique_chars = []
        for char in alphabet:
            if char not in seen:
                unique_chars.append(char)
                seen.add(char)
        return ''.join(unique_chars)
    
    def _generic_combine(self, alphabet: str, target_size: int) -> str:
        """Generic combination for unknown languages."""
        # Remove duplicates first
        unique_alphabet = self._remove_duplicates(alphabet)
        
        if len(unique_alphabet) <= target_size:
            return unique_alphabet
        
        # If too long, truncate to target size
        return unique_alphabet[:target_size]
    
    def _apply_custom_rules(self, alphabet: str, custom_rules: Dict[str, str]) -> str:
        """Apply custom combination rules."""
        result = alphabet
        for original, replacement in custom_rules.items():
            result = result.replace(original, replacement)
        return self._remove_duplicates(result)
    
    def get_combination_report(self, alphabet: str) -> Dict:
        """Generate a report on letter combination strategy."""
        language = self.detect_language(alphabet)
        original_size = len(alphabet)
        
        # Test different strategies
        strategies = {
            "preserve_base": self.combine_letters(alphabet, CombinationStrategy.PRESERVE_BASE),
            "smart_combine": self.combine_letters(alphabet, CombinationStrategy.SMART_COMBINE),
            "generic": self.combine_letters(alphabet, CombinationStrategy.PRESERVE_BASE, target_size=25)
        }
        
        return {
            "original_alphabet": alphabet,
            "original_size": original_size,
            "detected_language": language,
            "strategies": strategies,
            "recommendations": self._get_recommendations(language, original_size)
        }
    
    def _get_recommendations(self, language: str, size: int) -> List[str]:
        """Get recommendations for letter combination strategy."""
        recommendations = []
        
        if size > 25:
            recommendations.append(f"Alphabet has {size} letters, needs reduction for 5x5 square")
        
        if language in self.language_rules:
            recommendations.append(f"Use {language}-specific combination rules")
        else:
            recommendations.append("Use generic combination strategy")
        
        if language in self.frequency_data:
            recommendations.append("Smart combination available based on letter frequency")
        
        return recommendations


# Convenience functions for backward compatibility
def combine_similar_letters(alphabet: str, language: str = "auto") -> str:
    """Backward compatibility function."""
    engine = LetterCombinationEngine()
    if language == "auto":
        language = engine.detect_language(alphabet)
    
    return engine.combine_letters(alphabet, CombinationStrategy.SMART_COMBINE)


def detect_language(alphabet: str) -> str:
    """Backward compatibility function."""
    engine = LetterCombinationEngine()
    return engine.detect_language(alphabet)


def get_combination_strategies() -> Dict[str, Dict]:
    """Get all available combination strategies."""
    engine = LetterCombinationEngine()
    return engine.language_rules
