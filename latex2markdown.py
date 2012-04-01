import re
from collections import defaultdict

#------------------------------------------------------------------------------

import json
# Load our JSON configuration file.
with open("config.json", "r") as f:
    _block_configuration = json.load(f)

#------------------------------------------------------------------------------

class LaTeX2Markdown(object):
    """Initialise with a LaTeX string - see the main routine for examples of
    reading this string from an existing .tex file.

    To modify the outputted markdown, modify the _block_configuration variable
    before initializing the LaTeX2Markdown instance."""
    def __init__(self,  latex_string,
                        block_configuration = _block_configuration,
                        block_counter = defaultdict(lambda: 1)):

        self._block_configuration = block_configuration
        self._latex_string = latex_string
        self._block_counter = block_counter

        # Precompile the regexes

        # Select everything in the main matter
        self._main_re = re.compile(r"""\\begin{document}
                                    (?P<main>.*)
                                    \\end{document}""",
                                    flags=re.DOTALL + re.VERBOSE)

        # Select all our block materials.
        self._block_re = re.compile(r"""\\begin{(?P<block_name>exer|proof|thm|lem|prop)} # block name
                                    (\[(?P<block_title>.*?)\])? # Optional block title
                                    (?P<block_contents>.*?) # Non-greedy block contents
                                    \\end{(?P=block_name)}""", # closing block
                                    flags=re.DOTALL + re.VERBOSE)

        # Select all our list blocks
        self._lists_re = re.compile(r"""\\begin{(?P<block_name>enumerate|itemize)} # list name
                                    (\[.*?\])? # Optional enumerate settings i.e. (a)
                                    (?P<block_contents>.*?) # Non-greedy list contents
                                    \\end{(?P=block_name)}""", # closing list
                                    flags=re.DOTALL + re.VERBOSE)

        # Select all our headers
        self._header_re = re.compile(r"""\\(?P<header_name>chapter|section|subsection) # Header
                                    {(?P<header_contents>.*?)}""",  # Header title
                                    flags=re.DOTALL + re.VERBOSE)

        # Select all our 'auxillary blocks' - these need special treatment
        # for future use - e.g. pygments highlighting instead of code blocks
        # in Markdown
        self._aux_block_re = re.compile(r"""\\begin{(?P<block_name>lstlisting)} # block name
                                    (?P<block_contents>.*?) # Non-greedy block contents
                                    \\end{(?P=block_name)}""", # closing block
                                    flags=re.DOTALL + re.VERBOSE)

    def _replace_header(self, matchobj):
        """Creates a header string for a section/subsection/chapter match.
        For example, "### 2 - Integral Calculus\n" """

        header_name = matchobj.group('header_name')
        header_contents = matchobj.group('header_contents')

        header = self._format_block_name(header_name)

        block_config = self._block_configuration[header_name]

        # If we have a count, separate the title from the count with a dash
        separator = "-" if block_config.get("show_count") else ""

        output_str = "{header} {separator} {title}\n".format(
                        header=header,
                        title=header_contents,
                        separator=separator)

        return output_str

    def _replace_block(self, matchobj):
        """Create a string that replaces an entire block.
        The string consists of a header (e.g. ### Exercise 1)
        and a block, containing the LaTeX code.

        The block may be optionally indented, blockquoted, etc.
        These settings are customizable through the config.json
        file"""

        block_name = matchobj.group('block_name')
        block_contents = matchobj.group('block_contents')
        # Block title may not exist, so use .get method
        block_title = matchobj.groupdict().get('block_title')

        # We have to format differently for lists
        if block_name in {"itemize", "enumerate"}:
            formatted_contents = self._format_list_contents(block_name,
                                                        block_contents)
        else:
            formatted_contents = self._format_block_contents(block_name,
                                                        block_contents)

        header = self._format_block_name(block_name, block_title)

        output_str = "{header}\n\n{block_contents}".format(
                        header=header,
                        block_contents=formatted_contents)
        return output_str


    def _format_block_contents(self, block_name, block_contents):
        """Format the contents of a block with configuration parameters
        provided in the self._block_configuration attribute"""

        block_config = self._block_configuration[block_name]

        line_indent_char = block_config["line_indent_char"]

        output_str = ""
        for line in block_contents.lstrip().rstrip().split("\n"):
            line = line.lstrip().rstrip()
            indented_line = line_indent_char + line + "\n"
            output_str += indented_line
        return output_str

    def _format_list_contents(self, block_name, block_contents):
        """To format a list, we must remove the \item declaration in the
        LaTeX source.  All else is as in the _format_block_contents method."""
        block_config = self._block_configuration[block_name]

        list_heading = block_config["list_heading"]

        output_str = ""
        for line in block_contents.lstrip().rstrip().split("\n"):
            line = line.lstrip().rstrip()
            markdown_list_line = line.replace(r"\item", list_heading)
            output_str += markdown_list_line + "\n"
        return output_str

    def _format_block_name(self, block_name, block_title=None):
        """Format the Markdown header associated with a block.
        Due to the optional block_title, we split the string construction
        into two parts."""

        block_config = self._block_configuration[block_name]
        pretty_name = block_config["pretty_name"]
        show_count = block_config["show_count"]
        markdown_heading = block_config["markdown_heading"]

        block_count = self._block_counter[block_name] if show_count else ""
        self._block_counter[block_name] += 1

        output_str = "{markdown_heading} {pretty_name} {block_count}".format(
                        markdown_heading=markdown_heading,
                        pretty_name=pretty_name,
                        block_count=block_count)

        if block_title:
            output_str = "{output_str} ({block_title})".format(
                        output_str=output_str,
                        block_title=block_title)

        return output_str.lstrip().rstrip()

    def _latex_to_markdown(self):
        """Main function, returns the formatted Markdown as a string.
        Uses a lot of custom regexes to fix a lot of content - you may have
        to add or remove some regexes to suit your own needs."""

        # Get main content, skipping preamble and closing tags.
        output = self._main_re.search(self._latex_string).group("main")

        # Reformat, lists, blocks, and headers.
        output = self._lists_re.sub(self._replace_block, output)
        output = self._block_re.sub(self._replace_block, output)
        output = self._header_re.sub(self._replace_header, output)
        output = self._aux_block_re.sub(self._replace_block, output)

        # Fix \\ formatting for line breaks in align blocks
        output = re.sub(r" \\\\", r" \\\\\\\\", output)
        # Convert align* block  to align - this fixes formatting
        output = re.sub(r"align\*", r"align", output)

        # Fix emph, textbf, texttt formatting
        output = re.sub(r"\\emph{(.*?)}", r"*\1*", output)
        output = re.sub(r"\\textbf{(.*?)}", r"**\1**", output)
        output = re.sub(r"\\texttt{(.*?)}", r"`\1`", output)

        # Fix \% formatting
        output = re.sub(r"\\%", r"%", output)
        # Fix argmax, etc.
        output = re.sub(r"\\arg(max|min)", r"\\text{arg\1}", output)

        # Throw away content in IGNORE/END block
        output = re.sub(r"% LaTeX2Markdown IGNORE(.*?)\% LaTeX2Markdown END",
                        "", output, flags=re.DOTALL)
        return output.lstrip().rstrip()
    
    def to_markdown(self):
        return self._latex_to_markdown()
    
    def to_latex(self):
        return self._latex_string
        
#------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        input_file = "examples/latex_sample.tex"
        output_file = "examples/converted_latex_sample.md"
    else:
        input_file, output_file = sys.argv[1], sys.argv[2]
        
    with open(input_file, 'r') as f:
        latex_string = f.read()
        y = LaTeX2Markdown(latex_string)
        markdown_string = y.to_markdown()
        with open(output_file, 'w') as f_out:
            f_out.write(markdown_string)
