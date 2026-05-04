from abc import ABC, abstractmethod

class State(ABC):
    """One node in the FSM. Subclasses implement enter/update/exit."""
    
    priority = 0    

    @abstractmethod
    def enter(self, context : dict) -> None:
        pass

    @abstractmethod
    def update(self, context : dict) -> str | None:
        """Return next state name to transition, or None to stay."""
        pass
        
    @abstractmethod
    def exit(self, context : dict) -> None:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__