from src.core.figure import Figure


class Board:
    def __init__(self, data: dict):
        self.id: str = data.get("uuid")
        self.owner: str = data.get("owner")
        self.invited: list[str] = data.get("invited")
        self.mode: str = data.get("mode")
        self.privacy: str = data.get("privacy")
        self.white: str = data.get("white")
        self.black: str = data.get("black")
        self.status: str = data.get("status")
        self.state = {
            pos: Figure(item.get('figure'), pos, item.get('actor'))
            for pos, item in data.get('state').items()
        }

        self.code = None

    def update(self, data: dict):
        self.id: str = data.get("uuid")
        self.owner: str = data.get("owner")
        self.invited: list[str] = data.get("invited")
        self.mode: str = data.get("mode")
        self.privacy: str = data.get("privacy")
        self.white: str = data.get("white")
        self.black: str = data.get("black")
        self.status: str = data.get("status")
        self.update_state(data.get('state'))

    def update_state(self, state):
        self.state = {
            pos: Figure(item.get('figure'), pos, item.get('actor'))
            for pos, item in state.items()
        }


class Move:
    def __init__(self, data: dict):
        self.id: str = data.get("uuid")
        self.actor: str = data.get("actor")
        self.src: str = data.get("src")
        self.dst: str = data.get("dst")

    def __eq__(self, other):
        return other and self.id == other.id


class AvailableMove:
    def __init__(self, data: dict):
        print(data)
        self.src: str = data.get("src")
        self.dst: str = data.get("dst")
        self.promotion: str = data.get("promotion")
