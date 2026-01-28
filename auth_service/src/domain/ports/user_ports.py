from abc import ABC, abstractmethod
from typing import Optional

from pydantic import UUID4

from ..models.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user in the repository.

        Args:
            user: The user entity to create.

        Returns:
            The created user with persisted state.

        Raises:
            ValueError: If the user already exists.
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID4) -> Optional[User]:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: The user's UUID.

        Returns:
            The user if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address.

        Args:
            email: The user's email address.

        Returns:
            The user if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username.

        Args:
            username: The user's username.

        Returns:
            The user if found, None otherwise.
        """
        pass

    @abstractmethod
    async def update(self, user_id: UUID4, user: User) -> User:
        """Update an existing user.

        Args:
            user_id: The ID of the user to update.
            user: The updated user data.

        Returns:
            The updated user.

        Raises:
            ValueError: If the user does not exist.
        """
        pass

    @abstractmethod
    async def delete(self, user_id: UUID4) -> None:
        """Delete a user by their ID.

        Args:
            user_id: The ID of the user to delete.

        Raises:
            ValueError: If the user does not exist.
        """
        pass

    @abstractmethod
    async def exists(self, email: str) -> bool:
        """Check if a user exists by email.

        Args:
            email: The user's email address.

        Returns:
            True if the user exists, False otherwise.
        """
        pass


class UserUseCasePort(ABC):
    """Port for user-related use cases (i.e. the business logic)."""

    @abstractmethod
    async def register_user(
        self,
        name: str,
        surname: str,
        birth_date: str,
        email: str,
        username: str,
        password: str,
    ) -> User:
        """Register a new user.

        Args:
            name: User's first name.
            surname: User's last name.
            birth_date: User's birth date as ISO format string.
            email: User's email address.
            username: User's unique username.
            password: User's plain text password.

        Returns:
            The registered user.

        Raises:
            ValueError: If validation fails or user already exists.
        """
        pass

    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate a user by email and password.

        Args:
            email: User's email address.
            password: User's plain text password.

        Returns:
            The authenticated user.

        Raises:
            ValueError: If authentication fails.
        """
        pass

    @abstractmethod
    async def get_user(self, user_id: UUID4) -> User:
        """Retrieve a user by ID.

        Args:
            user_id: The user's unique identifier.

        Returns:
            The user.

        Raises:
            ValueError: If user not found.
        """
        pass

    @abstractmethod
    async def update_user(
        self,
        user_id: UUID4,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        """Update user profile information.

        Args:
            user_id: The user's unique identifier.
            name: Updated first name.
            surname: Updated last name.
            email: Updated email address.
            username: Updated username.

        Returns:
            The updated user.

        Raises:
            ValueError: If user not found or validation fails.
        """
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID4) -> None:
        """Delete a user account.

        Args:
            user_id: The user's unique identifier.

        Raises:
            ValueError: If user not found.
        """
        pass

    @abstractmethod
    async def activate_user(self, user_id: UUID4) -> User:
        """Activate a user account.

        Args:
            user_id: The user's unique identifier.

        Returns:
            The activated user.

        Raises:
            ValueError: If user not found.
        """
        pass

    @abstractmethod
    async def deactivate_user(self, user_id: UUID4) -> User:
        """Deactivate a user account.

        Args:
            user_id: The user's unique identifier.

        Returns:
            The deactivated user.

        Raises:
            ValueError: If user not found.
        """
        pass
