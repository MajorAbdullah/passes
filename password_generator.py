import random
import string
import secrets

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(self, length=12, use_lowercase=True, use_uppercase=True, 
                         use_digits=True, use_symbols=True, exclude_ambiguous=True):
        """Generate a secure password with specified criteria"""
        if length < 4:
            length = 4
        
        character_pool = ""
        required_chars = []
        
        if use_lowercase:
            character_pool += self.lowercase
            if exclude_ambiguous:
                character_pool = character_pool.replace('l', '').replace('o', '')
            required_chars.append(secrets.choice(self.lowercase))
        
        if use_uppercase:
            character_pool += self.uppercase
            if exclude_ambiguous:
                character_pool = character_pool.replace('I', '').replace('O', '')
            required_chars.append(secrets.choice(self.uppercase))
        
        if use_digits:
            character_pool += self.digits
            if exclude_ambiguous:
                character_pool = character_pool.replace('0', '').replace('1', '')
            required_chars.append(secrets.choice(self.digits))
        
        if use_symbols:
            character_pool += self.symbols
            required_chars.append(secrets.choice(self.symbols))
        
        if not character_pool:
            # Fallback to alphanumeric if no options selected
            character_pool = self.lowercase + self.uppercase + self.digits
            required_chars = [
                secrets.choice(self.lowercase),
                secrets.choice(self.uppercase),
                secrets.choice(self.digits)
            ]
        
        # Generate remaining characters
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [secrets.choice(character_pool) 
                                         for _ in range(remaining_length)]
        
        # Shuffle the password characters
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def check_password_strength(self, password):
        """Check password strength and return score and feedback"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        # Character variety checks
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.symbols for c in password)
        
        variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
        score += variety_count
        
        if not has_lower:
            feedback.append("Add lowercase letters")
        if not has_upper:
            feedback.append("Add uppercase letters")
        if not has_digit:
            feedback.append("Add numbers")
        if not has_symbol:
            feedback.append("Add special characters")
        
        # Common pattern checks
        if password.lower() in ['password', '123456', 'qwerty', 'admin', 'letmein']:
            score = 0
            feedback.append("Avoid common passwords")
        
        # Sequential characters check
        if self._has_sequential_chars(password):
            score -= 1
            feedback.append("Avoid sequential characters")
        
        # Repeated characters check
        if self._has_repeated_chars(password):
            score -= 1
            feedback.append("Avoid repeated characters")
        
        # Determine strength level
        if score >= 6:
            strength = "Very Strong"
            color = "green"
        elif score >= 4:
            strength = "Strong"
            color = "blue"
        elif score >= 2:
            strength = "Medium"
            color = "orange"
        else:
            strength = "Weak"
            color = "red"
        
        return {
            'score': max(0, score),
            'max_score': 6,
            'strength': strength,
            'color': color,
            'feedback': feedback
        }
    
    def _has_sequential_chars(self, password, min_length=3):
        """Check for sequential characters"""
        password = password.lower()
        for i in range(len(password) - min_length + 1):
            substring = password[i:i + min_length]
            if (substring in self.lowercase or 
                substring in self.digits or
                substring == substring[::-1]):  # reversed sequence
                return True
        return False
    
    def _has_repeated_chars(self, password, min_length=3):
        """Check for repeated characters"""
        for i in range(len(password) - min_length + 1):
            char = password[i]
            if password[i:i + min_length] == char * min_length:
                return True
        return False
    
    def generate_passphrase(self, word_count=4, separator="-"):
        """Generate a passphrase using random words"""
        # Simple word list for passphrases
        words = [
            'apple', 'banana', 'cherry', 'dragon', 'elephant', 'forest', 'garden', 'harbor',
            'island', 'jungle', 'kitchen', 'lemon', 'mountain', 'ocean', 'planet', 'quiet',
            'river', 'sunset', 'thunder', 'umbrella', 'village', 'winter', 'yellow', 'zebra',
            'bridge', 'castle', 'dream', 'energy', 'freedom', 'galaxy', 'harmony', 'journey',
            'knight', 'liberty', 'melody', 'nature', 'orange', 'phoenix', 'rainbow', 'spirit',
            'treasure', 'universe', 'victory', 'wisdom', 'crystal', 'adventure', 'butterfly',
            'compass', 'discovery', 'emerald', 'falcon', 'golden', 'horizon', 'infinite'
        ]
        
        selected_words = [secrets.choice(words) for _ in range(word_count)]
        # Capitalize first letter of each word
        selected_words = [word.capitalize() for word in selected_words]
        
        # Add some numbers for extra security
        selected_words.append(str(secrets.randbelow(100)))
        
        return separator.join(selected_words)
