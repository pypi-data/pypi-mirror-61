# $ANTLR 3.5.2 cadbiom/models/guard_transitions/condexp.g 2018-12-14 16:41:06

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

       



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
AND=4
COMMENT=5
DIGIT=6
DOL=7
F=8
IDENT=9
LETTER=10
NOT=11
OR=12
PD=13
PG=14
T=15
WS=16

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "AND", "COMMENT", "DIGIT", "DOL", "F", "IDENT", "LETTER", "NOT", "OR", 
    "PD", "PG", "T", "WS"
]




class condexpParser(Parser):
    grammarFileName = "cadbiom/models/guard_transitions/condexp.g"
    api_version = 1
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(condexpParser, self).__init__(input, state, *args, **kwargs)




        self.delegates = []






    # $ANTLR start "sig_bool"
    # cadbiom/models/guard_transitions/condexp.g:13:1: sig_bool returns [idents] : (id1= sig_bool1 DOL | DOL );
    def sig_bool(self, ):
        idents = None


        id1 = None

        idents = set([])
        try:
            try:
                # cadbiom/models/guard_transitions/condexp.g:15:9: (id1= sig_bool1 DOL | DOL )
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((F <= LA1_0 <= IDENT) or LA1_0 == NOT or (PG <= LA1_0 <= T)) :
                    alt1 = 1
                elif (LA1_0 == DOL) :
                    alt1 = 2
                else:
                    nvae = NoViableAltException("", 1, 0, self.input)

                    raise nvae


                if alt1 == 1:
                    # cadbiom/models/guard_transitions/condexp.g:15:11: id1= sig_bool1 DOL
                    pass 
                    self._state.following.append(self.FOLLOW_sig_bool1_in_sig_bool65)
                    id1 = self.sig_bool1()

                    self._state.following.pop()

                    self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_bool67)

                    #action start
                    idents = id1
                    #action end



                elif alt1 == 2:
                    # cadbiom/models/guard_transitions/condexp.g:16:11: DOL
                    pass 
                    self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_bool81)



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)

        finally:
            pass
        return idents

    # $ANTLR end "sig_bool"



    # $ANTLR start "sig_bool1"
    # cadbiom/models/guard_transitions/condexp.g:19:1: sig_bool1 returns [idents] : id1= sig_bool_and ( OR id2= sig_bool_and )* ;
    def sig_bool1(self, ):
        idents = None


        id1 = None
        id2 = None

        idents = set([])
        try:
            try:
                # cadbiom/models/guard_transitions/condexp.g:21:9: (id1= sig_bool_and ( OR id2= sig_bool_and )* )
                # cadbiom/models/guard_transitions/condexp.g:21:11: id1= sig_bool_and ( OR id2= sig_bool_and )*
                pass 
                self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool1146)
                id1 = self.sig_bool_and()

                self._state.following.pop()

                #action start
                idents = id1
                #action end


                # cadbiom/models/guard_transitions/condexp.g:22:11: ( OR id2= sig_bool_and )*
                while True: #loop2
                    alt2 = 2
                    LA2_0 = self.input.LA(1)

                    if (LA2_0 == OR) :
                        alt2 = 1


                    if alt2 == 1:
                        # cadbiom/models/guard_transitions/condexp.g:22:12: OR id2= sig_bool_and
                        pass 
                        self.match(self.input, OR, self.FOLLOW_OR_in_sig_bool1161)

                        self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool1165)
                        id2 = self.sig_bool_and()

                        self._state.following.pop()

                        #action start
                        idents = idents | id2
                        #action end



                    else:
                        break #loop2





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)

        finally:
            pass
        return idents

    # $ANTLR end "sig_bool1"



    # $ANTLR start "sig_bool_and"
    # cadbiom/models/guard_transitions/condexp.g:26:1: sig_bool_and returns [idents] : id1= sig_primary ( AND id2= sig_primary )* ;
    def sig_bool_and(self, ):
        idents = None


        id1 = None
        id2 = None

        idents = set([])
        try:
            try:
                # cadbiom/models/guard_transitions/condexp.g:28:9: (id1= sig_primary ( AND id2= sig_primary )* )
                # cadbiom/models/guard_transitions/condexp.g:28:11: id1= sig_primary ( AND id2= sig_primary )*
                pass 
                self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and229)
                id1 = self.sig_primary()

                self._state.following.pop()

                #action start
                idents = id1
                #action end


                # cadbiom/models/guard_transitions/condexp.g:29:11: ( AND id2= sig_primary )*
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == AND) :
                        alt3 = 1


                    if alt3 == 1:
                        # cadbiom/models/guard_transitions/condexp.g:29:12: AND id2= sig_primary
                        pass 
                        self.match(self.input, AND, self.FOLLOW_AND_in_sig_bool_and244)

                        self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and248)
                        id2 = self.sig_primary()

                        self._state.following.pop()

                        #action start
                        idents =  idents | id2
                        #action end



                    else:
                        break #loop3





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)

        finally:
            pass
        return idents

    # $ANTLR end "sig_bool_and"



    # $ANTLR start "sig_primary"
    # cadbiom/models/guard_transitions/condexp.g:33:1: sig_primary returns [idents] : ( NOT id1= sig_primary |id4= sig_constant |id2= IDENT | PG id3= sig_bool1 PD );
    def sig_primary(self, ):
        idents = None


        id2 = None
        id1 = None
        id4 = None
        id3 = None

        idents = set([])
        try:
            try:
                # cadbiom/models/guard_transitions/condexp.g:35:9: ( NOT id1= sig_primary |id4= sig_constant |id2= IDENT | PG id3= sig_bool1 PD )
                alt4 = 4
                LA4 = self.input.LA(1)
                if LA4 == NOT:
                    alt4 = 1
                elif LA4 == F or LA4 == T:
                    alt4 = 2
                elif LA4 == IDENT:
                    alt4 = 3
                elif LA4 == PG:
                    alt4 = 4
                else:
                    nvae = NoViableAltException("", 4, 0, self.input)

                    raise nvae


                if alt4 == 1:
                    # cadbiom/models/guard_transitions/condexp.g:35:11: NOT id1= sig_primary
                    pass 
                    self.match(self.input, NOT, self.FOLLOW_NOT_in_sig_primary310)

                    self._state.following.append(self.FOLLOW_sig_primary_in_sig_primary314)
                    id1 = self.sig_primary()

                    self._state.following.pop()

                    #action start
                    idents = id1
                    #action end



                elif alt4 == 2:
                    # cadbiom/models/guard_transitions/condexp.g:38:11: id4= sig_constant
                    pass 
                    self._state.following.append(self.FOLLOW_sig_constant_in_sig_primary356)
                    id4 = self.sig_constant()

                    self._state.following.pop()

                    #action start
                    idents = id4
                    #action end



                elif alt4 == 3:
                    # cadbiom/models/guard_transitions/condexp.g:41:11: id2= IDENT
                    pass 
                    id2 = self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary388)

                    #action start
                    idents = set([id2.text.encode("utf8")])
                    #action end



                elif alt4 == 4:
                    # cadbiom/models/guard_transitions/condexp.g:44:11: PG id3= sig_bool1 PD
                    pass 
                    self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary429)

                    self._state.following.append(self.FOLLOW_sig_bool1_in_sig_primary434)
                    id3 = self.sig_bool1()

                    self._state.following.pop()

                    self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary436)

                    #action start
                    idents = id3
                    #action end




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)

        finally:
            pass
        return idents

    # $ANTLR end "sig_primary"



    # $ANTLR start "sig_constant"
    # cadbiom/models/guard_transitions/condexp.g:48:1: sig_constant returns [idents] : ( T | F );
    def sig_constant(self, ):
        idents = None


        idents = set([])
        try:
            try:
                # cadbiom/models/guard_transitions/condexp.g:50:10: ( T | F )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == T) :
                    alt5 = 1
                elif (LA5_0 == F) :
                    alt5 = 2
                else:
                    nvae = NoViableAltException("", 5, 0, self.input)

                    raise nvae


                if alt5 == 1:
                    # cadbiom/models/guard_transitions/condexp.g:50:12: T
                    pass 
                    self.match(self.input, T, self.FOLLOW_T_in_sig_constant491)

                    #action start
                    idents = set([])
                    #action end



                elif alt5 == 2:
                    # cadbiom/models/guard_transitions/condexp.g:51:12: F
                    pass 
                    self.match(self.input, F, self.FOLLOW_F_in_sig_constant506)

                    #action start
                    idents = set([])
                    #action end




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)

        finally:
            pass
        return idents

    # $ANTLR end "sig_constant"



 

    FOLLOW_sig_bool1_in_sig_bool65 = frozenset([7])
    FOLLOW_DOL_in_sig_bool67 = frozenset([1])
    FOLLOW_DOL_in_sig_bool81 = frozenset([1])
    FOLLOW_sig_bool_and_in_sig_bool1146 = frozenset([1, 12])
    FOLLOW_OR_in_sig_bool1161 = frozenset([8, 9, 11, 14, 15])
    FOLLOW_sig_bool_and_in_sig_bool1165 = frozenset([1, 12])
    FOLLOW_sig_primary_in_sig_bool_and229 = frozenset([1, 4])
    FOLLOW_AND_in_sig_bool_and244 = frozenset([8, 9, 11, 14, 15])
    FOLLOW_sig_primary_in_sig_bool_and248 = frozenset([1, 4])
    FOLLOW_NOT_in_sig_primary310 = frozenset([8, 9, 11, 14, 15])
    FOLLOW_sig_primary_in_sig_primary314 = frozenset([1])
    FOLLOW_sig_constant_in_sig_primary356 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary388 = frozenset([1])
    FOLLOW_PG_in_sig_primary429 = frozenset([8, 9, 11, 14, 15])
    FOLLOW_sig_bool1_in_sig_primary434 = frozenset([13])
    FOLLOW_PD_in_sig_primary436 = frozenset([1])
    FOLLOW_T_in_sig_constant491 = frozenset([1])
    FOLLOW_F_in_sig_constant506 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("condexpLexer", condexpParser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
