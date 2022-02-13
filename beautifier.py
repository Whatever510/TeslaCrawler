""" This script beautifies a javascript file and makes it human-readable """
import jsbeautifier



def beautify_js(text, filename):
    """
    Make the JS Section human readable
    :param text: the text/ string to be beautified
    :param filename: the file to write to
    """
    opts = jsbeautifier.default_options()
    opts.indent_size = 4
    opts.indent_char = " "
    opts.max_preserve_newlines = 10
    opts.preserve_newlines = True
    opts.keep_array_indentation = False
    opts.break_chained_methods = False
    opts.indent_scripts = "normal"
    opts.brace_style = "none"
    opts.space_before_conditional = False
    opts.unescape_strings = False
    opts.jsling_happy = False
    opts.end_with_newline = False
    opts.wrap_line_length = 160
    opts.indent_inner_html = False
    opts.comma_first = False
    opts.e4x = False
    opts.indent_empty_lines = False

    res = jsbeautifier.beautify(text, opts=opts)
    with open(filename, "w", encoding="utf-8") as text_file:
        text_file.write(res)
