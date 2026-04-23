import argparse
import csv
from datetime import datetime, timedelta
class Task:
    def __init__(self, description, due_date, priority, duration, tag=None):
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.tag = tag
        self.priority = priority
        self.duration = duration
        self.urgency = None
        self.score = None

    def __str__(self):
        return f"description: {self.description}\ndue date: {self.due_date}\ncomplete: {self.completed}\ntag: {self.tag}\npriority: {self.priority}\nduration: {self.duration}"

    @classmethod
    def get(cls):
        try:
            description = input("Task description: ").strip()
            due_date = input("Input due date (dd-mm-yyyy): ").strip()
            tag = input("Add tag(optional): ").strip()
            priority = int(input("Input priority from 1 to 5 where 5 is the top priority: ").strip())
            duration = float(input("Input duration in hours: ").strip())

            if duration <= 0:
                print("Duration should be positive.")
                return

            if not description or not due_date or not priority or not duration:
                print("Missing required field(s): --due, --priority, --duration, --description")
                return

            try:
                datetime.strptime(due_date, "%d-%m-%Y")
            except ValueError:
                print("Invalid date format. Use dd-mm-yyyy")
                return

            if not (1 <= priority <= 5):
                print("Priority must be between 1 and 5")
                return

            return cls(description, due_date, priority, duration, tag)

        except ValueError:
            print("Invalid input. Priority and duration must be numbers.")
            return None


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def list_tasks(self):
        if not self.tasks:
            print("no task yet")
            return
        for index, task in enumerate(self.tasks, start=1):
            print(f"\n Task {index}")
            print(task)

    def save_to_file(self, filename="task.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["description", "due_date", "completed", "priority", "duration", "tag"])
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    "description":task.description,
                    "due_date": task.due_date,
                    "completed": task.completed,
                    "priority": task.priority,
                    "duration": task.duration,
                    "tag": task.tag if task.tag else ""
                })

    def load_from_file(self, filename="task.csv"):
        try:
            with open(filename, mode="r", newline="") as file:
                
                reader = csv.DictReader(file)
                for row in reader:
                    task = Task(
                        description=row["description"],
                        due_date=row["due_date"],
                        tag=row["tag"] if row["tag"] else None,
                        priority=int(row.get("priority", 3)),
                        duration=float(row.get("duration", 1)),
                    )
                    task.completed = row["completed"].lower() == "true"
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def edit_task(self, index):
        try:
            task = self.tasks[index]
        except IndexError:
            print("Invalid task number")
            return

        print("Leave blank to keep current value.")

        new_desc = input(f"New description (current {task.description}): ").strip()
        new_due = input(f"New due date (current {task.due_date}): ").strip()
        new_tag = input(f"New tag (current {task.tag}): ").strip()
        new_priority = input(f"New priority (current {task.priority}): ").strip()
        new_duration = input(f"New duration (current {task.duration}): ").strip()

        if not new_desc:
            new_desc = task.description

        if not new_due:
            new_due = task.due_date
        else:
            try:
                datetime.strptime(new_due, "%d-%m-%Y")
            except ValueError:
                print("Invalid date format. Use dd-mm-yyyy")
                return

        if not new_tag:
            new_tag = task.tag

        if not new_priority:
            new_priority = task.priority
        else:
            try:
                new_priority = int(new_priority)
            except ValueError:
                print("Priority must be a whole number")
                return
            if not (1 <= new_priority <= 5):
                print("Priority must be between 1 and 5")
                return

        if not new_duration:
            new_duration = task.duration
        else:
            try:
                new_duration = float(new_duration)
            except ValueError:
                print("Duration must be a number")
                return

        task.description = new_desc
        task.due_date = new_due
        task.tag = new_tag
        task.priority = new_priority
        task.duration = new_duration

    def delete_task(self, index):
        try:
            removed = self.tasks.pop(index)
            print(f"Remove task {removed.description}")
        except IndexError:
            print("Invalid task number")
    def complete_task(self, index):
        try:
            if self.tasks[index].completed is False:
                self.tasks[index].completed = True
                print(f"Marked task {index + 1} as complete.")
            else:
                self.tasks[index].completed = False
                print(f"Marked task {index + 1} as uncomplete.")
        except IndexError:
            print("Invalid task number")
class TaskScheduler:
    def __init__(self, tasks):
        self.tasks = tasks

    def compute_score(self, task, cur_time):
        due_date = datetime.strptime(task.due_date, "%d-%m-%Y")
        days = (due_date - cur_time).days

        urgency = (1 / (days + 1)) if days > 0 else (1 + abs(days) * 0.1)

        return 0.4 * urgency + 0.4 * task.priority - 0.2 * task.duration

    def recommended_order(self):
        remaining = self.tasks[:]
        order = []

        cur_time = datetime.now()

        while remaining:
            best_task = max(remaining, key=lambda t: self.compute_score(t, cur_time))
            order.append(best_task)

            cur_time += timedelta(hours=best_task.duration)
            remaining.remove(best_task)

        return order


def main():
    parser = argparse.ArgumentParser(description="Task manager")
    parser.add_argument("-a", "--add" ,help="add argument", type=str)
    parser.add_argument("--interactive", help="launch interactive task input", action="store_true")
    parser.add_argument("-e", "--edit",  help="edit task", type=int)
    parser.add_argument("-d", "--delete",help="delete task", type=int)
    parser.add_argument("-c", "--complete",help="mark complete", type=int)
    parser.add_argument("-v", "--view",help="view all tasks", action="store_true")
    parser.add_argument("-o", "--order",help="Suggest task by priority", action="store_true")
    parser.add_argument("--due", help="due date for the task", type=str)
    parser.add_argument("-t", "--tag", help="add tag", type=str)
    parser.add_argument("--priority", type=int, help="1–5 importance level")
    parser.add_argument("--duration", type=float, help="duration in hours")

    args = parser.parse_args()
    manager = TaskManager()
    manager.load_from_file()


    if args.add:
        if args.due is None or args.priority is None or args.duration is None:
            print("Missing required field(s): --due, --priority, --duration")
            return

        try:
            datetime.strptime(args.due, "%d-%m-%Y")
        except ValueError:
            print("Invalid date format. Use dd-mm-yyyy")
            return

        if not (1 <= args.priority <= 5):
            print("Priority must be between 1 and 5")
            return

        task = Task(
            description=args.add,
            due_date=args.due,
            priority=args.priority,
            duration=args.duration,
            tag=args.tag
        )

        manager.add_task(task)
        manager.save_to_file()
        print("Task added.")

    elif args.interactive:
        task = Task.get()
        if task:
            manager.add_task(task)
            manager.save_to_file()
            print("Task added interactively.")



    if args.edit is not None:
        manager.edit_task(args.edit - 1)
        manager.save_to_file()
    if args.delete is not None:
        manager.delete_task(args.delete - 1)
        manager.save_to_file()
    if args.complete is not None:
        manager.complete_task(args.complete - 1)
        manager.save_to_file()

    if args.view:
        manager.list_tasks()

    if args.order:
        scheduler = TaskScheduler([task for task in manager.tasks if not task.completed])    
        order = scheduler.recommended_order()
        for i, task in enumerate(order, start=1):
            print(f"{i}. {task.description}")

if __name__ == "__main__":
    main()