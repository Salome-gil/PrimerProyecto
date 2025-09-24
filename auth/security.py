"""
Módulo de seguridad para manejo de contraseñas
"""

import hashlib
import secrets
from typing import Tuple


class PasswordManager:
    """Gestor de contraseñas con hash seguro"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Generar hash seguro de una contraseña

        Args:
            password: Contraseña en texto plano

        Returns:
            Hash de la contraseña con salt
        """
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return f"{salt}:{password_hash.hex()}"

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verificar si una contraseña coincide con su hash

        Args:
            password: Contraseña en texto plano
            password_hash: Hash almacenado

        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            salt, hash_part = password_hash.split(":")
            password_hash_check = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
            )
            return password_hash_check.hex() == hash_part
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """
        Validar la fortaleza de una contraseña

        Args:
            password: Contraseña a validar

        Returns:
            Tupla con (es_válida, mensaje)
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"

        if len(password) > 128:
            return False, "La contraseña no puede exceder 128 caracteres"

        if not any(c.isupper() for c in password):
            return False, "La contraseña debe contener al menos una letra mayúscula"

        if not any(c.islower() for c in password):
            return False, "La contraseña debe contener al menos una letra minúscula"

        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe contener al menos un número"

        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "La contraseña debe contener al menos un carácter especial"

        return True, "Contraseña válida"

    @staticmethod
    def generate_secure_password(length: int = 12) -> str:
        """
        Generar una contraseña segura aleatoria

        Args:
            length: Longitud de la contraseña

        Returns:
            Contraseña segura generada
        """
        import string

        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = "".join(secrets.choice(characters) for _ in range(length))
        return password