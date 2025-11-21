from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from discord.ext.tasks import Loop


class TaskRouter:
    _task_map: ClassVar[dict[str, list["Loop"]]] = {}

    def __init__(self, module_group: str) -> None:
        self.module_group = module_group

    def __call__(self, task: "Loop") -> "Loop":
        if self.module_group in self._task_map:
            self._task_map[self.module_group].append(task)
        else:
            self._task_map[self.module_group] = [task]

        return task

    @classmethod
    def start_tasks(cls, enabled_modules: list[str]) -> None:
        """Start all tasks for enabled modules."""
        for module_group, tasks_list in cls._task_map.items():
            if module_group in enabled_modules:
                for task in tasks_list:
                    if not task.is_running():
                        task.start()

    @classmethod
    def stop_tasks(cls, enabled_modules: list[str]) -> None:
        """Stop all tasks for enabled modules."""
        for module_group, tasks_list in cls._task_map.items():
            if module_group in enabled_modules:
                for task in tasks_list:
                    if task.is_running():
                        task.cancel()

    @classmethod
    def stop_all_tasks(cls) -> None:
        """Stop all registered tasks."""
        for tasks_list in cls._task_map.values():
            for task in tasks_list:
                if task.is_running():
                    task.cancel()

