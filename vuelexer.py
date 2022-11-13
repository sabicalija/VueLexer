import re

from pygments.lexer import RegexLexer, bygroups, include, default, using
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.html import HtmlLexer
from pygments.lexers.css import CssLexer
from pygments.token import Token, Comment, Name, Number, Operator, Keyword, Punctuation, String, Text, Literal
import pygments.unistring as uni

# Vue Tokens
Vue = Token.Vue
RegExp = Token.RegExp
# Directive = Vue.Directive
# Properties = Vue.Properties

JS_IDENT_START = ('(?:[$_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') +
                  ']|\\\\u[a-fA-F0-9]{4})')
JS_IDENT_PART = ('(?:[$' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl',
                                       'Mn', 'Mc', 'Nd', 'Pc') +
                 u'\u200c\u200d]|\\\\u[a-fA-F0-9]{4})')
JS_IDENT = JS_IDENT_START + '(?:' + JS_IDENT_PART + ')*'

class EcmaScriptLexer(RegexLexer):
    name = 'EcmaScript'
    aliases = ['js', 'javascript']
    filenames = ['*.js', '*.jsm']
    mimetypes = ['application/javascript', 'application/x-javascript',
                 'text/x-javascript', 'text/javascript']

    flags = re.DOTALL | re.UNICODE | re.MULTILINE

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'<!--', Comment),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline)
        ],
        'slashstartsregex': [
            include('commentsandwhitespace'),
            ('/', RegExp.Slash, "regex"),
            (r'/(\\.|[^[/\\\n]|\[(\\.|[^\]\\\n])*])+/'r'([gismuy]+\b|\B)', String.Regex, '#pop'),
            (r'(?=/)', Text, ('#pop', 'badregex')),
            default('#pop')
        ],
        'regex': [
            (r'(\/)([ismg]*)', bygroups(RegExp.Slash, RegExp.Modifier), '#pop'),
            (r'\?|\.|\*', RegExp.Special),
            (r'\(|\)', RegExp.Groups),
            (r'\\.', RegExp.Escape),
            (r'.', RegExp.String)
        ],
        'badregex': [
            (r'\n', Text, '#pop')
        ],
        'vue': [
            (r'(Vue)(\()', bygroups(Vue.Class, Punctuation)),
        ],
        'vue-props': [
            (r'(data)(\(\))', bygroups(Vue.Instance, Punctuation)),
            (r'(data|el|methods|computed|watch|created|mounted)(\:|\()', bygroups(Vue.Instance, Operator)),
        ],
        'node': [
            (r'(Stream|Buffer|Server|require)\b', Name.Builtin),
            (r'(module)(\.)(exports)\b', bygroups(Name.Builtin, Punctuation, Name.Builtin)),
        ],
        'js-fix': [
            include('node'),
            (r'(return|default|try|catch|if|while|do|switch|for)\b', Keyword.Reserved, 'slashstartsregex'),
            (r'(const|debugger)\b', Keyword, 'slashstartsregex'),
            (r'(console)\b', Name.Builtin),
        ],
        'root': [
            include('vue'),
            include('vue-props'),
            include('js-fix'),
            (r'\A#! ?/.*?\n', Comment.Hashbang),  # recognized by node.js
            (r'^(?=\s|/|<!--)', Text, 'slashstartsregex'),
            include('commentsandwhitespace'),
            (r'(\.\d+|[0-9]+\.[0-9]*)([eE][-+]?[0-9]+)?', Number.Float),
            (r'0[bB][01]+', Number.Bin),
            (r'0[oO][0-7]+', Number.Oct),
            (r'0[xX][0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),
            (r'\.\.\.|=>', Operator),
            (r'\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|'
             r'(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?', Operator, 'slashstartsregex'),
            (r'[{(\[;,]', Punctuation, 'slashstartsregex'),
            (r'[})\].]', Punctuation),
            (r'(for|in|while|do|break|return|continue|switch|case|default|if|else|'
             r'throw|try|catch|finally|new|delete|typeof|instanceof|void|yield|'
             r'this|of)\b', Keyword, 'slashstartsregex'),
            (r'(var|let|with|function)\b', Keyword.Declaration, 'slashstartsregex'),
            (r'(abstract|boolean|byte|char|class|const|debugger|double|enum|export|'
             r'extends|final|float|goto|implements|import|int|interface|long|native|'
             r'package|private|protected|public|short|static|super|synchronized|throws|'
             r'transient|volatile)\b', Keyword.Reserved),
            (r'(true|false|null|NaN|Infinity|undefined)\b', Keyword.Constant),
            (r'(Array|Boolean|Date|Error|Function|Math|netscape|'
             r'Number|Object|Packages|RegExp|String|Promise|Proxy|sun|decodeURI|'
             r'decodeURIComponent|encodeURI|encodeURIComponent|'
             r'Error|eval|isFinite|isNaN|isSafeInteger|parseFloat|parseInt|'
             r'document|this|window)\b', Name.Builtin),
            (r'(\w+)(\s)*(\()', bygroups(Name.Function, Text.Whitespace, Punctuation), 'slashstartsregex'),
            (JS_IDENT, Name.Other),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
            (r'`', String.Backtick, 'interp'),
        ],
        'interp': [
            (r'`', String.Backtick, '#pop'),
            (r'\\\\', String.Backtick),
            (r'\\`', String.Backtick),
            (r'\$\{', String.Interpol, 'interp-inside'),
            (r'\$', String.Backtick),
            (r'[^`\\$]+', String.Backtick),
        ],
        'interp-inside': [
            # TODO: should this include single-line comments and allow nesting strings?
            (r'\}', String.Interpol, '#pop'),
            include('root'),
        ],
        # (\\\\|\\`|[^`])*`', String.Backtick),
    }

class VueLexer(RegexLexer):
    name = 'vue'
    aliases = ['vue', 'vuejs']
    filenames = ['*.vue']
    mimetypes = ['text/x-vue', 'application/x-vue']

    flags = re.MULTILINE | re.DOTALL | re.UNICODE

    tokens = {
        'root': [
            # ('^[^<&]+', using(EcmaScriptLexer)),
            # ('^(?!<)[^&]+', using(EcmaScriptLexer)),
            (r'^(?![^<])', Text, 'html-vue'),
            ('.*', using(EcmaScriptLexer)),
            # default('html-vue'),
        ],
        'html-vue': [
            # (r'({{)(\s*)(.*)(\s*)(}})', bygroups(Punctuation, Text, using(EcmaScriptLexer), Text, Punctuation), '#push'),
            (r'({{)(.*?)(}})', bygroups(Punctuation, using(EcmaScriptLexer), Punctuation), 'html-vue'),
            ('[^<{]+', Text),
            # ('{', Punctuation, 'expression'),
            (r'&\S*?;', Name.Entity),
            (r'\<\!\[CDATA\[.*?\]\]\>', Comment.Preproc),
            ('<!--', Comment, 'comment'),
            (r'<\?.*?\?>', Comment.Preproc),
            ('<![^>]*>', Comment.Preproc),
            (r'(<)(\s*)(script)(\s*)', bygroups(Punctuation, Text, Name.Tag, Text), ('script-content', 'tag')),
            (r'(<)(\s*)(style)(\s*)', bygroups(Punctuation, Text, Name.Tag, Text), ('style-content', 'tag')),
            # note: this allows tag names not used in HTML like <x:with-dash>,
            # this is to support yet-unknown template engines and the like
            (r'(<)(\s*)([\w:.-]+)', bygroups(Punctuation, Text, Name.Tag), 'tag'),
            (r'(<)(\s*)(/)(\s*)([\w:.-]+)(\s*)(>)', bygroups(Punctuation, Text, Punctuation, Text, Name.Tag, Text, Punctuation)),
        ],
        'comment': [
            ('[^-]+', Comment),
            ('-->', Comment, '#pop'),
            ('-', Comment),
        ],
        'tag': [
            (r'\s+', Text),
            include('vue-template'),
            (r'([\w:-]+\s*)(=)(\s*)', bygroups(Name.Attribute, Operator, Text), 'attr'),
            (r'[\w:-]+', Name.Attribute),
            (r'(/?)(\s*)(>)', bygroups(Punctuation, Text, Punctuation), '#pop'),
        ],
        'vue-template': [
            (r'(ref)(=)(".*?")', bygroups(Vue.Directive, Operator, String)),
            (r'(v-for)(=)(")(.*?)(")', bygroups(Vue.Directive, Operator, Vue.Directive, using(EcmaScriptLexer), Vue.Directive)),
            (r'(v-(?:|model|if))(=)(")(.*?)(")', bygroups(Vue.Directive, Operator, Vue.Directive, using(EcmaScriptLexer), Vue.Directive)),
            (r'(:style)(\s*)(=)(\s*)(")(\s*)(.*?)(")', bygroups(Vue.Directive, Text, Operator, Text, Vue.Directive, Text, using(EcmaScriptLexer), Vue.Directive)),
            (r'(v-bind:)(\w+)(\s*)(=)(\s*)(")(\s*)(.*?)(")', bygroups(Vue.Directive, Name.Attribute, Text, Operator, Text, Vue.Directive, Text, using(EcmaScriptLexer), Vue.Directive)),
            (r'(v-on:)(.*?)(\s*)(=)(\s*)(")(.*?)(")', bygroups(Vue.Directive, Name.Attribute, Text, Operator, Text, Vue.Directive, using(EcmaScriptLexer), Vue.Directive)),
            (r'(@)(.*?)(\s*)(=)(\s*)(")(.*?)(")', bygroups(Vue.Directive, Name.Attribute, Text, Operator, Text, Vue.Directive, using(EcmaScriptLexer), Vue.Directive)),
        ],
        'script-content': [
            (r'(<)(\s*)(/)(\s*)(script)(\s*)(>)', bygroups(Punctuation, Text, Punctuation, Text, Name.Tag, Text, Punctuation), '#pop'),
            (r'.+?(?=<\s*/\s*script\s*>)', using(EcmaScriptLexer)),
        ],
        'style-content': [
            (r'(<)(\s*)(/)(\s*)(style)(\s*)(>)', bygroups(Punctuation, Text, Punctuation, Text, Name.Tag, Text, Punctuation),'#pop'),
            (r'.+?(?=<\s*/\s*style\s*>)', using(CssLexer)),
        ],
        'attr': [
            ('{', Punctuation, 'expression'),
            ('".*?"', String, '#pop'),
            ("'.*?'", String, '#pop'),
            (r'[^\s>]+', String, '#pop'),
        ],
        'expression': [
            ('{', Punctuation, '#push'),
            ('}', Punctuation, '#pop'),
            # ('.*', using(EcmaScriptLexer)),
            # include('root')
            default('#pop')
        ]
    }