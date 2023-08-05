# $ANTLR 3.5.2 cadbiom/models/biosignal/translators/sigexpr_compiler.g 2018-12-14 16:41:05

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

from antlr3.tree import *



from cadbiom.models.biosignal.sig_expr import *
import string



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
AND=4
CHG=5
COM=6
COMMENT=7
CONSTR=8
DEF=9
DEFAULT=10
DIGIT=11
DOL=12
EG=13
EVENT=14
EXC=15
EXP=16
F=17
IDENT=18
INC=19
LETTER=20
MINUS=21
MUL=22
NOT=23
NOTEG=24
OR=25
PD=26
PG=27
PLUS=28
SCOL=29
SEQ=30
SYNC=31
T=32
WHEN=33
WS=34

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "AND", "CHG", "COM", "COMMENT", "CONSTR", "DEF", "DEFAULT", "DIGIT",
    "DOL", "EG", "EVENT", "EXC", "EXP", "F", "IDENT", "INC", "LETTER", "MINUS",
    "MUL", "NOT", "NOTEG", "OR", "PD", "PG", "PLUS", "SCOL", "SEQ", "SYNC",
    "T", "WHEN", "WS"
]




class sigexpr_compiler(Parser):
    grammarFileName = "cadbiom/models/biosignal/translators/sigexpr_compiler.g"
    api_version = 1
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(sigexpr_compiler, self).__init__(input, state, *args, **kwargs)




        self.state_events = []
        self.free_clocks = []
        self.state_only = False
        self.state_only_in_bool = False
        self.catch_free_clocks = False
        self.deep = -1
        self.message = ""
        self.error_reporter = None


        self.delegates = []

        self._adaptor = None
        self.adaptor = CommonTreeAdaptor()



    def getTreeAdaptor(self):
        return self._adaptor

    def setTreeAdaptor(self, adaptor):
        self._adaptor = adaptor

    adaptor = property(getTreeAdaptor, setTreeAdaptor)


    def set_error_reporter(self, err):
        self.error_reporter = err

    def displayRecognitionError(self, tokenNames, re):
           hdr = self.getErrorHeader(re)
           msg = self.getErrorMessage(re, tokenNames)
           self.error_reporter.display('sig_exp ->'+hdr+msg+self.message)


    def displayExceptionMessage(self, e):
      msg = self.getErrorMessage(self, e, tokenNames)
      self.error_reporter.display('sig_exp ->'+msg)

    # semantic checks for compilers
    def check_ident(self, symbol_table, st_only, free_clock, deep, message, name):
        """
        Check if  name  is declared  (with state/input type if st_only = True)
        @return: a SigIdentExpr
        """
        try:
          name = name.encode("utf-8")
          type, s_deep = symbol_table[name]
          # for condition compiler
          if st_only:
            if (not (type == "state" or type=="input")):
              self.error_reporter.display("type error -> " + name + " is not a state (" +type+")"+ message)
          else:
            if deep >= 0:
              if s_deep >= deep:
                 self.error_reporter.display("type error -> " + name + " not declared in a surrounding macro state"+ message)
        except KeyError:
          if free_clock and not st_only:
            self.free_clocks.append(name)
          else:
            self.error_reporter.display("dec -> Undeclared event or state:" + name + message)
        return SigIdentExpr(name)

    def check_updown(self, symbol_table, id, mode):
        """
        This function introduce new signals: state> or state<
        """
        id  = id.encode("utf-8")
        try:
            att = symbol_table[id]
            type = att[0]
            s_deep = att[1]
        except KeyError:
            self.error_reporter.display('dec -> Undeclared state in variation:' + id)
            type = "error"
        if type == "state":
            if mode == 1: #up
                name = id+">"
            else: #down
                name = id+"<"
            self.state_events.append(name)
            return SigIdentExpr(name)
        else:
            self.error_reporter.display('type error -> Up and Down can only be derived from a state: '+id)

    def  check_change(self, symbol_table, id):
        id  = id.encode("utf-8")
        try:
            att = symbol_table[id]
            type = att[0]
            s_deep = att[1]
        except KeyError:
            self.error_reporter.display('dec -> Undeclared signal in variation:' + id)
            type = "error"
        if type == "state":
            refresh_expr = SigIdentExpr(id)
            st_expr = SigIdentExpr(id)
            return SigWhenExpr(SigConstExpr(True),SigDiffExpr(st_expr, refresh_expr))
        else:
            self.error_reporter.display('type error -> Change can only be derived  from a state: '+id)

    def check_sync(self, lexp):
        # type checking is done in expressions
        return SigConstraintExpr(SigConstraintExpr.SYNCHRO, lexp)

    def check_exclus(self, lexp):
        return SigConstraintExpr(SigConstraintExpr.EXCLU, lexp)


    def check_included(self, exp1,exp2):
        return SigConstraintExpr(SigConstraintExpr.INCL, [exp1,exp2])



    class sig_expression_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_expression_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_expression"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:163:1: sig_expression[tab_symb] returns [exp] : (exp1= sig_expression1[tab_symb] DOL |exp2= sig_constraint[tab_symb] DOL );
    def sig_expression(self, tab_symb):
        retval = self.sig_expression_return()
        retval.start = self.input.LT(1)


        root_0 = None

        DOL1 = None
        DOL2 = None
        exp1 = None
        exp2 = None

        DOL1_tree = None
        DOL2_tree = None

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:164:9: (exp1= sig_expression1[tab_symb] DOL |exp2= sig_constraint[tab_symb] DOL )
            alt1 = 2
            LA1_0 = self.input.LA(1)

            if (LA1_0 == DOL or LA1_0 == EVENT or (F <= LA1_0 <= IDENT) or LA1_0 == NOT or LA1_0 == PG or (T <= LA1_0 <= WHEN)) :
                alt1 = 1
            elif (LA1_0 == EXC or LA1_0 == INC or LA1_0 == SYNC) :
                alt1 = 2
            else:
                nvae = NoViableAltException("", 1, 0, self.input)

                raise nvae


            if alt1 == 1:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:164:11: exp1= sig_expression1[tab_symb] DOL
                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_sig_expression1_in_sig_expression148)
                exp1 = self.sig_expression1(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)


                DOL1 = self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_expression151)
                DOL1_tree = self._adaptor.createWithPayload(DOL1)
                self._adaptor.addChild(root_0, DOL1_tree)



                #action start
                retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
                #action end



            elif alt1 == 2:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:166:11: exp2= sig_constraint[tab_symb] DOL

                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_sig_constraint_in_sig_expression181)
                exp2 = self.sig_constraint(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp2.tree)


                DOL2 = self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_expression184)
                DOL2_tree = self._adaptor.createWithPayload(DOL2)
                self._adaptor.addChild(root_0, DOL2_tree)



                #action start
                retval.exp = ((exp2 is not None) and [exp2.exp] or [None])[0]
                #action end



            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_expression"


    class sig_expression1_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_expression1_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_expression1"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:170:1: sig_expression1[tab_symb] returns [exp] : (exp1= sig_exp[tab_symb] ( DEFAULT ^exp2= sig_exp[tab_symb] )* |);
    def sig_expression1(self, tab_symb):
        retval = self.sig_expression1_return()
        retval.start = self.input.LT(1)


        root_0 = None

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:171:9: (exp1= sig_exp[tab_symb] ( DEFAULT ^exp2= sig_exp[tab_symb] )* |)
            alt3 = 2
            LA3_0 = self.input.LA(1)

            if (LA3_0 == EVENT or (F <= LA3_0 <= IDENT) or LA3_0 == NOT or LA3_0 == PG or (T <= LA3_0 <= WHEN)) :
                alt3 = 1
            elif (LA3_0 == COM or LA3_0 == DOL or LA3_0 == PD) :
                alt3 = 2
            else:
                nvae = NoViableAltException("", 3, 0, self.input)

                raise nvae


            if alt3 == 1:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:171:11: exp1= sig_exp[tab_symb] ( DEFAULT ^exp2= sig_exp[tab_symb] )*

                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_sig_exp_in_sig_expression1230)
                exp1 = self.sig_exp(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)


                #action start
                retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
                #action end


                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:172:11: ( DEFAULT ^exp2= sig_exp[tab_symb] )*
                while True: #loop2
                    alt2 = 2
                    LA2_0 = self.input.LA(1)

                    if (LA2_0 == DEFAULT) :
                        alt2 = 1


                    if alt2 == 1:
                        # cadbiom/models/biosignal/translators/sigexpr_compiler.g:172:12: DEFAULT ^exp2= sig_exp[tab_symb]

                        DEFAULT3 = self.match(self.input, DEFAULT, self.FOLLOW_DEFAULT_in_sig_expression1247)
                        DEFAULT3_tree = self._adaptor.createWithPayload(DEFAULT3)
                        root_0 = self._adaptor.becomeRoot(DEFAULT3_tree, root_0)



                        self._state.following.append(self.FOLLOW_sig_exp_in_sig_expression1252)
                        exp2 = self.sig_exp(tab_symb)

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exp2.tree)


                        #action start
                        retval.exp = SigDefaultExpr(retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                        #action end



                    else:
                        break #loop2



            elif alt3 == 2:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:176:11:

                root_0 = self._adaptor.nil()


                #action start
                retval.exp = SigConstExpr(True)
                #action end



            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_expression1"


    class sig_exp_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_exp_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_exp"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:179:1: sig_exp[tab_symb] returns [exp] : exp1= sig_bool[tab_symb] ( WHEN ^exp2= sig_bool[tab_symb] )* ;
    def sig_exp(self, tab_symb):
        retval = self.sig_exp_return()
        retval.start = self.input.LT(1)

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:180:9: (exp1= sig_bool[tab_symb] ( WHEN ^exp2= sig_bool[tab_symb] )* )
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:180:12: exp1= sig_bool[tab_symb] ( WHEN ^exp2= sig_bool[tab_symb] )*

            root_0 = self._adaptor.nil()


            self._state.following.append(self.FOLLOW_sig_bool_in_sig_exp338)
            exp1 = self.sig_bool(tab_symb)

            self._state.following.pop()
            self._adaptor.addChild(root_0, exp1.tree)


            #action start
            retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
            #action end


            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:181:11: ( WHEN ^exp2= sig_bool[tab_symb] )*
            while True: #loop4
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == WHEN) :
                    alt4 = 1


                if alt4 == 1:
                    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:181:12: WHEN ^exp2= sig_bool[tab_symb]

                    WHEN4 = self.match(self.input, WHEN, self.FOLLOW_WHEN_in_sig_exp355)
                    WHEN4_tree = self._adaptor.createWithPayload(WHEN4)
                    root_0 = self._adaptor.becomeRoot(WHEN4_tree, root_0)



                    #action start
                    st_only_save = self.state_only; self.state_only = self.state_only_in_bool
                    #action end


                    self._state.following.append(self.FOLLOW_sig_bool_in_sig_exp389)
                    exp2 = self.sig_bool(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exp2.tree)


                    #action start
                    retval.exp = SigWhenExpr(retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                    self.state_only = st_only_save
                    #action end



                else:
                    break #loop4




            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_exp"


    class sig_bool_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_bool_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_bool"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:190:1: sig_bool[tab_symb] returns [exp] : exp1= sig_bool_and[tab_symb] ( OR ^exp2= sig_bool_and[tab_symb] )* ;
    def sig_bool(self, tab_symb):
        retval = self.sig_bool_return()
        retval.start = self.input.LT(1)

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:191:9: (exp1= sig_bool_and[tab_symb] ( OR ^exp2= sig_bool_and[tab_symb] )* )
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:191:11: exp1= sig_bool_and[tab_symb] ( OR ^exp2= sig_bool_and[tab_symb] )*

            root_0 = self._adaptor.nil()


            self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool471)
            exp1 = self.sig_bool_and(tab_symb)

            self._state.following.pop()
            self._adaptor.addChild(root_0, exp1.tree)


            #action start
            retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
            #action end


            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:192:11: ( OR ^exp2= sig_bool_and[tab_symb] )*
            while True: #loop5
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == OR) :
                    alt5 = 1


                if alt5 == 1:
                    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:192:12: OR ^exp2= sig_bool_and[tab_symb]

                    OR5 = self.match(self.input, OR, self.FOLLOW_OR_in_sig_bool487)
                    OR5_tree = self._adaptor.createWithPayload(OR5)
                    root_0 = self._adaptor.becomeRoot(OR5_tree, root_0)



                    self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool492)
                    exp2 = self.sig_bool_and(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exp2.tree)


                    #action start
                    retval.exp = SigSyncBinExpr("or", retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                    #action end



                else:
                    break #loop5




            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_bool"


    class sig_bool_and_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_bool_and_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_bool_and"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:197:1: sig_bool_and[tab_symb] returns [exp] : exp1= sig_primary[tab_symb] ( AND ^exp2= sig_primary[tab_symb] )* ;
    def sig_bool_and(self, tab_symb):
        retval = self.sig_bool_and_return()
        retval.start = self.input.LT(1)

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:198:9: (exp1= sig_primary[tab_symb] ( AND ^exp2= sig_primary[tab_symb] )* )
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:198:11: exp1= sig_primary[tab_symb] ( AND ^exp2= sig_primary[tab_symb] )*

            root_0 = self._adaptor.nil()


            self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and561)
            exp1 = self.sig_primary(tab_symb)

            self._state.following.pop()
            self._adaptor.addChild(root_0, exp1.tree)


            #action start
            retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
            #action end


            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:199:11: ( AND ^exp2= sig_primary[tab_symb] )*
            while True: #loop6
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == AND) :
                    alt6 = 1


                if alt6 == 1:
                    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:199:12: AND ^exp2= sig_primary[tab_symb]

                    AND6 = self.match(self.input, AND, self.FOLLOW_AND_in_sig_bool_and577)
                    AND6_tree = self._adaptor.createWithPayload(AND6)
                    root_0 = self._adaptor.becomeRoot(AND6_tree, root_0)



                    self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and582)
                    exp2 = self.sig_primary(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exp2.tree)


                    #action start
                    retval.exp = SigSyncBinExpr("and",retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                    #action end



                else:
                    break #loop6




            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_bool_and"


    class sig_primary_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_primary_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_primary"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:204:1: sig_primary[tab_symb] returns [exp] : ( NOT ^nexp= sig_primary[tab_symb] |cexp= sig_constant | EVENT PG !exps= sig_expression1[tab_symb] PD !| WHEN PG !expw= sig_expression1[tab_symb] PD !|i7= IDENT UP |i8= IDENT DOWN |id2= IDENT | PG expse= sig_expression1[tab_symb] PD );
    def sig_primary(self, tab_symb):
        retval = self.sig_primary_return()
        retval.start = self.input.LT(1)

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:205:9: ( NOT ^nexp= sig_primary[tab_symb] |cexp= sig_constant | EVENT PG !exps= sig_expression1[tab_symb] PD !| WHEN PG !expw= sig_expression1[tab_symb] PD !|i7= IDENT UP |i8= IDENT DOWN |id2= IDENT | PG expse= sig_expression1[tab_symb] PD )
            alt7 = 8
            LA7 = self.input.LA(1)
            if LA7 == NOT:
                alt7 = 1
            elif LA7 == F or LA7 == T:
                alt7 = 2
            elif LA7 == EVENT:
                alt7 = 3
            elif LA7 == WHEN:
                alt7 = 4
            elif LA7 == IDENT:
                LA7 = self.input.LA(2)
                if LA7 == 3:
                    alt7 = 5
                elif LA7 == 2:
                    alt7 = 6
                elif LA7 == AND or LA7 == COM or LA7 == DEFAULT or LA7 == DOL or LA7 == OR or LA7 == PD or LA7 == WHEN:
                    alt7 = 7
                else:
                    nvae = NoViableAltException("", 7, 6, self.input)

                    raise nvae


            elif LA7 == PG:
                alt7 = 8
            else:
                nvae = NoViableAltException("", 7, 0, self.input)

                raise nvae


            if alt7 == 1:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:205:11: NOT ^nexp= sig_primary[tab_symb]

                root_0 = self._adaptor.nil()


                NOT7 = self.match(self.input, NOT, self.FOLLOW_NOT_in_sig_primary656)
                NOT7_tree = self._adaptor.createWithPayload(NOT7)
                root_0 = self._adaptor.becomeRoot(NOT7_tree, root_0)



                self._state.following.append(self.FOLLOW_sig_primary_in_sig_primary661)
                nexp = self.sig_primary(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, nexp.tree)


                #action start
                retval.exp = SigNotExpr(((nexp is not None) and [nexp.exp] or [None])[0])
                #action end



            elif alt7 == 2:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:208:11: cexp= sig_constant

                root_0 = self._adaptor.nil()


                self._state.following.append(self.FOLLOW_sig_constant_in_sig_primary704)
                cexp = self.sig_constant()

                self._state.following.pop()
                self._adaptor.addChild(root_0, cexp.tree)


                #action start
                retval.exp = ((cexp is not None) and [cexp.exp] or [None])[0]
                #action end



            elif alt7 == 3:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:211:11: EVENT PG !exps= sig_expression1[tab_symb] PD !

                root_0 = self._adaptor.nil()


                EVENT8 = self.match(self.input, EVENT, self.FOLLOW_EVENT_in_sig_primary751)
                EVENT8_tree = self._adaptor.createWithPayload(EVENT8)
                self._adaptor.addChild(root_0, EVENT8_tree)



                self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary753)

                self._state.following.append(self.FOLLOW_sig_expression1_in_sig_primary758)
                exps = self.sig_expression1(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exps.tree)


                self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary761)

                #action start
                retval.exp = SigEventExpr(((exps is not None) and [exps.exp] or [None])[0])
                #action end



            elif alt7 == 4:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:214:11: WHEN PG !expw= sig_expression1[tab_symb] PD !

                root_0 = self._adaptor.nil()


                WHEN11 = self.match(self.input, WHEN, self.FOLLOW_WHEN_in_sig_primary798)
                WHEN11_tree = self._adaptor.createWithPayload(WHEN11)
                self._adaptor.addChild(root_0, WHEN11_tree)



                self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary800)

                self._state.following.append(self.FOLLOW_sig_expression1_in_sig_primary805)
                expw = self.sig_expression1(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, expw.tree)


                self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary808)

                #action start
                retval.exp = SigWhenExpr(SigConstExpr(True),((expw is not None) and [expw.exp] or [None])[0])
                #action end



            elif alt7 == 5:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:217:11: i7= IDENT UP

                root_0 = self._adaptor.nil()


                i7 = self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary838)
                i7_tree = self._adaptor.createWithPayload(i7)
                self._adaptor.addChild(root_0, i7_tree)



                UP14 = self.match(self.input, 3, self.FOLLOW_3_in_sig_primary840)
                UP14_tree = self._adaptor.createWithPayload(UP14)
                self._adaptor.addChild(root_0, UP14_tree)



                #action start
                retval.exp = self.check_updown(tab_symb, i7.text, 1)
                #action end



            elif alt7 == 6:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:220:11: i8= IDENT DOWN

                root_0 = self._adaptor.nil()


                i8 = self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary870)
                i8_tree = self._adaptor.createWithPayload(i8)
                self._adaptor.addChild(root_0, i8_tree)



                DOWN15 = self.match(self.input, 2, self.FOLLOW_2_in_sig_primary872)
                DOWN15_tree = self._adaptor.createWithPayload(DOWN15)
                self._adaptor.addChild(root_0, DOWN15_tree)



                #action start
                retval.exp = self.check_updown(tab_symb, i8.text, 2)
                #action end



            elif alt7 == 7:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:225:11: id2= IDENT

                root_0 = self._adaptor.nil()


                id2 = self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary915)
                id2_tree = self._adaptor.createWithPayload(id2)
                self._adaptor.addChild(root_0, id2_tree)



                #action start
                retval.exp = self.check_ident(tab_symb, self.state_only, self.catch_free_clocks, self.deep, self.message, id2.text)
                #action end



            elif alt7 == 8:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:228:11: PG expse= sig_expression1[tab_symb] PD

                root_0 = self._adaptor.nil()


                PG16 = self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary956)
                PG16_tree = self._adaptor.createWithPayload(PG16)
                self._adaptor.addChild(root_0, PG16_tree)



                self._state.following.append(self.FOLLOW_sig_expression1_in_sig_primary960)
                expse = self.sig_expression1(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, expse.tree)


                PD17 = self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary963)
                PD17_tree = self._adaptor.createWithPayload(PD17)
                self._adaptor.addChild(root_0, PD17_tree)



                #action start
                retval.exp = ((expse is not None) and [expse.exp] or [None])[0]
                #action end



            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_primary"


    class sig_constant_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_constant_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_constant"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:232:1: sig_constant returns [exp] : ( T | F );
    def sig_constant(self, ):
        retval = self.sig_constant_return()
        retval.start = self.input.LT(1)


        root_0 = None

        T18 = None
        F19 = None

        T18_tree = None
        F19_tree = None

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:233:10: ( T | F )
            alt8 = 2
            LA8_0 = self.input.LA(1)

            if (LA8_0 == T) :
                alt8 = 1
            elif (LA8_0 == F) :
                alt8 = 2
            else:
                nvae = NoViableAltException("", 8, 0, self.input)

                raise nvae


            if alt8 == 1:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:233:12: T

                root_0 = self._adaptor.nil()


                T18 = self.match(self.input, T, self.FOLLOW_T_in_sig_constant1008)
                T18_tree = self._adaptor.createWithPayload(T18)
                self._adaptor.addChild(root_0, T18_tree)



                #action start
                retval.exp = SigConstExpr(True)
                #action end



            elif alt8 == 2:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:234:12: F

                root_0 = self._adaptor.nil()


                F19 = self.match(self.input, F, self.FOLLOW_F_in_sig_constant1023)
                F19_tree = self._adaptor.createWithPayload(F19)
                self._adaptor.addChild(root_0, F19_tree)



                #action start
                retval.exp = SigConstExpr(False)
                #action end



            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_constant"


    class sig_constraint_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.sig_constraint_return, self).__init__()

            self.exp = None
            self.tree = None





    # $ANTLR start "sig_constraint"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:237:1: sig_constraint[tab_symb] returns [exp] : ( SYNC ^ PG !el= exp_list[tab_symb] PD !| EXC ^ PG !el= exp_list[tab_symb] PD !| INC ^ PG !e3= sig_expression1[tab_symb] COM !e4= sig_exp[tab_symb] PD !);
    def sig_constraint(self, tab_symb):
        retval = self.sig_constraint_return()
        retval.start = self.input.LT(1)


        root_0 = None

        SYNC20 = None
        PG21 = None
        PD22 = None
        EXC23 = None
        PG24 = None
        PD25 = None
        INC26 = None
        PG27 = None
        COM28 = None
        PD29 = None
        el = None
        e3 = None
        e4 = None

        SYNC20_tree = None
        PG21_tree = None
        PD22_tree = None
        EXC23_tree = None
        PG24_tree = None
        PD25_tree = None
        INC26_tree = None
        PG27_tree = None
        COM28_tree = None
        PD29_tree = None

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:238:10: ( SYNC ^ PG !el= exp_list[tab_symb] PD !| EXC ^ PG !el= exp_list[tab_symb] PD !| INC ^ PG !e3= sig_expression1[tab_symb] COM !e4= sig_exp[tab_symb] PD !)
            alt9 = 3
            LA9 = self.input.LA(1)
            if LA9 == SYNC:
                alt9 = 1
            elif LA9 == EXC:
                alt9 = 2
            elif LA9 == INC:
                alt9 = 3
            else:
                nvae = NoViableAltException("", 9, 0, self.input)

                raise nvae


            if alt9 == 1:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:238:12: SYNC ^ PG !el= exp_list[tab_symb] PD !

                root_0 = self._adaptor.nil()


                SYNC20 = self.match(self.input, SYNC, self.FOLLOW_SYNC_in_sig_constraint1075)
                SYNC20_tree = self._adaptor.createWithPayload(SYNC20)
                root_0 = self._adaptor.becomeRoot(SYNC20_tree, root_0)



                PG21 = self.match(self.input, PG, self.FOLLOW_PG_in_sig_constraint1078)

                self._state.following.append(self.FOLLOW_exp_list_in_sig_constraint1083)
                el = self.exp_list(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, el.tree)


                PD22 = self.match(self.input, PD, self.FOLLOW_PD_in_sig_constraint1087)

                #action start
                retval.exp = self.check_sync(((el is not None) and [el.expl] or [None])[0])
                #action end



            elif alt9 == 2:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:241:12: EXC ^ PG !el= exp_list[tab_symb] PD !

                root_0 = self._adaptor.nil()


                EXC23 = self.match(self.input, EXC, self.FOLLOW_EXC_in_sig_constraint1138)
                EXC23_tree = self._adaptor.createWithPayload(EXC23)
                root_0 = self._adaptor.becomeRoot(EXC23_tree, root_0)



                PG24 = self.match(self.input, PG, self.FOLLOW_PG_in_sig_constraint1142)

                self._state.following.append(self.FOLLOW_exp_list_in_sig_constraint1149)
                el = self.exp_list(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, el.tree)


                PD25 = self.match(self.input, PD, self.FOLLOW_PD_in_sig_constraint1152)

                #action start
                retval.exp = self.check_exclus(((el is not None) and [el.expl] or [None])[0])
                #action end



            elif alt9 == 3:
                # cadbiom/models/biosignal/translators/sigexpr_compiler.g:244:12: INC ^ PG !e3= sig_expression1[tab_symb] COM !e4= sig_exp[tab_symb] PD !

                root_0 = self._adaptor.nil()


                INC26 = self.match(self.input, INC, self.FOLLOW_INC_in_sig_constraint1181)
                INC26_tree = self._adaptor.createWithPayload(INC26)
                root_0 = self._adaptor.becomeRoot(INC26_tree, root_0)



                PG27 = self.match(self.input, PG, self.FOLLOW_PG_in_sig_constraint1184)

                self._state.following.append(self.FOLLOW_sig_expression1_in_sig_constraint1189)
                e3 = self.sig_expression1(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, e3.tree)


                COM28 = self.match(self.input, COM, self.FOLLOW_COM_in_sig_constraint1192)

                self._state.following.append(self.FOLLOW_sig_exp_in_sig_constraint1197)
                e4 = self.sig_exp(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, e4.tree)


                PD29 = self.match(self.input, PD, self.FOLLOW_PD_in_sig_constraint1200)

                #action start
                retval.exp = self.check_included(((e3 is not None) and [e3.exp] or [None])[0], ((e4 is not None) and [e4.exp] or [None])[0])
                #action end



            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "sig_constraint"


    class exp_list_return(ParserRuleReturnScope):
        def __init__(self):
            super(sigexpr_compiler.exp_list_return, self).__init__()

            self.expl = None
            self.tree = None





    # $ANTLR start "exp_list"
    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:248:1: exp_list[tab_symb] returns [expl] : exp1= sig_expression1[tab_symb] ( COM exp2= sig_expression1[tab_symb] )* ;
    def exp_list(self, tab_symb):
        retval = self.exp_list_return()
        retval.start = self.input.LT(1)


        root_0 = None

        COM30 = None
        exp1 = None
        exp2 = None

        COM30_tree = None

        try:
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:249:10: (exp1= sig_expression1[tab_symb] ( COM exp2= sig_expression1[tab_symb] )* )
            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:249:12: exp1= sig_expression1[tab_symb] ( COM exp2= sig_expression1[tab_symb] )*

            root_0 = self._adaptor.nil()


            self._state.following.append(self.FOLLOW_sig_expression1_in_exp_list1257)
            exp1 = self.sig_expression1(tab_symb)

            self._state.following.pop()
            self._adaptor.addChild(root_0, exp1.tree)


            #action start
            retval.expl = [((exp1 is not None) and [exp1.exp] or [None])[0]]
            #action end


            # cadbiom/models/biosignal/translators/sigexpr_compiler.g:250:13: ( COM exp2= sig_expression1[tab_symb] )*
            while True: #loop10
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == COM) :
                    alt10 = 1


                if alt10 == 1:
                    # cadbiom/models/biosignal/translators/sigexpr_compiler.g:250:14: COM exp2= sig_expression1[tab_symb]

                    COM30 = self.match(self.input, COM, self.FOLLOW_COM_in_exp_list1275)
                    COM30_tree = self._adaptor.createWithPayload(COM30)
                    self._adaptor.addChild(root_0, COM30_tree)



                    self._state.following.append(self.FOLLOW_sig_expression1_in_exp_list1279)
                    exp2 = self.sig_expression1(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exp2.tree)


                    #action start
                    retval.expl.append(((exp2 is not None) and [exp2.exp] or [None])[0])
                    #action end



                else:
                    break #loop10




            retval.stop = self.input.LT(-1)


            retval.tree = self._adaptor.rulePostProcessing(root_0)
            self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)



        except RecognitionException as re:
            self.reportError(re)
            self.recover(self.input, re)
            retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)

        return retval

    # $ANTLR end "exp_list"





    FOLLOW_sig_expression1_in_sig_expression148 = frozenset([12])
    FOLLOW_DOL_in_sig_expression151 = frozenset([1])
    FOLLOW_sig_constraint_in_sig_expression181 = frozenset([12])
    FOLLOW_DOL_in_sig_expression184 = frozenset([1])
    FOLLOW_sig_exp_in_sig_expression1230 = frozenset([1, 10])
    FOLLOW_DEFAULT_in_sig_expression1247 = frozenset([14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_exp_in_sig_expression1252 = frozenset([1, 10])
    FOLLOW_sig_bool_in_sig_exp338 = frozenset([1, 33])
    FOLLOW_WHEN_in_sig_exp355 = frozenset([14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_bool_in_sig_exp389 = frozenset([1, 33])
    FOLLOW_sig_bool_and_in_sig_bool471 = frozenset([1, 25])
    FOLLOW_OR_in_sig_bool487 = frozenset([14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_bool_and_in_sig_bool492 = frozenset([1, 25])
    FOLLOW_sig_primary_in_sig_bool_and561 = frozenset([1, 4])
    FOLLOW_AND_in_sig_bool_and577 = frozenset([14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_primary_in_sig_bool_and582 = frozenset([1, 4])
    FOLLOW_NOT_in_sig_primary656 = frozenset([14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_primary_in_sig_primary661 = frozenset([1])
    FOLLOW_sig_constant_in_sig_primary704 = frozenset([1])
    FOLLOW_EVENT_in_sig_primary751 = frozenset([27])
    FOLLOW_PG_in_sig_primary753 = frozenset([14, 17, 18, 23, 26, 27, 32, 33])
    FOLLOW_sig_expression1_in_sig_primary758 = frozenset([26])
    FOLLOW_PD_in_sig_primary761 = frozenset([1])
    FOLLOW_WHEN_in_sig_primary798 = frozenset([27])
    FOLLOW_PG_in_sig_primary800 = frozenset([14, 17, 18, 23, 26, 27, 32, 33])
    FOLLOW_sig_expression1_in_sig_primary805 = frozenset([26])
    FOLLOW_PD_in_sig_primary808 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary838 = frozenset([3])
    FOLLOW_3_in_sig_primary840 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary870 = frozenset([2])
    FOLLOW_2_in_sig_primary872 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary915 = frozenset([1])
    FOLLOW_PG_in_sig_primary956 = frozenset([14, 17, 18, 23, 26, 27, 32, 33])
    FOLLOW_sig_expression1_in_sig_primary960 = frozenset([26])
    FOLLOW_PD_in_sig_primary963 = frozenset([1])
    FOLLOW_T_in_sig_constant1008 = frozenset([1])
    FOLLOW_F_in_sig_constant1023 = frozenset([1])
    FOLLOW_SYNC_in_sig_constraint1075 = frozenset([27])
    FOLLOW_PG_in_sig_constraint1078 = frozenset([6, 14, 17, 18, 23, 27, 32, 33])
    FOLLOW_exp_list_in_sig_constraint1083 = frozenset([26])
    FOLLOW_PD_in_sig_constraint1087 = frozenset([1])
    FOLLOW_EXC_in_sig_constraint1138 = frozenset([27])
    FOLLOW_PG_in_sig_constraint1142 = frozenset([6, 14, 17, 18, 23, 27, 32, 33])
    FOLLOW_exp_list_in_sig_constraint1149 = frozenset([26])
    FOLLOW_PD_in_sig_constraint1152 = frozenset([1])
    FOLLOW_INC_in_sig_constraint1181 = frozenset([27])
    FOLLOW_PG_in_sig_constraint1184 = frozenset([6, 14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_expression1_in_sig_constraint1189 = frozenset([6])
    FOLLOW_COM_in_sig_constraint1192 = frozenset([14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_exp_in_sig_constraint1197 = frozenset([26])
    FOLLOW_PD_in_sig_constraint1200 = frozenset([1])
    FOLLOW_sig_expression1_in_exp_list1257 = frozenset([1, 6])
    FOLLOW_COM_in_exp_list1275 = frozenset([6, 14, 17, 18, 23, 27, 32, 33])
    FOLLOW_sig_expression1_in_exp_list1279 = frozenset([1, 6])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("sigexpr_lexer", sigexpr_compiler)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
