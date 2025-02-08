%{
#include <stdio.h>
#include <stdlib.h>

// Function to report errors
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

// Declare the lexer function
int yylex();
%}

// Define the tokens
%token NUMBER
%token ADD SUB
%token LPAREN RPAREN

// Define precedence and associativity
%left ADD SUB
%left LPAREN RPAREN

%%

// Grammar rules
expression:
    NUMBER                  { printf("Number: %d\n", $1); }
    | LPAREN expression RPAREN
    | expression ADD expression { $$ = $1 + $3; printf("Sum: %d\n", $$); }
    | expression SUB expression { $$ = $1 - $3; printf("Difference: %d\n", $$);}
    ;

%%

int main() {
    printf("Enter an expression: ");
    yyparse();
    return 0;
}