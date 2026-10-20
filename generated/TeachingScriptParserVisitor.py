# Generated from TeachingScriptParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TeachingScriptParser import TeachingScriptParser
else:
    from TeachingScriptParser import TeachingScriptParser

# This class defines a complete generic visitor for a parse tree produced by TeachingScriptParser.

class TeachingScriptParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TeachingScriptParser#program.
    def visitProgram(self, ctx:TeachingScriptParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#lesson.
    def visitLesson(self, ctx:TeachingScriptParser.LessonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#statement.
    def visitStatement(self, ctx:TeachingScriptParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#datasetStmt.
    def visitDatasetStmt(self, ctx:TeachingScriptParser.DatasetStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#testStmt.
    def visitTestStmt(self, ctx:TeachingScriptParser.TestStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#checkpointStmt.
    def visitCheckpointStmt(self, ctx:TeachingScriptParser.CheckpointStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#rollbackStmt.
    def visitRollbackStmt(self, ctx:TeachingScriptParser.RollbackStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#addExamplesStmt.
    def visitAddExamplesStmt(self, ctx:TeachingScriptParser.AddExamplesStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#example.
    def visitExample(self, ctx:TeachingScriptParser.ExampleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeachingScriptParser#featureVector.
    def visitFeatureVector(self, ctx:TeachingScriptParser.FeatureVectorContext):
        return self.visitChildren(ctx)



del TeachingScriptParser