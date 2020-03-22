grammar Tight;

/**************************************************
 * Lexer Rules
 **************************************************/

/* Keywords */
ALWAYS      : 'always';
BITS        : 'bits';
BYTES       : 'bytes';
OPTIONAL    : 'optional';
OTHERWISE   : 'otherwise';
PACKET      : 'packet';
SINT        : 'sint';
STR         : 'str';
UINT        : 'uint';
VARIABLE    : 'variable';
WHEN        : 'when';

/* Separators */
AMP         : '&';
COLON       : ':';
LBRACE      : '{';
LBRACK      : '[';
LCHEVR      : '<';
LPAREN      : '(';
RBRACE      : '}';
RBRACK      : ']';
RCHEVR      : '>';
RPAREN      : ')';
SEMI        : ';';

/**************************************************
 * Parser Rules
 **************************************************/

tight
    : empty_statement
    ;

empty_statement
    : SEMI
    ;
