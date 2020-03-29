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
    : ( BLOCK_COMMENT | LINE_COMMENT ) -> skip;

/* Keywords */
ALWAYS      : 'always';
BE          : 'be';
BITS        : 'bits';
BYTES       : 'bytes';
CASE        : 'case';
IGNORE      : '_';
LE          : 'le';
OPTIONAL    : 'optional';
OTHERWISE   : 'otherwise';
PACKET      : 'packet';
SINT        : 'sint';
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
PIPE        : '|';
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

module
    : packet* EOF
    ;

packet
    : PACKET IDENT
        ( COLON IDENT
            ( LPAREN cond_exp RPAREN )? )?
      def_block
    ;

cond_exp
    : value
    | LPAREN cond_exp RPAREN
    | LOGIC_NOT cond_exp
    | cond_exp cond_relation cond_exp
    | cond_exp cond_conjunction cond_exp
    ;

cond_relation
    : EQ
    | GT
    | GTE
    | LT
    | LTE
    | NOT_EQ
    ;

cond_conjunction
    : LOGIC_AND
    | LOGIC_OR
    ;

def_block
    : LBRACE
        ( always_statement
        | empty_statement
        | optional_statement
        | variable_statement
        )*
      RBRACE
    ;

always_statement
    : ALWAYS IDENT field_desc SEMI
    ;

empty_statement
    : SEMI
    ;

optional_statement
    : OPTIONAL IDENT WHEN LPAREN cond_exp RPAREN def_block;

variable_statement
    : VARIABLE IDENT case_block;

case_block
    : LBRACE case_statement+ otherwise_statement? RBRACE
    ;

case_statement
    : CASE LPAREN cond_exp RPAREN case_tag def_block
    ;

case_tag
    : PIPE IDENT COLON LITERAL PIPE
    ;

otherwise_statement
    : OTHERWISE case_tag def_block;

field_desc
    : LBRACK scalar_type COLON count ( COLON value )? RBRACK
    | LBRACK scalar_type COLON COLON value RBRACK
    ;

scalar_type
    : IGNORE
    | SINT
    | UINT
    ;

count
    : value units
    ;

value
    : LITERAL
    | resolvable
    ;

resolvable
    : AMP IDENT
    ;

units
    : BYTES (BE|LE)?
    | BITS
    ;
