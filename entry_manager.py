import json
import os

class EntryManager:
    def __init__(self, filename, source):
        self.filename = filename
        self.source = source
        self.entries = []
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if self.source not in data:
                        data[self.source] = {"entries": []}
                    self.data = data
                    self.entries = data[self.source]["entries"]
            except json.JSONDecodeError:
                self.data = {self.source: {"entries": []}}
                self.entries = self.data[self.source]["entries"]
        else:
            self.data = {self.source: {"entries": []}}
            self.entries = self.data[self.source]["entries"]

    def get_entries(self):
        return self.entries

    def add_entry_id(self, entry_id):
        if entry_id not in self.entries:
            self.entries.append(entry_id)
            self._save()

    def _save(self):
        self.data[self.source]["entries"] = self.entries
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)