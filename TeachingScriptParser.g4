parser grammar TeachingScriptParser;

options { tokenVocab=TeachingScriptLexer; }

program : lesson EOF ;

lesson : LESSON STRING LBRACE statement* RBRACE ;

statement
    : datasetStmt
    | testStmt
    | checkpointStmt
    | rollbackStmt
    | addExamplesStmt
    ;

datasetStmt     : DATASET STRING ;
testStmt        : TEST ;
checkpointStmt  : CHECKPOINT STRING ;
rollbackStmt    : ROLLBACK STRING ;
addExamplesStmt : ADD_EXAMPLES LBRACE example* RBRACE ;

example       : featureVector ARROW STRING ;
featureVector : LBRACKET NUMBER (COMMA NUMBER)* RBRACKET ;