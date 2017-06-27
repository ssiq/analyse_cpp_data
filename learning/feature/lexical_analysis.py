


keyword_spe_typelist = ('void', 'int', 'char', 'double', 'float', 'bool', 'vector', 'string', 'set', 'long', 'short')
keyword_typelist = ('class', 'struct', 'enum', 'namespace', 'operator', 'template', 'typename')
keyword_modifiedlist = ('const', 'extern', 'static', 'auto', 'explicit', 'export', 'friend', 'inline', 'mutable', 'new', 'private', 'protected', 'public', 'register', 'signed', 'unsigned', 'virtual', 'union')
keyword_funclist = ('typedef', 'const_case', 'dynamic_cast', 'static_cast', 'reinterpret_cast', 'sizeof')
keyword_grammarlist = ('if', 'else', 'switch', 'case', 'default', 'for', 'do', 'while', 'continue', 'break', 'try', 'catch', 'throw', 'delete', 'return', 'goto', 'typeid', 'using')
keyword_valuelist = ('TRUE', 'FALSE', 'this')
operator_calculatelist = ('=', '+', '-', '*', '/', '%', '++', '--', '+=', '-=', '*=', '/=', '%=', '<<', '>>', '&', '|', '^', '&=', '|=', '^=')
operator_comparelist = ('!', '<', '>', '<=', '>=', '==', '!=', '&&', '||')
symbol_bounderlist = ('(', ')', '[', ']', '{', '}', '.', ',', '#', '_', ';', '\'', '"', '->', '::', ':', '?', '~')
symbol_notelist = ('/*', '*/', '//')
wordlist = ('标识符', '数字', '常量', '注释')


class TokenType:
    VOID = 1
    INT = 2
    CHAR = 3
    DOUBLE = 4
    FLOAT = 5
    BOOL = 6
    VECTOR = 7
    STRING = 8
    SET = 9
    LONG = 10
    SHORT = 11

    CLASS = 21
    STRUCT = 22
    ENUM = 23
    NAMESPACE = 24
    OPERATOR = 25
    TEMPLATE = 26
    TYPENAME = 27

    CONST = 31
    EXTERN = 32
    STATIC = 33
    AUTO = 34
    EXPLICIT = 35
    EXPORT = 36
    FRIEND = 37
    INLINE = 38
    MUTABLE = 39
    NEW = 40
    PRIVATE = 41
    PROTECTED = 42
    PUBLIC = 43
    REGISTER = 44
    SIGNED = 45
    UNSIGNED = 46
    VIRTUAL = 47
    UNION = 48

    TYPEDEF = 51
    CONST_CAST = 52
    DYNAMIC_CAST = 53
    STATIC_CAST = 54
    REINTERPRET_CAST = 55
    SIZEOF = 56

    IF = 61
    ELSE = 62
    SWITCH = 63
    CASE = 64
    DEFAULT = 65
    FOR = 66
    DO = 67
    WHILE = 68
    CONTINUE = 69
    BREAK = 70
    TRY = 71
    CATCH = 72
    THROW = 73
    DELETE = 74
    RETURN = 75
    GOTO = 76
    TYPEID = 77
    USING = 78

    TRUE = 81
    FALSE = 82
    THIS = 83

    ASG = 91             # =
    PLUS = 92            # +
    MINUS = 93           # -
    MUL = 94             # *
    DIV = 95             # /
    MOD = 96             # %
    SELF_PLUS = 97       # ++
    SELF_MINUS = 98      # --
    COMPLETE_PLUS = 99   # +=
    COMPLETE_MINUS = 100  # -=
    COMPLETE_MUL = 101    # *=
    COMPLETE_DIV = 102    # /=
    COMPLETE_MOD = 103    # %=
    LEFT_MOVE = 104       # <<
    RIGHT_MOVE = 105      # >>
    BYTE_AND = 106        # &
    BYTE_OR = 107         # |
    BYTE_XOR = 108        # ^
    NEGATE = 109          # ~
    COMPLETE_BYTE_AND = 110   # &=
    COMPLETE_BYTE_OR = 111    # |=
    COMPLETE_BYTE_XOR = 112   # ^=
    COMPLETE_NEGATE = 113     # ~=

    NOT = 121             # !
    LES_THAN = 122        # <
    GRT_THAN = 123        # >
    LES_EQUAL = 124       # <=
    GRT_EQUAL = 125       # >=
    EQUAL = 126           # ==
    NOT_EQUAL = 127       # !=
    AND = 128             # &&
    OR = 129              # ||

    LEFT_BRA = 131        # (
    RIGHT_BRA = 132       # )
    LEFT_INDEX = 133      # [
    RIGHT_INDEX = 134     # ]
    LEFT_BOUNDER = 135    # {
    RIGHT_BOUNDER = 136   # }
    POINTER = 137         # .
    COMMA = 138           # ,
    JING = 139            # #
    UNDER_LINE = 140      # _
    SEMI = 141            # ;
    SIG_QUE = 142         # '
    DOU_QUE = 143         # "
    ARROW = 144           # ->
    SCOPE = 145           # ::
    COLON = 146           # :
    QUES = 147            # ?

    NOTE1 = 151           # /*
    NOTE1_END = 152       # */
    NOTE2 = 153           # //

    IDENTIFIER = 161       # 标识符
    NUMBER = 162          # 数字
    CONSTANT = 163        # "常量"
    NOTE = 164            # 注释

    ERROR_IDENTIFIER = 171 # 错误的标识符
    ERROR_NUMBER = 172     # 错误的数字




def search_key(content):
    init_keyword_spe_typelist = 1
    init_keyword_typelist = 21
    init_keyword_modifiedlist = 31
    init_keyword_funclist = 51
    init_keyword_grammarlist = 61
    init_keyword_valuelist = 81

    base = init_keyword_spe_typelist
    for i in range(0, len(keyword_spe_typelist)):
        if keyword_spe_typelist[i] == content:
            return base + i

    base = init_keyword_typelist
    for i in range(0, len(keyword_typelist)):
        if keyword_typelist[i] == content:
            return base + i

    base = init_keyword_modifiedlist
    for i in range(0, len(keyword_modifiedlist)):
        if keyword_modifiedlist[i] == content:
            return base + i

    base = init_keyword_funclist
    for i in range(0, len(keyword_funclist)):
        if keyword_funclist[i] == content:
            return base + i

    base = init_keyword_grammarlist
    for i in range(0, len(keyword_grammarlist)):
        if keyword_grammarlist[i] == content:
            return base + i

    base = init_keyword_valuelist
    for i in range(0, len(keyword_valuelist)):
        if keyword_valuelist[i] == content:
            return base + i

    return -1


def add_token(key_id, key_value, tokens):
    #print(key_id, key_value)
    tokens.append({'id': key_id, 'value': key_value})


def get_token_list(content):

    n = len(content)
    i = 0
    token_list = []

    while i < n:
        c = content[i]
        i += 1

        #处理字符串
        if ('A' <= c <= 'Z') or ('a' <= c <= 'z') or ('_' == c):
            token_str = ''
            token_str += c

            while i < n:
                t = content[i]
                i += 1
                if ('A' <= t <= 'Z') or ('a' <= t <= 'z') or ('_' == t) or ('0' <= t <= '9'):
                    token_str += t
                else:
                    i -= 1
                    break

            keyid = search_key(token_str)
            if keyid != -1:
                add_token(keyid, token_str, token_list)
            else:
                add_token(TokenType.IDENTIFIER, token_str, token_list)
        elif '0' <= c <= '9':
            token_str = ''
            token_str += c
            point_num = 0

            while i < n:
                t = content[i]
                i += 1
                if '0' <= t <= '9':
                    token_str += t
                elif t == '.':
                    point_num += 1
                    token_str += t
                else:
                    i -= 1
                    break

            if point_num >1:
                add_token(TokenType.ERROR_NUMBER, token_str, token_list)
            else:
                add_token(TokenType.NUMBER, token_str, token_list)
        elif c == '/' and i < n and content[i] == '*':
            add_token(TokenType.NOTE1, '/*', token_list)
            i += 1

            token_str = ''
            while i<n:
                t = content[i]
                i += 1
                if t == '*' and i < n and content[i] == '/':
                    add_token(TokenType.NOTE, token_str, token_list)
                    add_token(TokenType.NOTE1_END, '*/', token_list)
                    i += 1
                    break
                else:
                    token_str += t
        elif c == '/' and i < n and content[i] == '/':
            add_token(TokenType.NOTE2, '//', token_list)
            i += 1

            token_str = ''
            while i < n:
                t = content[i]
                i += 1
                if t == '\n':
                    add_token(TokenType.NOTE, token_str, token_list)
                    break
                else:
                    token_str += t
        elif c == '"':
            add_token(TokenType.DOU_QUE, '"', token_list)

            token_str = ''
            while i<n:
                t = content[i]
                i += 1
                if t == '\\' and i < n and content[i] == '"':
                    token_str +=t
                    token_str += content[i]
                    i += 1
                elif t == '"':
                    add_token(TokenType.CONSTANT, token_str, token_list)
                    add_token(TokenType.DOU_QUE, '"', token_list)
                    break
                else:
                    token_str += t

        elif c == ' ' or c == '\t' or c == '\r' or c == '\n':
            pass

        elif c == '=' and i < n and content[i] == '=':
            add_token(TokenType.EQUAL, '==', token_list)
            i += 1
        elif c == '=':
            add_token(TokenType.ASG, '=', token_list)

        elif c == '+' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_PLUS, '+=', token_list)
            i += 1
        elif c == '+' and i < n and content[i] == '+':
            add_token(TokenType.SELF_PLUS, '++', token_list)
            i += 1
        elif c == '+':
            add_token(TokenType.PLUS, '+', token_list)

        elif c == '-' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_MINUS, '-=', token_list)
            i += 1
        elif c == '-' and i < n and content[i] == '-':
            add_token(TokenType.SELF_MINUS, '--', token_list)
            i += 1
        elif c == '-' and i < n and content[i] == '>':
            add_token(TokenType.ARROW, '->', token_list)
            i += 1
        elif c == '-':
            add_token(TokenType.MINUS, '-', token_list)

        elif c == '*' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_MUL, '*=', token_list)
            i += 1
        elif c == '*':
            add_token(TokenType.MUL, '*', token_list)

        elif c == '/' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_DIV, '/=', token_list)
            i += 1
        elif c == '/':
            add_token(TokenType.DIV, '/', token_list)

        elif c == '%' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_MOD, '%=', token_list)
            i += 1
        elif c == '%':
            add_token(TokenType.MOD, '%', token_list)

        elif c == '<' and i < n and content[i] == '<':
            add_token(TokenType.LEFT_MOVE, '<<', token_list)
            i += 1
        elif c == '>' and i < n and content[i] == '>':
            add_token(TokenType.RIGHT_MOVE, '>>', token_list)

        elif c == '&' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_BYTE_AND, '&=', token_list)
            i += 1
        elif c == '&' and i < n and content[i] == '&':
            add_token(TokenType.AND, '&&', token_list)
            i += 1
        elif c == '&':
            add_token(TokenType.BYTE_AND, '&', token_list)

        elif c == '|' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_BYTE_OR, '|=', token_list)
            i += 1
        elif c == '|' and i < n and content[i] == '|':
            add_token(TokenType.OR, '||', token_list)
            i += 1
        elif c == '|':
            add_token(TokenType.BYTE_OR, '|', token_list)

        elif c == '^' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_BYTE_XOR, '^=', token_list)
            i += 1
        elif c == '^':
            add_token(TokenType.BYTE_XOR, '^', token_list)

        elif c == '~' and i < n and content[i] == '=':
            add_token(TokenType.COMPLETE_NEGATE, '~=', token_list)
            i += 1
        elif c == '~':
            add_token(TokenType.NEGATE, '~', token_list)

        elif c == '!' and i < n and content[i] == '=':
            add_token(TokenType.NOT_EQUAL, '!=', token_list)
            i += 1
        elif c == '!':
            add_token(TokenType.NOT, '!', token_list)

        elif c == '<' and i < n and content[i] == '=':
            add_token(TokenType.LES_EQUAL, '<=', token_list)
            i += 1
        elif c == '<':
            add_token(TokenType.LES_THAN, '<', token_list)

        elif c == '>' and i < n and content[i] == '=':
            add_token(TokenType.GRT_EQUAL, '>=', token_list)
            i += 1
        elif c == '>':
            add_token(TokenType.GRT_THAN, '>', token_list)

        elif c == '(':
            add_token(TokenType.LEFT_BRA, '(', token_list)
        elif c == ')':
            add_token(TokenType.RIGHT_BRA, ')', token_list)

        elif c == '[':
            add_token(TokenType.LEFT_INDEX, '[', token_list)
        elif c == ']':
            add_token(TokenType.RIGHT_INDEX, ']', token_list)

        elif c == '{':
            add_token(TokenType.LEFT_BOUNDER, '{', token_list)
        elif c == '}':
            add_token(TokenType.RIGHT_BOUNDER, '}', token_list)

        elif c == '.':
            add_token(TokenType.POINTER, '.', token_list)
        elif c == ',':
            add_token(TokenType.COMMA, ',', token_list)
        elif c == '#':
            add_token(TokenType.JING, '#', token_list)
        elif c == '_':
            add_token(TokenType.UNDER_LINE, '_', token_list)
        elif c == ';':
            add_token(TokenType.SEMI, ';', token_list)
        elif c == '\'':
            add_token(TokenType.SIG_QUE, '\'', token_list)
        elif c == ':' and i < n and content[i] == ':':
            add_token(TokenType.SCOPE, '::', token_list)
            i += 1
        elif c == ':':
            add_token(TokenType.COLON, ':', token_list)
        elif c == '?':
            add_token(TokenType.QUES, '?', token_list)

    return token_list






