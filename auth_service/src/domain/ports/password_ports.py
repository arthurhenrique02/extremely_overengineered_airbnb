from abc import ABC, abstractmethod


class PasswordHashingPort(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a plain text password.

        Args:
            password: The plain text password to hash.

        Returns:
            The hashed password.
        """
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hashed password.

        Args:
            plain_password: The plain text password to verify.
            hashed_password: The hashed password to verify against.

        Returns:
            True if the password matches, False otherwise.
        """
        pass


class PasswordPolicyPort(ABC):
    @abstractmethod
    def validate_password(self, password: str) -> bool:
        """Validate a password against the defined policy.

        Args:
            password: The plain text password to validate.

        Returns:
            True if the password meets the policy, False otherwise.

        Raises:
            ValueError: If the password does not meet the policy.
        """
        pass


class PasswordResetPort(ABC):
    @abstractmethod
    async def initiate_password_reset(self, email: str) -> None:
        """Initiate a password reset process for a user.

        Args:
            email: The user's email address.

        Raises:
            ValueError: If the user does not exist.
        """
        pass

    @abstractmethod
    async def complete_password_reset(self, token: str, new_password: str) -> None:
        """Complete the password reset process using a token.

        Args:
            token: The password reset token.
            new_password: The new plain text password.

        Raises:
            ValueError: If the token is invalid or expired.
        """
        pass
