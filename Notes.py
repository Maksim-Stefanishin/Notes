import json
import os
from datetime import datetime


class Note:
    def __init__(self, note_id, title, body, timestamp):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'note_id': self.note_id,
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp
        }


class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        notes = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                notes_data = json.load(file)
                notes = [Note(**note_data) for note_data in notes_data]
        return notes

    def save_notes(self):
        notes_data = [note.to_dict() for note in self.notes]
        with open(self.file_path, 'w') as file:
            json.dump(notes_data, file, indent=2)

    def show_notes(self, filtered_notes=None):
        if filtered_notes is None:
            notes_to_display = self.notes
        else:
            notes_to_display = filtered_notes

        for note in notes_to_display:
            print(f"ID: {note.note_id}\nTitle: {note.title}\nBody: {note.body}\nTimestamp: {note.timestamp}\n")

    def add_note(self, title, body):
        note_id = len(self.notes) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_note = Note(note_id, title, body, timestamp)
        self.notes.append(new_note)
        print("Note added successfully.")

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = title
                note.body = body
                note.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Note edited successfully.")
                return
        print("Note not found.")

    def delete_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                print("Note deleted successfully.")
                return
        print("Note not found.")

    def filter_notes_by_date(self, date_str):
        filtered_notes = [note for note in self.notes if note.timestamp.startswith(date_str)]
        return filtered_notes


def main():
    file_path = "notes.json"
    note_manager = NoteManager(file_path)

    while True:
        print("\n1. Show Notes\n2. Add Note\n3. Edit Note\n4. Delete Note\n5. Filter by Date\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            date_filter = input("Enter date to filter (YYYY-MM-DD), press Enter to show all: ")
            if date_filter:
                filtered_notes = note_manager.filter_notes_by_date(date_filter)
                note_manager.show_notes(filtered_notes)
            else:
                note_manager.show_notes()
        elif choice == '2':
            title = input("Enter note title: ")
            body = input("Enter note body: ")
            note_manager.add_note(title, body)
        elif choice == '3':
            note_id = int(input("Enter note ID to edit: "))
            title = input("Enter new title: ")
            body = input("Enter new body: ")
            note_manager.edit_note(note_id, title, body)
        elif choice == '4':
            note_id = int(input("Enter note ID to delete: "))
            note_manager.delete_note(note_id)
        elif choice == '5':
            date_filter = input("Enter date to filter (YYYY-MM-DD): ")
            filtered_notes = note_manager.filter_notes_by_date(date_filter)
            note_manager.show_notes(filtered_notes)
        elif choice == '6':
            note_manager.save_notes()
            print("Exiting the application. Notes saved.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

