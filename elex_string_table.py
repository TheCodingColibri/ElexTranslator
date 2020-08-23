from elex_string_table_entry import ElexStringTableEntry


class ElexStringTable:
    def __init__(self, string_table_file_path, description):
        self.string_table_by_id = dict()
        self.description = description
        with open(string_table_file_path, "r") as string_table_file:
            for line in string_table_file:
                entry = ElexStringTableEntry.entry_for(line)
                self.string_table_by_id[entry.engine_id] = entry

    def get_entry(self, engine_id: str) -> ElexStringTableEntry:
        return self.string_table_by_id[engine_id]

    def get_table(self) -> dict:
        return self.string_table_by_id

    def size(self) -> int:
        return len(self.string_table_by_id)