from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth_service.src.adapters.persistence.models._sqlalchemy.user import UserModel
from auth_service.src.domain.models.user import User
from auth_service.src.domain.ports.user_ports import UserRepositoryPort


class SqlAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """Create a new user in the database.

        Args:
            user: The user entity to create.

        Returns:
            The created user with persisted state.

        Raises:
            ValueError: If the user already exists.
        """
        # NOTE: Just checking by email for simplicity
        # TODO: Add checking by username, cellphone and card id
        existing = await self.get_by_email(user.email)
        if existing:
            raise ValueError(f"User with email '{user.email}' already exists")

        user_model = UserModel(**user.model_dump())
        self.session.add(user_model)
        await self.session.flush()

        return User.model_validate(user_model)

    async def update(self, user_id: UUID, user: User) -> User:
        """Update an existing user.

        Args:
            user_id: The ID of the user to update.
            user: The updated user data.

        Returns:
            The updated user.

        Raises:
            ValueError: If the user does not exist.
        """
        user_model = await self.session.get(UserModel, user_id)
        if not user_model:
            raise ValueError(f"User with id '{user_id}' not found")

        for field, value in user.model_dump(
            exclude={"id", "created_at"}, exclude_unset=True
        ).items():
            setattr(user_model, field, value)

        user_model.updated_at = datetime.utcnow()
        await self.session.flush()

        return User.model_validate(user_model)

    async def delete(self, user_id: UUID) -> None:
        """Delete a user by their ID.

        Args:
            user_id: The ID of the user to delete.

        Raises:
            ValueError: If the user does not exist.
        """
        user_model = await self.session.get(UserModel, user_id)
        if not user_model:
            raise ValueError(f"User with id '{user_id}' not found")

        await self.session.delete(user_model)
        await self.session.flush()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalars().first()

        return User.model_validate(user_model) if user_model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user_model = result.scalars().first()

        return User.model_validate(user_model) if user_model else None

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(query)
        user_model = result.scalars().first()

        return User.model_validate(user_model) if user_model else None

    async def exists(self, email: str) -> bool:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        return result.scalars().first() is not None
