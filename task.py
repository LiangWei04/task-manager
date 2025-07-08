import argparse
import csv

class Task:
    def __init__(self, description, due_date, tag=None):
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.tag = tag
    
    def __str__(self):
        return f"description: {self.description}\ndue date: {self.due_date}\ncomplete: {self.completed}\ntag: {self.tag}"

    @classmethod
    def get(cls):
        description = input("Task description: ")
        due_date = input("input due date (dd/mm/yy): ")
        tag = input("Add tag(optional):")
        return cls(description, due_date, tag)
    
    
    

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
                    writer = csv.DictWriter(file, fieldnames=["description", "due_date", "completed", "tag"])
                    writer.writeheader()
                    for task in self.tasks:
                        writer.writerow({
                            "description":task.description,
                            "due_date": task.due_date,
                            "completed": task.completed,
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
                        tag=row["tag"] if row["tag"] else None
                    )
                    task.completed = row["completed"].lower() == "true"
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def edit_task(self, index):
        try:
            task = self.tasks[index]
            print("Leave blank to keep current value.")
            new_desc = input(f"New description (current {task.description}): ") or task.description
            new_due = input(f"New due date (current {task.due_date})") or task.due_date
            new_tag = input(f"New tag (current {task.tag})") or task.tag
            task.description = new_desc
            task.due_date = new_due
            task.tag = new_tag
        except IndexError:
            print("❌ invalid task number")
    def delete_task(self, index):
        try:
            removed = self.tasks.pop(index)
            print(f"remove task {removed.description}")
        except IndexError:
            print("❌ invalid task number")
    def complete_task(self, index):
        try:
            if self.tasks[index].completed == False:
                self.tasks[index].completed = True
                print(f"✅ Marked task {index + 1} as complete.")
            else:
                self.tasks[index].completed = False
                print(f"✅ Marked task {index + 1} as uncomplete.")
        except IndexError:
            print("❌ invalid task number")

def main():
    parser = argparse.ArgumentParser(description="Task manager")
    parser.add_argument("-a", "--add" ,help="add argument", type=str)
    parser.add_argument("--interactive", help="launch interactive task input", action="store_true")
    parser.add_argument("-e", "--edit",  help="edit task", type=str)
    parser.add_argument("-d", "--delete",help="delete task", type=str)
    parser.add_argument("-c", "--complete",help="mark complete", type=str)
    parser.add_argument("-v", "--view",help="view all tasks", action="store_true")
    parser.add_argument("--due", help="due date for the task", type=str)
    parser.add_argument("-t", "--tag", help="add tag", type=str)
    
    args = parser.parse_args()
    manager = TaskManager()
    manager.load_from_file()
    if args.add:
        task = Task(description=args.add, due_date=args.due, tag=args.tag)
        manager.add_task(task)
        manager.save_to_file()
        print("✅ Task added.")
    elif args.interactive:
        task = Task.get()
        manager.add_task(task)
        manager.save_to_file()
        print("✅ Task added interactively.")
    
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



if __name__ == "__main__":
    main()