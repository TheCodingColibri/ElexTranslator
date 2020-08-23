from elex_string_table_format import ElexStringTableFormat


class ElexStringTableEntry:
    def __init__(self, engine_id: str, text: str, stage_dir_text: str):
        self.engine_id = engine_id
        self.text = text
        self.stage_dir_text = stage_dir_text

    def to_string(self) -> str:
        return self.engine_id + "|" + self.text + "|" + self.stage_dir_text

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.to_string())

    @staticmethod
    def remove_trailing_newline(value: str) -> str:
        if value.endswith("\n"):
            index = value.rindex("\n")
            slice_without_ending_newline = slice(0, index, 1)
            result = value[slice_without_ending_newline]
            return result
        return value

    @staticmethod
    def entry_for(line: str):
        f = ElexStringTableFormat()
        split_line = line.split(f.separator, 2)
        return ElexStringTableEntry(split_line[f.indexes["engine_id"]],
                                    split_line[f.indexes["text"]],
                                    ElexStringTableEntry.remove_trailing_newline(
                                        split_line[f.indexes["stage_dir_text"]]))
