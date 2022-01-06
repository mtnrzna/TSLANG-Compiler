# compiler #ply #python #AST #abstract_syntax_tree #BNF #visitor_design_pattern

Front end of a compiler for a phony language called "teslang" using PLY.

Front end of this compiler contains: lexical analysis, syntax analysis and semantic analysis.

-Lexical analysis here is done with lex.py from PLY package. Tokens and reserved tokens were defined using Regex and handed over to the lex.py

-Syntax analysis contains defining "teslang" grammar using BNF as described in PLY documantation and finally handing this grammar over to yacc.py.
I also used syntax error handling using error token. After reduction of each rule, the syntax tree and abstract synta tree, AST, of that node is created. abstract syntax tree is printed in the console as a tree, usuing "anytree" library and AST is being used for the next section.

-In semantic analysis I traversed AST and first fill the symbol table with function and variable definitions in preprocess.py and then with traversing the AST for the second time I filled the symbol table using rest of the code. Traversing the AST is done using visitor design pattern. Also the preprocess action results in the "forward referencing" feature.



BNF sample used in parser: "func : FUNCTION iden LPARANT flist RPARANT RETURNS type COLON body END"

Syntax tree sample created in parser:
prog
└── func
    ├── function
    ├── iden
    │   └── find
    ├── (
    ├── flist
    │   ├── type
    │   │   └── Array
    │   └── iden
    │       └── A
    .
    .
    .




-This project was my assignment from "Compiler Design" course in university. 
Uni.: Babol Noshirvani University of Technology (BNUT), Prof.:Dr.Ali Gholami Rudi 

-Matin Rezania
Jan of 2022





ref.: https://www.dabeaz.com/ply/ply.html