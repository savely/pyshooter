from .base_state import State

class FSM:
    """
    Finite state machine. Owner is whatever object the states act on —
    an entity, the app, a scene. States receive it directly in every call.
    """

    def __init__(self, owner):
        self._owner  = owner
        self._states: dict[str, State] = {}
        self._current: State | None = None

    #setup methods
    def add(self, state: State) -> "FSM":
        """Register a state. Uses the class name as the key. Chainable."""
        self._states[state.name] = state
        return self

    def start(self, name: str, context: dict = None) -> None:
        """Activate the FSM. Must be called before update()."""
        self._current = self._get(name)
        self._current.enter(self._owner)
        
    #runtime methods

    def update(self, context: dict = None) -> None:
        next_name = self._current.update(context)
        if next_name:
            self.transition(next_name)

    def transition(self, name: str, force: bool = False) -> None:
        """
        Switch to a new state.
        Blocked if the incoming state has lower priority than the current one,
        unless force=True.
        """
        incoming = self._get(name)

        if not force and incoming.priority < self._current.priority:
            return

        self._current.exit()
        self._current = incoming
        self._current.enter(self._owner)

    #accessors
    @property
    def current(self) -> str:
        return self._current.name

    #helpers
    def is_in(self, *names: str) -> bool:
        return self._current.name in names

    def _get(self, name: str) -> State:
        if name not in self._states:
            known = ", ".join(self._states)
            raise KeyError(f"Unknown state '{name}'. Registered: [{known}]")
        return self._states[name]