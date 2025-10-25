"""
Hill Cipher implementation.

The Hill cipher uses matrix multiplication to encrypt n-grams.
It operates on groups of letters using modular arithmetic.
"""

import re
import numpy as np
from typing import List, Optional


def _prepare_text(text: str, n: int) -> str:
    """
    Prepare text for Hill encryption/decryption.
    
    Args:
        text: Input text
        n: Size of n-grams (matrix size)
        
    Returns:
        Prepared text (uppercase, letters only, X padding for proper length)
    """
    # Remove non-alphabetic characters and convert to uppercase
    text_clean = re.sub(r'[^A-Za-z]', '', text.upper())
    
    # Add X padding to make length divisible by n
    while len(text_clean) % n != 0:
        text_clean += 'X'
    
    return text_clean


def _char_to_num(char: str) -> int:
    """
    Convert character to number (A=0, B=1, ..., Z=25).
    
    Args:
        char: Single character
        
    Returns:
        Number representation (0-25)
    """
    return ord(char) - ord('A')


def _num_to_char(num: int) -> str:
    """
    Convert number to character (0=A, 1=B, ..., 25=Z).
    
    Args:
        num: Number (0-25)
        
    Returns:
        Character representation
    """
    return chr((num % 26) + ord('A'))


def _mod_inverse(a: int, m: int) -> int:
    """
    Find modular inverse of a mod m.
    
    Args:
        a: Number to find inverse of
        m: Modulus
        
    Returns:
        Modular inverse
        
    Raises:
        ValueError: If modular inverse doesn't exist
    """
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse of {a} mod {m} does not exist")
    
    return (x % m + m) % m


def _matrix_inverse(matrix: np.ndarray) -> np.ndarray:
    """
    Find modular inverse of matrix mod 26.
    
    Args:
        matrix: Input matrix
        
    Returns:
        Modular inverse matrix
        
    Raises:
        ValueError: If matrix is not invertible mod 26
    """
    det = int(round(np.linalg.det(matrix))) % 26
    if det == 0:
        raise ValueError("Matrix determinant is 0, matrix is not invertible")
    
    # Check if determinant is coprime with 26
    if np.gcd(det, 26) != 1:
        raise ValueError(f"Matrix determinant {det} is not coprime with 26")
    
    # Find modular inverse of determinant
    det_inv = _mod_inverse(det, 26)
    
    # Calculate adjugate matrix
    adjugate = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix)).astype(int) % 26
    
    # Calculate modular inverse
    inverse = (adjugate * det_inv) % 26
    
    return inverse.astype(int)


def _encrypt_ngram(key_matrix: np.ndarray, ngram: str) -> str:
    """
    Encrypt an n-gram using Hill cipher.
    
    Args:
        key_matrix: Encryption key matrix (n x n)
        ngram: String of n characters to encrypt
        
    Returns:
        Encrypted n-gram
    """
    n = len(ngram)
    if n != key_matrix.shape[0]:
        raise ValueError(f"N-gram length {n} must match matrix size {key_matrix.shape[0]}")
    
    # Convert characters to numbers
    vector = np.array([_char_to_num(char) for char in ngram])
    
    # Matrix multiplication
    result_vector = (key_matrix @ vector) % 26
    
    # Convert back to characters
    return ''.join(_num_to_char(num) for num in result_vector)


def _decrypt_ngram(key_matrix: np.ndarray, ngram: str) -> str:
    """
    Decrypt an n-gram using Hill cipher.
    
    Args:
        key_matrix: Encryption key matrix (n x n)
        ngram: String of n characters to decrypt
        
    Returns:
        Decrypted n-gram
    """
    n = len(ngram)
    if n != key_matrix.shape[0]:
        raise ValueError(f"N-gram length {n} must match matrix size {key_matrix.shape[0]}")
    
    # Find modular inverse of key matrix
    inverse_matrix = _matrix_inverse(key_matrix)
    
    # Convert characters to numbers
    vector = np.array([_char_to_num(char) for char in ngram])
    
    # Matrix multiplication with inverse
    result_vector = (inverse_matrix @ vector) % 26
    
    # Convert back to characters
    return ''.join(_num_to_char(num) for num in result_vector)


def encrypt(plaintext: str, key_matrix: List[List[int]]) -> str:
    """
    Encrypt plaintext using Hill cipher.
    
    Args:
        plaintext: Text to encrypt
        key_matrix: Encryption key matrix (n x n)
        
    Returns:
        Encrypted text
        
    Raises:
        ValueError: If key matrix is invalid or not square
    """
    key_array = np.array(key_matrix)
    
    if key_array.ndim != 2:
        raise ValueError("Key matrix must be 2-dimensional")
    
    if key_array.shape[0] != key_array.shape[1]:
        raise ValueError("Key matrix must be square")
    
    n = key_array.shape[0]
    if n < 2:
        raise ValueError("Key matrix must be at least 2x2")
    
    # Prepare text
    text = _prepare_text(plaintext, n)
    
    # Encrypt n-grams
    result = ""
    for i in range(0, len(text), n):
        ngram = text[i:i+n]
        result += _encrypt_ngram(key_array, ngram)
    
    return result


def decrypt(ciphertext: str, key_matrix: List[List[int]]) -> str:
    """
    Decrypt ciphertext using Hill cipher.
    
    Args:
        ciphertext: Text to decrypt
        key_matrix: Encryption key matrix (n x n)
        
    Returns:
        Decrypted text
        
    Raises:
        ValueError: If key matrix is invalid or not invertible
    """
    key_array = np.array(key_matrix)
    
    if key_array.ndim != 2:
        raise ValueError("Key matrix must be 2-dimensional")
    
    if key_array.shape[0] != key_array.shape[1]:
        raise ValueError("Key matrix must be square")
    
    n = key_array.shape[0]
    if n < 2:
        raise ValueError("Key matrix must be at least 2x2")
    
    # Prepare text
    text = _prepare_text(ciphertext, n)
    
    # Decrypt n-grams
    result = ""
    for i in range(0, len(text), n):
        ngram = text[i:i+n]
        result += _decrypt_ngram(key_array, ngram)
    
    return result
