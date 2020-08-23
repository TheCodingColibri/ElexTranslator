from elex_string_table import ElexStringTable
from config import Config
import readline


def main():
    config = Config()
    print_comparer_info(config)
    start_comparison(config)
    write_target_file(config)


def start_comparison(config: Config):
    differing_entries = different_entries(config)  # TODO rename method

    print("\n------- Begin Editing -------\n")
    count_translations = 0
    aborted_by_user = False
    for engine_id in differing_entries:
        source_entry = config.source_string_table.get_entry(engine_id)
        compare_entry = config.compare_string_table.get_entry(engine_id)
        target_default = config.target_string_table_default.get_entry(engine_id)
        modded_entry_ger = config.target_string_table.get_entry(engine_id)
        count_translations += 1

        if aborted_by_user:
            continue

        print("Differing value for id={0} ({1}/{2})".format(source_entry.engine_id, count_translations,
                                                            len(differing_entries)))
        print_entry_of(config.source_string_table.description, source_entry.text)
        print_entry_of(config.compare_string_table.description, compare_entry.text)
        print_entry_of(config.target_string_table_default.description, target_default.text)

        if bool(config.target["run-with-auto-fill"]):
            modded_entry_ger.text = config.target["auto-fill-value"]
            print("\t---> Writing auto-fill value '{}' for this entry".format(config.target["auto-fill-value"]))
            continue

        user_input = prompt_entry_for(config.target["name"], modded_entry_ger.text)
        if abort_on_user_input(user_input):
            aborted_by_user = True

        if user_input == "":
            print("\t---> Writing suggested value '{}' fir this entry".format(modded_entry_ger.text))
        else:
            modded_entry_ger.text = user_input
    print("\n------- Finished Editing -------\n")
    print("A total of {0} entries has been translated/edited".format(count_translations))


def different_entries(config: Config) -> list:
    differing_engine_ids = list()
    for entry in config.source_string_table.get_table():
        source_entry = config.source_string_table.get_entry(entry)
        compare_entry = config.compare_string_table.get_entry(entry)
        if hash(source_entry) != hash(compare_entry):
            differing_engine_ids.append(entry)
    return differing_engine_ids


def write_target_file(config: Config):
    with open(config.target["file"], "w") as result_file:
        for entry in config.target_string_table.get_table():
            result_file.write(config.target_string_table.get_entry(entry).to_string())
            result_file.write("\n")


def abort_on_user_input(user_input: str) -> bool:
    return user_input == "q"


def print_entry_of(table_description: str, entry_text: str):
    print("\t{0:20}: {1}".format(table_description, entry_text))


def prompt_entry_for(table_description: str, entry_text: str) -> str:
    prompt = "\t{0:20}: ".format(table_description)
    readline.set_startup_hook(lambda: readline.insert_text(entry_text))
    try:
        pass
    finally:
        readline.set_startup_hook()
    return input(prompt)


def print_string_table_info(string_table: ElexStringTable):
    print("\tString table '{0}' with {1} entries".format(string_table.description,
                                                         string_table.size()))


def print_comparer_info(config: Config):
    print("Elex String Table comparison/translation/editing tool.")

    print("Quick overview for this tool:")
    print("------------------------------")
    print("Config:")
    print("\tEdit the 'config.json' file to control the flow of this tool")
    print("\tThe 'source' and 'compare' properties specify the two string tables that will be compared")
    print("\tThe 'target' property specifies the target string table that will be created by this tool")
    print("\tThe 'default_for_target' property serves as a pre-filled string table from which values are suggested to "
          "be taken over into the target string table")
    print("\tWhen 'run-with-auto-fill' is 'true', this tool runs non-interactively i.e. differing string table "
          "entries will be filled with the value specified in 'auto-fill-value'. This is useful if the translation "
          "shall be done with a different tool e.g. a spreadsheet software.")
    print("Editing:")
    print("This tool will go through the string tables configured line by line. If it spots a difference it will stop "
          "and print out the differing lines and prompt you for a translation.")
    print("\tEnter 'q' to exit the tool, all changes done so far are written to the target string table")
    print("\tEnter ENTER (i.e. enter no value) to copy/take over the suggested default value for the target string "
          "table")
    print("")

    print("String tables that are compared:")
    print_string_table_info(config.source_string_table)
    print_string_table_info(config.compare_string_table)
    print("String table used as default translation:")
    print_string_table_info(config.target_string_table_default)


main()
