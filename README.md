# NeuroPY

This is our project made with PLY, which is a reimplementation of the classical lex-yacc combo.

## Status

So far the lexer and parser have an initial implementation, that allows them to recognize specific patterns in their input.

- Lex.py contains the lexer/scanner: A module to convert characters (user input) into tokens which are fed to the parser
- Yacc.py contains the parser: A module to convert tokens into a specialized tree data structure.
- SemanticCube.py contains the semantic cube, which is a data structure that stores the type compatibility of different operators in a programming language.
  In this case, the cube is defined for the types "INT", "FLOAT", and "STRING", and for each type, it specifies which operators are compatible with which other types.
- Quadruple.py contains a data structure used in compiler construction to store information about operations to be performed on operands. It contains information such as the operator, left and right operands, and the result

## Authors

- Juventino Gutierrez Romo A01250658
