# $ANTLR 3.5.2 cadbiom/models/guard_transitions/translators/pintlang.g 2018-12-14 16:41:07

import sys
from antlr3 import *
from antlr3.compat import set, frozenset



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
AND=4
ARROW=5
COM=6
COMMENT=7
COOP=8
DIGIT=9
IDENT=10
INT=11
IN_KW=12
LB=13
LETTER=14
LP=15
NOT=16
OR=17
PROC=18
RB=19
RP=20
SC=21
WS=22


class pintlangLexer(Lexer):

    grammarFileName = "cadbiom/models/guard_transitions/translators/pintlang.g"
    api_version = 1

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(pintlangLexer, self).__init__(input, state)

        self.delegates = []




                            
    def set_error_reporter(self, err):
        self.error_reporter = err

    def displayRecognitionError(self, tokenNames, re):
        hdr = self.getErrorHeader(re)
        msg = self.getErrorMessage(re, tokenNames)
        self.error_reporter.display(hdr,msg)
        

    def displayExceptionMessage(self, e):
        msg = self.getErrorMessage(self, e, tokenNames)
        self.error_reporter.display('',msg)



    # $ANTLR start "WS"
    def mWS(self, ):
        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:251:13: ( ( ' ' | '\\t' | '\\n' ) )
            # cadbiom/models/guard_transitions/translators/pintlang.g:251:16: ( ' ' | '\\t' | '\\n' )
            pass 
            if (9 <= self.input.LA(1) <= 10) or self.input.LA(1) == 32:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse



            #action start
            _channel = HIDDEN;
            #action end




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "WS"



    # $ANTLR start "COMMENT"
    def mCOMMENT(self, ):
        try:
            _type = COMMENT
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:253:13: ( '//' (~ '\\n' )* '\\n' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:253:15: '//' (~ '\\n' )* '\\n'
            pass 
            self.match("//")


            # cadbiom/models/guard_transitions/translators/pintlang.g:253:19: (~ '\\n' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((0 <= LA1_0 <= 9) or (11 <= LA1_0 <= 65535)) :
                    alt1 = 1


                if alt1 == 1:
                    # cadbiom/models/guard_transitions/translators/pintlang.g:
                    pass 
                    if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop1


            self.match(10)

            #action start
            _channel = HIDDEN;
            #action end




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "COMMENT"



    # $ANTLR start "PROC"
    def mPROC(self, ):
        try:
            _type = PROC
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:256:9: ( 'process' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:256:11: 'process'
            pass 
            self.match("process")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "PROC"



    # $ANTLR start "ARROW"
    def mARROW(self, ):
        try:
            _type = ARROW
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:257:9: ( '->' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:257:11: '->'
            pass 
            self.match("->")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "ARROW"



    # $ANTLR start "COOP"
    def mCOOP(self, ):
        try:
            _type = COOP
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:258:9: ( 'COOPERATIVITY' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:258:11: 'COOPERATIVITY'
            pass 
            self.match("COOPERATIVITY")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "COOP"



    # $ANTLR start "IN_KW"
    def mIN_KW(self, ):
        try:
            _type = IN_KW
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:259:9: ( 'in' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:259:11: 'in'
            pass 
            self.match("in")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "IN_KW"



    # $ANTLR start "LP"
    def mLP(self, ):
        try:
            _type = LP
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:261:9: ( '(' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:261:11: '('
            pass 
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "LP"



    # $ANTLR start "RP"
    def mRP(self, ):
        try:
            _type = RP
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:262:9: ( ')' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:262:11: ')'
            pass 
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "RP"



    # $ANTLR start "LB"
    def mLB(self, ):
        try:
            _type = LB
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:263:9: ( '[' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:263:11: '['
            pass 
            self.match(91)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "LB"



    # $ANTLR start "RB"
    def mRB(self, ):
        try:
            _type = RB
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:264:9: ( ']' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:264:11: ']'
            pass 
            self.match(93)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "RB"



    # $ANTLR start "SC"
    def mSC(self, ):
        try:
            _type = SC
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:265:9: ( ';' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:265:11: ';'
            pass 
            self.match(59)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "SC"



    # $ANTLR start "COM"
    def mCOM(self, ):
        try:
            _type = COM
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:266:9: ( ',' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:266:11: ','
            pass 
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "COM"



    # $ANTLR start "AND"
    def mAND(self, ):
        try:
            _type = AND
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:268:9: ( 'and' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:268:11: 'and'
            pass 
            self.match("and")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "AND"



    # $ANTLR start "OR"
    def mOR(self, ):
        try:
            _type = OR
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:269:9: ( 'or' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:269:11: 'or'
            pass 
            self.match("or")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "OR"



    # $ANTLR start "NOT"
    def mNOT(self, ):
        try:
            _type = NOT
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:270:9: ( 'not' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:270:11: 'not'
            pass 
            self.match("not")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "NOT"



    # $ANTLR start "LETTER"
    def mLETTER(self, ):
        try:
            # cadbiom/models/guard_transitions/translators/pintlang.g:272:19: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:
            pass 
            if (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:
            pass

    # $ANTLR end "LETTER"



    # $ANTLR start "DIGIT"
    def mDIGIT(self, ):
        try:
            # cadbiom/models/guard_transitions/translators/pintlang.g:274:19: ( '0' .. '9' )
            # cadbiom/models/guard_transitions/translators/pintlang.g:
            pass 
            if (48 <= self.input.LA(1) <= 57):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:
            pass

    # $ANTLR end "DIGIT"



    # $ANTLR start "IDENT"
    def mIDENT(self, ):
        try:
            _type = IDENT
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:276:9: ( LETTER ( LETTER | DIGIT )* )
            # cadbiom/models/guard_transitions/translators/pintlang.g:276:11: LETTER ( LETTER | DIGIT )*
            pass 
            self.mLETTER()


            # cadbiom/models/guard_transitions/translators/pintlang.g:276:17: ( LETTER | DIGIT )*
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((48 <= LA2_0 <= 57) or (65 <= LA2_0 <= 90) or LA2_0 == 95 or (97 <= LA2_0 <= 122)) :
                    alt2 = 1


                if alt2 == 1:
                    # cadbiom/models/guard_transitions/translators/pintlang.g:
                    pass 
                    if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop2




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "IDENT"



    # $ANTLR start "INT"
    def mINT(self, ):
        try:
            _type = INT
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/translators/pintlang.g:278:9: ( ( DIGIT )+ )
            # cadbiom/models/guard_transitions/translators/pintlang.g:278:11: ( DIGIT )+
            pass 
            # cadbiom/models/guard_transitions/translators/pintlang.g:278:11: ( DIGIT )+
            cnt3 = 0
            while True: #loop3
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((48 <= LA3_0 <= 57)) :
                    alt3 = 1


                if alt3 == 1:
                    # cadbiom/models/guard_transitions/translators/pintlang.g:
                    pass 
                    if (48 <= self.input.LA(1) <= 57):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt3 >= 1:
                        break #loop3

                    eee = EarlyExitException(3, self.input)
                    raise eee

                cnt3 += 1




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "INT"



    def mTokens(self):
        # cadbiom/models/guard_transitions/translators/pintlang.g:1:8: ( WS | COMMENT | PROC | ARROW | COOP | IN_KW | LP | RP | LB | RB | SC | COM | AND | OR | NOT | IDENT | INT )
        alt4 = 17
        LA4 = self.input.LA(1)
        if LA4 == 9 or LA4 == 10 or LA4 == 32:
            alt4 = 1
        elif LA4 == 47:
            alt4 = 2
        elif LA4 == 112:
            LA4_3 = self.input.LA(2)

            if (LA4_3 == 114) :
                LA4_18 = self.input.LA(3)

                if (LA4_18 == 111) :
                    LA4_24 = self.input.LA(4)

                    if (LA4_24 == 99) :
                        LA4_30 = self.input.LA(5)

                        if (LA4_30 == 101) :
                            LA4_34 = self.input.LA(6)

                            if (LA4_34 == 115) :
                                LA4_36 = self.input.LA(7)

                                if (LA4_36 == 115) :
                                    LA4_38 = self.input.LA(8)

                                    if ((48 <= LA4_38 <= 57) or (65 <= LA4_38 <= 90) or LA4_38 == 95 or (97 <= LA4_38 <= 122)) :
                                        alt4 = 16
                                    else:
                                        alt4 = 3

                                else:
                                    alt4 = 16

                            else:
                                alt4 = 16

                        else:
                            alt4 = 16

                    else:
                        alt4 = 16

                else:
                    alt4 = 16

            else:
                alt4 = 16

        elif LA4 == 45:
            alt4 = 4
        elif LA4 == 67:
            LA4_5 = self.input.LA(2)

            if (LA4_5 == 79) :
                LA4_19 = self.input.LA(3)

                if (LA4_19 == 79) :
                    LA4_25 = self.input.LA(4)

                    if (LA4_25 == 80) :
                        LA4_31 = self.input.LA(5)

                        if (LA4_31 == 69) :
                            LA4_35 = self.input.LA(6)

                            if (LA4_35 == 82) :
                                LA4_37 = self.input.LA(7)

                                if (LA4_37 == 65) :
                                    LA4_39 = self.input.LA(8)

                                    if (LA4_39 == 84) :
                                        LA4_41 = self.input.LA(9)

                                        if (LA4_41 == 73) :
                                            LA4_42 = self.input.LA(10)

                                            if (LA4_42 == 86) :
                                                LA4_43 = self.input.LA(11)

                                                if (LA4_43 == 73) :
                                                    LA4_44 = self.input.LA(12)

                                                    if (LA4_44 == 84) :
                                                        LA4_45 = self.input.LA(13)

                                                        if (LA4_45 == 89) :
                                                            LA4_46 = self.input.LA(14)

                                                            if ((48 <= LA4_46 <= 57) or (65 <= LA4_46 <= 90) or LA4_46 == 95 or (97 <= LA4_46 <= 122)) :
                                                                alt4 = 16
                                                            else:
                                                                alt4 = 5

                                                        else:
                                                            alt4 = 16

                                                    else:
                                                        alt4 = 16

                                                else:
                                                    alt4 = 16

                                            else:
                                                alt4 = 16

                                        else:
                                            alt4 = 16

                                    else:
                                        alt4 = 16

                                else:
                                    alt4 = 16

                            else:
                                alt4 = 16

                        else:
                            alt4 = 16

                    else:
                        alt4 = 16

                else:
                    alt4 = 16

            else:
                alt4 = 16

        elif LA4 == 105:
            LA4_6 = self.input.LA(2)

            if (LA4_6 == 110) :
                LA4_20 = self.input.LA(3)

                if ((48 <= LA4_20 <= 57) or (65 <= LA4_20 <= 90) or LA4_20 == 95 or (97 <= LA4_20 <= 122)) :
                    alt4 = 16
                else:
                    alt4 = 6

            else:
                alt4 = 16

        elif LA4 == 40:
            alt4 = 7
        elif LA4 == 41:
            alt4 = 8
        elif LA4 == 91:
            alt4 = 9
        elif LA4 == 93:
            alt4 = 10
        elif LA4 == 59:
            alt4 = 11
        elif LA4 == 44:
            alt4 = 12
        elif LA4 == 97:
            LA4_13 = self.input.LA(2)

            if (LA4_13 == 110) :
                LA4_21 = self.input.LA(3)

                if (LA4_21 == 100) :
                    LA4_27 = self.input.LA(4)

                    if ((48 <= LA4_27 <= 57) or (65 <= LA4_27 <= 90) or LA4_27 == 95 or (97 <= LA4_27 <= 122)) :
                        alt4 = 16
                    else:
                        alt4 = 13

                else:
                    alt4 = 16

            else:
                alt4 = 16

        elif LA4 == 111:
            LA4_14 = self.input.LA(2)

            if (LA4_14 == 114) :
                LA4_22 = self.input.LA(3)

                if ((48 <= LA4_22 <= 57) or (65 <= LA4_22 <= 90) or LA4_22 == 95 or (97 <= LA4_22 <= 122)) :
                    alt4 = 16
                else:
                    alt4 = 14

            else:
                alt4 = 16

        elif LA4 == 110:
            LA4_15 = self.input.LA(2)

            if (LA4_15 == 111) :
                LA4_23 = self.input.LA(3)

                if (LA4_23 == 116) :
                    LA4_29 = self.input.LA(4)

                    if ((48 <= LA4_29 <= 57) or (65 <= LA4_29 <= 90) or LA4_29 == 95 or (97 <= LA4_29 <= 122)) :
                        alt4 = 16
                    else:
                        alt4 = 15

                else:
                    alt4 = 16

            else:
                alt4 = 16

        elif LA4 == 65 or LA4 == 66 or LA4 == 68 or LA4 == 69 or LA4 == 70 or LA4 == 71 or LA4 == 72 or LA4 == 73 or LA4 == 74 or LA4 == 75 or LA4 == 76 or LA4 == 77 or LA4 == 78 or LA4 == 79 or LA4 == 80 or LA4 == 81 or LA4 == 82 or LA4 == 83 or LA4 == 84 or LA4 == 85 or LA4 == 86 or LA4 == 87 or LA4 == 88 or LA4 == 89 or LA4 == 90 or LA4 == 95 or LA4 == 98 or LA4 == 99 or LA4 == 100 or LA4 == 101 or LA4 == 102 or LA4 == 103 or LA4 == 104 or LA4 == 106 or LA4 == 107 or LA4 == 108 or LA4 == 109 or LA4 == 113 or LA4 == 114 or LA4 == 115 or LA4 == 116 or LA4 == 117 or LA4 == 118 or LA4 == 119 or LA4 == 120 or LA4 == 121 or LA4 == 122:
            alt4 = 16
        elif LA4 == 48 or LA4 == 49 or LA4 == 50 or LA4 == 51 or LA4 == 52 or LA4 == 53 or LA4 == 54 or LA4 == 55 or LA4 == 56 or LA4 == 57:
            alt4 = 17
        else:
            nvae = NoViableAltException("", 4, 0, self.input)

            raise nvae


        if alt4 == 1:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:10: WS
            pass 
            self.mWS()



        elif alt4 == 2:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:13: COMMENT
            pass 
            self.mCOMMENT()



        elif alt4 == 3:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:21: PROC
            pass 
            self.mPROC()



        elif alt4 == 4:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:26: ARROW
            pass 
            self.mARROW()



        elif alt4 == 5:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:32: COOP
            pass 
            self.mCOOP()



        elif alt4 == 6:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:37: IN_KW
            pass 
            self.mIN_KW()



        elif alt4 == 7:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:43: LP
            pass 
            self.mLP()



        elif alt4 == 8:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:46: RP
            pass 
            self.mRP()



        elif alt4 == 9:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:49: LB
            pass 
            self.mLB()



        elif alt4 == 10:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:52: RB
            pass 
            self.mRB()



        elif alt4 == 11:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:55: SC
            pass 
            self.mSC()



        elif alt4 == 12:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:58: COM
            pass 
            self.mCOM()



        elif alt4 == 13:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:62: AND
            pass 
            self.mAND()



        elif alt4 == 14:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:66: OR
            pass 
            self.mOR()



        elif alt4 == 15:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:69: NOT
            pass 
            self.mNOT()



        elif alt4 == 16:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:73: IDENT
            pass 
            self.mIDENT()



        elif alt4 == 17:
            # cadbiom/models/guard_transitions/translators/pintlang.g:1:79: INT
            pass 
            self.mINT()








 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(pintlangLexer)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
