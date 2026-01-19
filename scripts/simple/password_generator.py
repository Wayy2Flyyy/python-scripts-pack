"""Generate secure random passwords."""

from __future__ import annotations

import math
import secrets
import string


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Password length (minimum 4)
        use_uppercase: Include uppercase letters
        use_lowercase: Include lowercase letters
        use_digits: Include digits
        use_special: Include special characters
        
    Returns:
        Generated password
    """
    if length < 4:
        raise ValueError("Password length must be at least 4")
    
    charset = ""
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_lowercase:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_special:
        charset += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    
    if not charset:
        raise ValueError("At least one character type must be enabled")
    
    # Ensure at least one character from each enabled type
    password = []
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice("!@#$%^&*()-_=+[]{}|;:,.<>?"))
    
    # Fill the rest with random characters from the full charset
    for _ in range(length - len(password)):
        password.append(secrets.choice(charset))
    
    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)


def estimate_strength(password: str) -> str:
    """Estimate password strength based on entropy."""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password)
    
    charset_size = 0
    if has_upper:
        charset_size += 26
    if has_lower:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_special:
        charset_size += 22
    
    # Calculate entropy bits: log2(charset_size^length)
    if charset_size > 0:
        entropy = length * math.log2(charset_size)
    else:
        entropy = 0
    
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Fair"
    elif entropy < 80:
        return "Strong"
    else:
        return "Very Strong"


def main() -> None:
    """Interactive password generator."""
    print("Secure Password Generator")
    print("=" * 50)
    print()
    
    # Get length
    while True:
        length_input = input("Password length (default 16): ").strip()
        if not length_input:
            length = 16
            break
        try:
            length = int(length_input)
            if length < 4:
                print("Length must be at least 4")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Get character type preferences
    print("\nInclude character types:")
    use_uppercase = input("Uppercase letters? (Y/n): ").strip().lower() != "n"
    use_lowercase = input("Lowercase letters? (Y/n): ").strip().lower() != "n"
    use_digits = input("Digits? (Y/n): ").strip().lower() != "n"
    use_special = input("Special characters? (Y/n): ").strip().lower() != "n"
    
    # Get count
    while True:
        count_input = input("\nNumber of passwords to generate (default 1): ").strip()
        if not count_input:
            count = 1
            break
        try:
            count = int(count_input)
            if count < 1:
                print("Count must be at least 1")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    print("\nGenerated passwords:")
    print("-" * 50)
    
    try:
        for i in range(count):
            password = generate_password(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_special=use_special,
            )
            strength = estimate_strength(password)
            print(f"{i + 1}. {password} [{strength}]")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
