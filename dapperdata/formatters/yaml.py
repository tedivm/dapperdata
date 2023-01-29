import sys
from typing import Any

import ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


# Extend the YAML object to capture strings.
class YAMLWithStrings(YAML):
    def dump(self, data: Any, stream=None, **kw) -> None | str:
        return_string = False
        if stream is None:
            return_string = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if return_string:
            return stream.getvalue()
        return None


#
# Overload the comment writer to remove superfluous newlines.
#

# Save the original comment writer so our extended version can use it.
ruamel.yaml.emitter.Emitter.write_comment_original = ruamel.yaml.emitter.Emitter.write_comment  # type: ignore

# Create the new comment writer.
def strip_empty_lines_write_comment(self, comment: Any, pre: bool = False) -> None:
    # Check if comment is nothing but newlines.
    # Then replace with a single new line.
    string_check = comment.value.replace("\n", "")
    if len(string_check) == 0:
        comment.value = "\n"
        pre = True
    self.write_comment_original(comment, pre)


# Set ruamel.yaml to use the new writer.
ruamel.yaml.emitter.Emitter.write_comment = strip_empty_lines_write_comment  # type: ignore


yaml = YAMLWithStrings()
yaml.preserve_quotes = True  # type: ignore
yaml.default_flow_style = False
yaml.width = 120  # type: ignore
yaml.indent(mapping=2, sequence=4, offset=2)


def yaml_formatter(input: str) -> str:
    # The load function returns a MappedComment class that includes
    # comments and other useful data. The dump function uses that to add
    # comments back in.
    data = yaml.load(input)
    return yaml.dump(data)  # type: ignore
