import re
from collections import defaultdict

#------------------------------------------------------------------------------

import json

with open("config.json", "r") as f:
    _block_configuration = json.load(f)


#------------------------------------------------------------------------------

class LaTeX2Markdown(object):
    def __init__(self,  latex_string, 
                        block_configuration = _block_configuration, 
                        block_counter = defaultdict(lambda: 1)):
        self._block_configuration = block_configuration
        self._latex_string = latex_string
        self._block_counter = block_counter
        self._main_re = re.compile(r"""\\begin{document}
                                    (?P<main>.*)
                                    \\end{document}""", 
                                    flags=re.DOTALL + re.VERBOSE)

        self._block_re = re.compile(r"""\\begin{(?P<block_name>exer|proof|thm|lem|prop)} # block name
                                    (\[(?P<block_title>.*?)\])? # Optional block title
                                    (?P<block_contents>.*?) # Non-greedy block contents
                                    \\end{(?P=block_name)}""", # closing block
                                    flags=re.DOTALL + re.VERBOSE)

        self._lists_re = re.compile(r"""\\begin{(?P<block_name>enumerate|itemize)} # list name
                                    (\[.*?\])? # Optional enumerate settings i.e. (a)
                                    (?P<block_contents>.*?) # Non-greedy list contents
                                    \\end{(?P=block_name)}""", # closing list
                                    flags=re.DOTALL + re.VERBOSE)

        self._header_re = re.compile(r"""\\(?P<header_name>chapter|section|subsection) # Header
                                    {(?P<header_contents>.*?)}""",  # Header title
                                    flags=re.DOTALL + re.VERBOSE)

        self._aux_block_re = re.compile(r"""\\begin{(?P<block_name>lstlisting)} # block name
                                    (?P<block_contents>.*?) # Non-greedy block contents
                                    \\end{(?P=block_name)}""", # closing block
                                    flags=re.DOTALL + re.VERBOSE)

    def _replace_header(self, matchobj):
        header_name = matchobj.group('header_name')
        header_contents = matchobj.group('header_contents')
        
        header = self._format_block_name(header_name)
        
        block_config = self._block_configuration[header_name]
        separator = "-" if block_config.get("show_count") else ""
        
        return "{header} {separator} {title}\n".format(header=header, title=header_contents, separator=separator)

    def _replace_block(self, matchobj):
        block_name = matchobj.group('block_name')
        block_contents = matchobj.group('block_contents')
        block_title = matchobj.groupdict().get('block_title')
        
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
        block_config = self._block_configuration[block_name]
        
        line_indent_char = block_config["line_indent_char"]
    
        output_str = ""
        for line in block_contents.lstrip().rstrip().split("\n"):
            line = line.lstrip().rstrip() 
            indented_line = line_indent_char + line + "\n"
            output_str += indented_line   
        return output_str

    def _format_list_contents(self, block_name, block_contents):
        block_config = self._block_configuration[block_name]
        
        list_heading = block_config["list_heading"]
    
        output_str = ""
        for line in block_contents.lstrip().rstrip().split("\n"):
            line = line.lstrip().rstrip() 
            markdown_list_line = line.replace(r"\item", list_heading)
            output_str += markdown_list_line + "\n"
        return output_str
    
    def _format_block_name(self, block_name, block_title=None):
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
        
    def latex_to_markdown(self):
        # Get main content, skipping preamble and closing tags.
        output = self._main_re.search(self._latex_string).group("main")
    
        # Reformat, lists, blocks, and headers.
        output = self._lists_re.sub(self._replace_block, output)
        output = self._block_re.sub(self._replace_block, output)
        output = self._header_re.sub(self._replace_header, output)
        output = self._aux_block_re.sub(self._replace_block, output)
    
        # Fix \\ formatting for line breaks in align blocks  
        output = re.sub(r" \\\\", r" \\\\\\\\", output)
        # Fix Align* block formatting
        output = re.sub(r"align\*", r"align", output)
        # Fix emph{} formatting
        output = re.sub(r"\\emph{(.*?)}", r"*\1*", output)
        # Fix \% formatting
        output = re.sub(r"\\%", r"%", output)
        # Fix argmax, etc.
        output = re.sub(r"\\arg(max|min)", r"\\text{arg\1}", output)
        # Throw away content in IGNORE/END block
        output = re.sub(r"% LaTeX2Markdown IGNORE(.*?)\% LaTeX2Markdown END", 
                        "", output, flags=re.DOTALL)
        return output

#------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        input_file = "latex_sample.tex"
        output_file = "converted_latex_sample.md"
    else:
        input_file, output_file = sys.argv[1], sys.argv[2]
        
    with open(input_file, 'r') as f:
        latex_string = f.read()
        y = LaTeX2Markdown(latex_string)
        markdown_string = y.latex_to_markdown().lstrip().rstrip()
        with open(output_file, 'w') as f_out:
            f_out.write(markdown_string)
    