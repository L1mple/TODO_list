from abc import ABC, abstractmethod

from todo.domain.models import Task


class AbstractTaskRepository(ABC):
    """Abstract repository for repository pattern."""

    @abstractmethod
    async def create_one(self, task: Task):
        """Create one method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def create_many(self, tasks: list[Task]):
        """Create many method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_id(self, uid: str):
        """Get method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, page: int = 0, per_page: int = 10):
        """Get many method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def list_all(self):
        """List method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def delete_one_by_id(self, uid: str):
        """Delete method in repository."""
        raise NotImplementedError

    @abstractmethod
    async def replace_one(self, task: Task):
        """Patch method in repository."""
        raise NotImplementedError
