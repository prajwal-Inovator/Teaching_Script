# Generated from TeachingScriptParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,16,78,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,1,0,1,0,1,0,1,1,1,1,1,1,1,1,5,1,28,8,1,
        10,1,12,1,31,9,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,3,2,40,8,2,1,3,1,3,
        1,3,1,4,1,4,1,5,1,5,1,5,1,6,1,6,1,6,1,7,1,7,1,7,5,7,56,8,7,10,7,
        12,7,59,9,7,1,7,1,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,5,9,71,8,9,10,
        9,12,9,74,9,9,1,9,1,9,1,9,0,0,10,0,2,4,6,8,10,12,14,16,18,0,0,74,
        0,20,1,0,0,0,2,23,1,0,0,0,4,39,1,0,0,0,6,41,1,0,0,0,8,44,1,0,0,0,
        10,46,1,0,0,0,12,49,1,0,0,0,14,52,1,0,0,0,16,62,1,0,0,0,18,66,1,
        0,0,0,20,21,3,2,1,0,21,22,5,0,0,1,22,1,1,0,0,0,23,24,5,1,0,0,24,
        25,5,13,0,0,25,29,5,7,0,0,26,28,3,4,2,0,27,26,1,0,0,0,28,31,1,0,
        0,0,29,27,1,0,0,0,29,30,1,0,0,0,30,32,1,0,0,0,31,29,1,0,0,0,32,33,
        5,8,0,0,33,3,1,0,0,0,34,40,3,6,3,0,35,40,3,8,4,0,36,40,3,10,5,0,
        37,40,3,12,6,0,38,40,3,14,7,0,39,34,1,0,0,0,39,35,1,0,0,0,39,36,
        1,0,0,0,39,37,1,0,0,0,39,38,1,0,0,0,40,5,1,0,0,0,41,42,5,2,0,0,42,
        43,5,13,0,0,43,7,1,0,0,0,44,45,5,4,0,0,45,9,1,0,0,0,46,47,5,5,0,
        0,47,48,5,13,0,0,48,11,1,0,0,0,49,50,5,6,0,0,50,51,5,13,0,0,51,13,
        1,0,0,0,52,53,5,3,0,0,53,57,5,7,0,0,54,56,3,16,8,0,55,54,1,0,0,0,
        56,59,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,60,1,0,0,0,59,57,1,
        0,0,0,60,61,5,8,0,0,61,15,1,0,0,0,62,63,3,18,9,0,63,64,5,12,0,0,
        64,65,5,13,0,0,65,17,1,0,0,0,66,67,5,9,0,0,67,72,5,14,0,0,68,69,
        5,11,0,0,69,71,5,14,0,0,70,68,1,0,0,0,71,74,1,0,0,0,72,70,1,0,0,
        0,72,73,1,0,0,0,73,75,1,0,0,0,74,72,1,0,0,0,75,76,5,10,0,0,76,19,
        1,0,0,0,4,29,39,57,72
    ]

class TeachingScriptParser ( Parser ):

    grammarFileName = "TeachingScriptParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'lesson'", "'dataset'", "'add_examples'", 
                     "'test'", "'checkpoint'", "'rollback'", "'{'", "'}'", 
                     "'['", "']'", "','", "'->'" ]

    symbolicNames = [ "<INVALID>", "LESSON", "DATASET", "ADD_EXAMPLES", 
                      "TEST", "CHECKPOINT", "ROLLBACK", "LBRACE", "RBRACE", 
                      "LBRACKET", "RBRACKET", "COMMA", "ARROW", "STRING", 
                      "NUMBER", "WS", "LINE_COMMENT" ]

    RULE_program = 0
    RULE_lesson = 1
    RULE_statement = 2
    RULE_datasetStmt = 3
    RULE_testStmt = 4
    RULE_checkpointStmt = 5
    RULE_rollbackStmt = 6
    RULE_addExamplesStmt = 7
    RULE_example = 8
    RULE_featureVector = 9

    ruleNames =  [ "program", "lesson", "statement", "datasetStmt", "testStmt", 
                   "checkpointStmt", "rollbackStmt", "addExamplesStmt", 
                   "example", "featureVector" ]

    EOF = Token.EOF
    LESSON=1
    DATASET=2
    ADD_EXAMPLES=3
    TEST=4
    CHECKPOINT=5
    ROLLBACK=6
    LBRACE=7
    RBRACE=8
    LBRACKET=9
    RBRACKET=10
    COMMA=11
    ARROW=12
    STRING=13
    NUMBER=14
    WS=15
    LINE_COMMENT=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lesson(self):
            return self.getTypedRuleContext(TeachingScriptParser.LessonContext,0)


        def EOF(self):
            return self.getToken(TeachingScriptParser.EOF, 0)

        def getRuleIndex(self):
            return TeachingScriptParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = TeachingScriptParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.lesson()
            self.state = 21
            self.match(TeachingScriptParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LessonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LESSON(self):
            return self.getToken(TeachingScriptParser.LESSON, 0)

        def STRING(self):
            return self.getToken(TeachingScriptParser.STRING, 0)

        def LBRACE(self):
            return self.getToken(TeachingScriptParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(TeachingScriptParser.RBRACE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TeachingScriptParser.StatementContext)
            else:
                return self.getTypedRuleContext(TeachingScriptParser.StatementContext,i)


        def getRuleIndex(self):
            return TeachingScriptParser.RULE_lesson

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLesson" ):
                return visitor.visitLesson(self)
            else:
                return visitor.visitChildren(self)




    def lesson(self):

        localctx = TeachingScriptParser.LessonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_lesson)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.match(TeachingScriptParser.LESSON)
            self.state = 24
            self.match(TeachingScriptParser.STRING)
            self.state = 25
            self.match(TeachingScriptParser.LBRACE)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 124) != 0):
                self.state = 26
                self.statement()
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 32
            self.match(TeachingScriptParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def datasetStmt(self):
            return self.getTypedRuleContext(TeachingScriptParser.DatasetStmtContext,0)


        def testStmt(self):
            return self.getTypedRuleContext(TeachingScriptParser.TestStmtContext,0)


        def checkpointStmt(self):
            return self.getTypedRuleContext(TeachingScriptParser.CheckpointStmtContext,0)


        def rollbackStmt(self):
            return self.getTypedRuleContext(TeachingScriptParser.RollbackStmtContext,0)


        def addExamplesStmt(self):
            return self.getTypedRuleContext(TeachingScriptParser.AddExamplesStmtContext,0)


        def getRuleIndex(self):
            return TeachingScriptParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = TeachingScriptParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_statement)
        try:
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 34
                self.datasetStmt()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 35
                self.testStmt()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 36
                self.checkpointStmt()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 4)
                self.state = 37
                self.rollbackStmt()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 5)
                self.state = 38
                self.addExamplesStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DatasetStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DATASET(self):
            return self.getToken(TeachingScriptParser.DATASET, 0)

        def STRING(self):
            return self.getToken(TeachingScriptParser.STRING, 0)

        def getRuleIndex(self):
            return TeachingScriptParser.RULE_datasetStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDatasetStmt" ):
                return visitor.visitDatasetStmt(self)
            else:
                return visitor.visitChildren(self)




    def datasetStmt(self):

        localctx = TeachingScriptParser.DatasetStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_datasetStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(TeachingScriptParser.DATASET)
            self.state = 42
            self.match(TeachingScriptParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TestStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TEST(self):
            return self.getToken(TeachingScriptParser.TEST, 0)

        def getRuleIndex(self):
            return TeachingScriptParser.RULE_testStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTestStmt" ):
                return visitor.visitTestStmt(self)
            else:
                return visitor.visitChildren(self)




    def testStmt(self):

        localctx = TeachingScriptParser.TestStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_testStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(TeachingScriptParser.TEST)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CheckpointStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHECKPOINT(self):
            return self.getToken(TeachingScriptParser.CHECKPOINT, 0)

        def STRING(self):
            return self.getToken(TeachingScriptParser.STRING, 0)

        def getRuleIndex(self):
            return TeachingScriptParser.RULE_checkpointStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCheckpointStmt" ):
                return visitor.visitCheckpointStmt(self)
            else:
                return visitor.visitChildren(self)




    def checkpointStmt(self):

        localctx = TeachingScriptParser.CheckpointStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_checkpointStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(TeachingScriptParser.CHECKPOINT)
            self.state = 47
            self.match(TeachingScriptParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RollbackStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ROLLBACK(self):
            return self.getToken(TeachingScriptParser.ROLLBACK, 0)

        def STRING(self):
            return self.getToken(TeachingScriptParser.STRING, 0)

        def getRuleIndex(self):
            return TeachingScriptParser.RULE_rollbackStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRollbackStmt" ):
                return visitor.visitRollbackStmt(self)
            else:
                return visitor.visitChildren(self)




    def rollbackStmt(self):

        localctx = TeachingScriptParser.RollbackStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_rollbackStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(TeachingScriptParser.ROLLBACK)
            self.state = 50
            self.match(TeachingScriptParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddExamplesStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD_EXAMPLES(self):
            return self.getToken(TeachingScriptParser.ADD_EXAMPLES, 0)

        def LBRACE(self):
            return self.getToken(TeachingScriptParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(TeachingScriptParser.RBRACE, 0)

        def example(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TeachingScriptParser.ExampleContext)
            else:
                return self.getTypedRuleContext(TeachingScriptParser.ExampleContext,i)


        def getRuleIndex(self):
            return TeachingScriptParser.RULE_addExamplesStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddExamplesStmt" ):
                return visitor.visitAddExamplesStmt(self)
            else:
                return visitor.visitChildren(self)




    def addExamplesStmt(self):

        localctx = TeachingScriptParser.AddExamplesStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_addExamplesStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(TeachingScriptParser.ADD_EXAMPLES)
            self.state = 53
            self.match(TeachingScriptParser.LBRACE)
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9:
                self.state = 54
                self.example()
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 60
            self.match(TeachingScriptParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExampleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def featureVector(self):
            return self.getTypedRuleContext(TeachingScriptParser.FeatureVectorContext,0)


        def ARROW(self):
            return self.getToken(TeachingScriptParser.ARROW, 0)

        def STRING(self):
            return self.getToken(TeachingScriptParser.STRING, 0)

        def getRuleIndex(self):
            return TeachingScriptParser.RULE_example

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExample" ):
                return visitor.visitExample(self)
            else:
                return visitor.visitChildren(self)




    def example(self):

        localctx = TeachingScriptParser.ExampleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_example)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.featureVector()
            self.state = 63
            self.match(TeachingScriptParser.ARROW)
            self.state = 64
            self.match(TeachingScriptParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FeatureVectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACKET(self):
            return self.getToken(TeachingScriptParser.LBRACKET, 0)

        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(TeachingScriptParser.NUMBER)
            else:
                return self.getToken(TeachingScriptParser.NUMBER, i)

        def RBRACKET(self):
            return self.getToken(TeachingScriptParser.RBRACKET, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(TeachingScriptParser.COMMA)
            else:
                return self.getToken(TeachingScriptParser.COMMA, i)

        def getRuleIndex(self):
            return TeachingScriptParser.RULE_featureVector

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFeatureVector" ):
                return visitor.visitFeatureVector(self)
            else:
                return visitor.visitChildren(self)




    def featureVector(self):

        localctx = TeachingScriptParser.FeatureVectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_featureVector)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(TeachingScriptParser.LBRACKET)
            self.state = 67
            self.match(TeachingScriptParser.NUMBER)
            self.state = 72
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11:
                self.state = 68
                self.match(TeachingScriptParser.COMMA)
                self.state = 69
                self.match(TeachingScriptParser.NUMBER)
                self.state = 74
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 75
            self.match(TeachingScriptParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





