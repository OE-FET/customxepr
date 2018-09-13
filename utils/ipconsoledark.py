"""
A Pygments style based on the based on Base16 Ocean Dark color scheme.

.. Pygments: http://pygments.org/
.. Base16: https://github.com/chriskempson/base16
"""
from __future__ import unicode_literals, absolute_import
from pygments.style import Style
from pygments.token import (Token, Comment, Name, Keyword, Generic, Number,
                            Operator, String)


BACKGROUND = '# 31363B'
CURRENTLINE = '# 343d46'
SELECTION = '# 4f5b66'
FOREGROUND = '# c0c5ce'
COMMENT = '# 65737e'
RED = '# bf616a'
ORANGE = '# d08770'
YELLOW = '# AFEEFE'
GREEN = '# DAF7A6'
CYAN = '# 8959a8'
BLUE = '# 8fa1b3'
PURPLE = '# b48ead'


class IpconsoledarkStyle(Style):
    background_color = BACKGROUND
    highlight_color = SELECTION

    styles = {
        Keyword: PURPLE,
        Keyword.Constant: ORANGE,
        Keyword.Declaration: BLUE,
        # Keyword.Namespace
        # Keyword.Pseudo
        Keyword.Reserved: BLUE,
        Keyword.Type: RED,

        # Name
        Name.Attribute: FOREGROUND,
        Name.Builtin: YELLOW,
        Name.Builtin.Pseudo: BLUE,
        Name.Class: BLUE,
        Name.Constant: ORANGE,
        Name.Decorator: BLUE,
        Name.Entity: ORANGE,
        Name.Exception: ORANGE,
        Name.Function: BLUE,
        # Name.Label
        # Name.Namespace
        # Name.Other
        Name.Tag: BLUE,
        Name.Variable: BLUE,
        # Name.Variable.Class
        # Name.Variable.Global
        # Name.Variable.Instance

        # Literal
        # Literal.Date
        String: GREEN,
        String.Backtick: FOREGROUND,
        String.Char: GREEN,
        String.Doc: FOREGROUND,
        # String.Double
        String.Escape: ORANGE,
        String.Heredoc: FOREGROUND,
        # String.Interpol
        # String.Other
        String.Regex: RED,
        # String.Single
        # String.Symbol
        Number: ORANGE,
        # Number.Float
        # Number.Hex
        # Number.Integer
        # Number.Integer.Long
        # Number.Oct

        Operator: CYAN,
        # Operator.Word

        # Punctuation: ORANGE,

        Comment: COMMENT,
        # Comment.Multiline
        Comment.Preproc: GREEN,
        # Comment.Single
        Comment.Special: GREEN,

        # Generic
        Generic.Deleted: CYAN,
        Generic.Emph: 'italic',
        Generic.Error: RED,
        Generic.Heading: ORANGE,
        Generic.Inserted: GREEN,
        Generic.Output: BLUE,
        Generic.Prompt: GREEN,
        Generic.Strong: 'bold',
        Generic.Subheading: ORANGE,
        # Generic.Traceback

        Token: FOREGROUND,
        Token.Other: ORANGE,
        Token.Prompt: GREEN,
        Token.PromptNum: GREEN,
        Token.OutPrompt: BLUE,
        Token.OutPromptNum: BLUE,
    }
