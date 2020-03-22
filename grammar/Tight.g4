grammar Tight;

/**************************************************
 * Lexer Rules
 **************************************************/

/* Comments */
fragment BLOCK_COMMENT
    : '/*' .*? '*/'
    ;

fragment LINE_COMMENT
    : '//' ~('\r'|'\n')*
    ;

COMMENT
    : BLOCK_COMMENT
    | LINE_COMMENT
    ;

/* Keywords */
ALWAYS      : 'always';
BE          : 'be';
BITS        : 'bits';
BYTES       : 'bytes';
IGNORE      : '_';
LE          : 'le';
OPTIONAL    : 'optional';
OTHERWISE   : 'otherwise';
PACKET      : 'packet';
SINT        : 'sint';
STR         : 'str';
UINT        : 'uint';
VARIABLE    : 'variable';
WHEN        : 'when';

/* Letters and Digits */
fragment DECIMAL_DIGIT
    : [0-9]
    ;

fragment HEX_DIGIT
    : [0-9A-Fa-f]
    ;

fragment LETTER
    : [A-Za-z_]
    ;

fragment OCTAL_DIGIT
    : [0-7]
    ;

/* Literals and Identifers */
fragment DECIMAL_LITERAL
    : [1-9] DECIMAL_DIGIT*
    ;

fragment HEX_LITERAL
    : '0' ('x'|'X') HEX_DIGIT+
    ;

fragment OCTAL_LITERAL
    : '0' OCTAL_DIGIT*
    ;

IDENT
    : LETTER (LETTER|DECIMAL_DIGIT)*
    ;

LITERAL
    : DECIMAL_LITERAL
    | HEX_LITERAL
    | OCTAL_LITERAL
    ;

/* Separators */
LBRACE      : '{';
LBRACK      : '[';
LPAREN      : '(';
RBRACE      : '}';
RBRACK      : ']';
RPAREN      : ')';

/* Operators */
AMP         : '&';
COLON       : ':';
EQ          : '==';
GT          : '>';
GTE         : '>=';
LOGIC_AND   : '&&';
LOGIC_NOT   : '!';
LOGIC_OR    : '||';
LT          : '<';
LTE         : '<=';
NOT_EQ      : '!=';
SEMI        : ';';

/* Whitespace */
WHITESPACE  : [ \t\r\n]+ -> skip;

/**************************************************
 * Parser Rules
 **************************************************/

tight
    : empty_statement
    ;

empty_statement
    : SEMI
    ;
