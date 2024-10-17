from typing import Literal
from rich.text import Text

from rich.highlighter import RegexHighlighter
from rich.theme import Theme
from rich.console import Console


class DocHighlighter(RegexHighlighter):
    base_style = "doc."
    highlights = [r"(?P<option>((?<!\w)[-\+]\w)|(--[\w-]+))", r"(?P<code_block>`.*?`)", r"(?P<argument><.+?>)"]


doc_theme = Theme({"doc.option": "bold green1", "doc.code_block": "italic cyan", "doc.argument": "underline"})
doc_highlighter = DocHighlighter()

_console = Console(theme=doc_theme)


def print_doc(which: Literal["check", "rename"]):
    with _console.pager(styles=True):
        if which == "check":
            _console.print(check_doc)

        elif which == "rename":
            _console.print(rename_doc)

        else:
            raise RuntimeError("Could not find documentation")


def _SectionBody(header: Text, *body: Text) -> Text:
    return Text.assemble(header, *body, "\n")


def _SectionHeader(text: str) -> Text:
    return Text(text.upper() + "\n", "bold blue")


def _SectionParagraph(*text: str | Text) -> Text:
    return Text.assemble("\t", *(doc_highlighter(t + " ") for t in text), "\n")


def _Link(text: str) -> Text:
    return Text(text, "bold blue")


B, H, P = _SectionBody, _SectionHeader, _SectionParagraph


check_doc = Text.assemble(
    Text("ArchiveTools check\n\n"),
    B(H("name"), P("check - check for invalid file paths on a target file system")),
    B(
        H("synopsis"),
        P("archivetools check -h | --help"),
        P("archivetools check --doc"),
        P(r"""archivetools check [<filename>]
                           [-f | --fs <file system>]
                           [-c | --config <path>]
                           [--output <format>]
                           [-[+]eil]
"""),
    ),
    B(
        H("description"),
        P(
            "Check performs checks on a file or directory <filename> to find file names that would be invalid on a target <file system>.",
            "This is usefull to identify issues before copying files from one file system to another.",
        ),
    ),
    B(
        H("options"),
        P("-h or --help", "\n\t\tDisplay a short description of this command with a summary of its options.\n"),
        P("--doc\tDisplay the full command documentation.\n"),
        P(
            "-f or --fs <file system>",
            "\n\t\tSelect the target file system for the checks. <file system> can be [windows].\n",
        ),
        P("-c or --config <path>", "\n\t\tProvide a", _Link("configuration"), "file.\n"),
        P(
            "--output <format>",
            "\n\t\tSelect an output <format. <format> can be [cli, csv].\n",
            "\t\t- cli is more user-friendly and uses colors to clearly point at invalid path portions.\n",
            "\t\t- csv is easier to parse and to store.\n",
        ),
        P("-e or check-empty-dirs", "\n\t\tCheck for empty directories recursively.\n"),
        P("+e or add-check-empty-dirs", "\n\t\tCheck for empty directories as well as the default -i and -l checks.\n"),
        P("-i or check-invalid-characters", "\n\t\tCheck for invalid characters in file paths. Active by default.\n"),
        P(
            "-l or check-path-length",
            "\n\t\tCheck for path length exceeding the file system's limite. Active by default.\n",
        ),
        P(
            "By default, checks for invalid characters and path lenghts are performed, as if using `archivetools check -i -l` options.",
            "-e, -i and -l options individually select checks to be run, i.e. `archivetools check -e` will ONLY run checks for empty directories.",
        ),
        P(
            "For convenience, the +e option can be used to add empty directories checks to the default -i and -l checks."
            "This is equivalent to `archivetools check -i -l -e`.",
        ),
    ),
    B(
        H("configuration"),
        P(
            "Configuration options must be written to a file and passed through the -c option. The default configuration for the check command is :",
        ),
        P(
            """
[windows]
special_characters = <>:/\\|?*
max_path_length = 260

[special_characters]
extra = ""

[exclude]
""",
        ),
        P(
            "Section [special_characters] allows to define extra characters to consider invalid if found in file paths during -i checks.\n"
        ),
        P(
            "Section [exclude] allows to define a list of paths to exclude from the analysis (one path per line). Paths can be absolute or relative to the command's execution directory."
        ),
    ),
)

rename_doc = Text.assemble(
    Text("ArchiveTools rename\n\n"),
    B(H("name"), P("rename - fix issues making file paths invalid on a target file system")),
    B(
        H("synopsis"),
        P("archivetools rename -h | --help"),
        P("archivetools rename --doc"),
        P(r"""archivetools rename [<filename>]
                           [-f | --fs <file system>]
                           [-c | --config <path>]
                           [-[+]eil]
"""),
    ),
    B(
        H("description"),
        P(
            "Rename fixes issues with a file path or with paths within a directory <filename> to comply with rules on a target <file system>.",
            "\n\tFirst, invalid characters are replaced with a replacement character, _ (underscore) by default."
            "\n\tThen, files and directories are renamed according to rules defined in the",
            _Link("configuration"),
            "file.",
            "\n\tFinally, empty directories are removed and path lengths are checked.",
        ),
    ),
    B(
        H("options"),
        P("-h or --help", "\n\t\tDisplay a short description of this command with a summary of its options.\n"),
        P("--doc\tDisplay the full command documentation.\n"),
        P(
            "-f or --fs <file system>",
            "\n\t\tSelect the target file system for the checks. <file system> can be [windows].\n",
        ),
        P("-c or --config <path>", "\n\t\tProvide a", _Link("configuration"), "file.\n"),
        P("-e or check-empty-dirs", "\n\t\tRemove empty directories recursively.\n"),
        P(
            "+e or add-check-empty-dirs",
            "\n\t\tRemove empty directories as well as the default -i and -l operations.\n",
        ),
        P(
            "-i or check-invalid-characters",
            "\n\t\tReplace invalid characters in file paths with a replacement defined in the configuration file. Active by default, replacement by an underscore.\n",
        ),
        P(
            "-l or check-path-length",
            "\n\t\tCheck for path length exceeding the file system's limite. Active by default.\n",
        ),
        P(
            "By default, checks for invalid characters and path lenghts are performed, as if using `archivetools check -i -l` options.",
            "-e, -i and -l options individually select checks to be run, i.e. `archivetools check -e` will ONLY run checks for empty directories.",
        ),
        P(
            "For convenience, the +e option can be used to add empty directories checks to the default -i and -l checks."
            "This is equivalent to `archivetools check -i -l -e`.",
        ),
    ),
    B(
        H("configuration"),
        P(
            "Configuration options must be written to a file and passed through the -c option. The default configuration for the rename command is :",
        ),
        P(
            """
[windows]
special_characters = <>:/\\|?*
max_path_length = 260

[special_characters]
extra = ""
replacement = _

[replace]

[exclude]
""",
        ),
        P(
            "Section [special_characters] allows to define:"
            "\n\t- extra characters to consider invalid if found in file paths during -i checks.",
            "\n\t- a replacement string for invalid characters.\n",
        ),
        P(
            "Section [replace] allows to define renaming rules to apply to file paths (one rule per line).",
            "\n\tA renaming rule follows the format : `<pattern> = <replacement> [NO_CASE] [NO_ACCENT]` where <pattern> is a regex string to match in paths and <replacement> is a regular string to use as replacement for the matched pattern.",
            "\n\tOptional flags NO_CASE and NO_ACCENT indicate that pattern matching should be insensitive to case and accents respectively.",
            "\n\tExample: `(_){2,} = _` matches multiple consecutive underscores and replaces them by a single underscore.\n",
        ),
        P(
            "Section [exclude] allows to define a list of paths to exclude from the analysis (one path per line). Paths can be absolute or relative to the command's execution directory."
        ),
    ),
)