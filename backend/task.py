from dataclasses import dataclass, field

from model import model


@dataclass
class Task:
    init_request: str
    done: bool = False
    action_tasks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "init_request": self.init_request,
            "done": self.done,
            "action_tasks": list(self.action_tasks),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Task":
        subtasks = [str(task) for task in data.get("action_tasks", [])]
        return cls(
            init_request=str(data.get("init_request", "")),
            done=bool(data.get("done", False)),
            action_tasks=subtasks,
        )

    def analyze(self) -> list[str]:
        return model(init_request=self.init_request)
