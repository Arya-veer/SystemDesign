%{
#include "parse.tab.h"  // Include the Bison-generated header file
%}

%%

[ \t\n]     ;  // Ignore whitespace and newlines
"+"         { return ADD; }
"-"         { return SUB; }
"("         { return LPAREN; }
")"         { return RPAREN; }
[0-9]+      { yylval = atoi(yytext); return NUMBER; } // Assign to yylval.number
.           { printf("Unknown character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}