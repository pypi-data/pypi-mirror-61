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


class condexpLexer(Lexer):

    grammarFileName = "cadbiom/models/guard_transitions/condexp.g"
    api_version = 1

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(condexpLexer, self).__init__(input, state)

        self.delegates = []






    # $ANTLR start "WS"
    def mWS(self, ):
        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/condexp.g:55:13: ( ( ' ' | '\\t' | '\\n' ) )
            # cadbiom/models/guard_transitions/condexp.g:55:16: ( ' ' | '\\t' | '\\n' )
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

            # cadbiom/models/guard_transitions/condexp.g:57:13: ( '//' (~ '\\n' )* '\\n' )
            # cadbiom/models/guard_transitions/condexp.g:57:15: '//' (~ '\\n' )* '\\n'
            pass 
            self.match("//")


            # cadbiom/models/guard_transitions/condexp.g:57:19: (~ '\\n' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((0 <= LA1_0 <= 9) or (11 <= LA1_0 <= 65535)) :
                    alt1 = 1


                if alt1 == 1:
                    # cadbiom/models/guard_transitions/condexp.g:
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



    # $ANTLR start "AND"
    def mAND(self, ):
        try:
            _type = AND
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/condexp.g:60:9: ( 'and' )
            # cadbiom/models/guard_transitions/condexp.g:60:11: 'and'
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

            # cadbiom/models/guard_transitions/condexp.g:61:9: ( 'or' )
            # cadbiom/models/guard_transitions/condexp.g:61:11: 'or'
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

            # cadbiom/models/guard_transitions/condexp.g:62:9: ( 'not' )
            # cadbiom/models/guard_transitions/condexp.g:62:11: 'not'
            pass 
            self.match("not")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "NOT"



    # $ANTLR start "T"
    def mT(self, ):
        try:
            _type = T
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/condexp.g:63:9: ( 'true' )
            # cadbiom/models/guard_transitions/condexp.g:63:11: 'true'
            pass 
            self.match("true")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T"



    # $ANTLR start "F"
    def mF(self, ):
        try:
            _type = F
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/condexp.g:64:9: ( 'false' )
            # cadbiom/models/guard_transitions/condexp.g:64:11: 'false'
            pass 
            self.match("false")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "F"



    # $ANTLR start "PG"
    def mPG(self, ):
        try:
            _type = PG
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/condexp.g:66:9: ( '(' )
            # cadbiom/models/guard_transitions/condexp.g:66:11: '('
            pass 
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "PG"



    # $ANTLR start "PD"
    def mPD(self, ):
        try:
            _type = PD
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/condexp.g:67:9: ( ')' )
            # cadbiom/models/guard_transitions/condexp.g:67:11: ')'
            pass 
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "PD"



    # $ANTLR start "DOL"
    def mDOL(self, ):
        try:
            _type = DOL
            _channel = DEFAULT_CHANNEL

            # cadbiom/models/guard_transitions/condexp.g:68:9: ( '$' )
            # cadbiom/models/guard_transitions/condexp.g:68:11: '$'
            pass 
            self.match(36)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "DOL"



    # $ANTLR start "LETTER"
    def mLETTER(self, ):
        try:
            # cadbiom/models/guard_transitions/condexp.g:71:19: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )
            # cadbiom/models/guard_transitions/condexp.g:
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
            # cadbiom/models/guard_transitions/condexp.g:73:19: ( '0' .. '9' )
            # cadbiom/models/guard_transitions/condexp.g:
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

            # cadbiom/models/guard_transitions/condexp.g:75:9: ( ( LETTER | DIGIT )+ )
            # cadbiom/models/guard_transitions/condexp.g:75:11: ( LETTER | DIGIT )+
            pass 
            # cadbiom/models/guard_transitions/condexp.g:75:11: ( LETTER | DIGIT )+
            cnt2 = 0
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((48 <= LA2_0 <= 57) or (65 <= LA2_0 <= 90) or LA2_0 == 95 or (97 <= LA2_0 <= 122)) :
                    alt2 = 1


                if alt2 == 1:
                    # cadbiom/models/guard_transitions/condexp.g:
                    pass 
                    if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt2 >= 1:
                        break #loop2

                    eee = EarlyExitException(2, self.input)
                    raise eee

                cnt2 += 1




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "IDENT"



    def mTokens(self):
        # cadbiom/models/guard_transitions/condexp.g:1:8: ( WS | COMMENT | AND | OR | NOT | T | F | PG | PD | DOL | IDENT )
        alt3 = 11
        LA3 = self.input.LA(1)
        if LA3 == 9 or LA3 == 10 or LA3 == 32:
            alt3 = 1
        elif LA3 == 47:
            alt3 = 2
        elif LA3 == 97:
            LA3_3 = self.input.LA(2)

            if (LA3_3 == 110) :
                LA3_12 = self.input.LA(3)

                if (LA3_12 == 100) :
                    LA3_17 = self.input.LA(4)

                    if ((48 <= LA3_17 <= 57) or (65 <= LA3_17 <= 90) or LA3_17 == 95 or (97 <= LA3_17 <= 122)) :
                        alt3 = 11
                    else:
                        alt3 = 3

                else:
                    alt3 = 11

            else:
                alt3 = 11

        elif LA3 == 111:
            LA3_4 = self.input.LA(2)

            if (LA3_4 == 114) :
                LA3_13 = self.input.LA(3)

                if ((48 <= LA3_13 <= 57) or (65 <= LA3_13 <= 90) or LA3_13 == 95 or (97 <= LA3_13 <= 122)) :
                    alt3 = 11
                else:
                    alt3 = 4

            else:
                alt3 = 11

        elif LA3 == 110:
            LA3_5 = self.input.LA(2)

            if (LA3_5 == 111) :
                LA3_14 = self.input.LA(3)

                if (LA3_14 == 116) :
                    LA3_19 = self.input.LA(4)

                    if ((48 <= LA3_19 <= 57) or (65 <= LA3_19 <= 90) or LA3_19 == 95 or (97 <= LA3_19 <= 122)) :
                        alt3 = 11
                    else:
                        alt3 = 5

                else:
                    alt3 = 11

            else:
                alt3 = 11

        elif LA3 == 116:
            LA3_6 = self.input.LA(2)

            if (LA3_6 == 114) :
                LA3_15 = self.input.LA(3)

                if (LA3_15 == 117) :
                    LA3_20 = self.input.LA(4)

                    if (LA3_20 == 101) :
                        LA3_24 = self.input.LA(5)

                        if ((48 <= LA3_24 <= 57) or (65 <= LA3_24 <= 90) or LA3_24 == 95 or (97 <= LA3_24 <= 122)) :
                            alt3 = 11
                        else:
                            alt3 = 6

                    else:
                        alt3 = 11

                else:
                    alt3 = 11

            else:
                alt3 = 11

        elif LA3 == 102:
            LA3_7 = self.input.LA(2)

            if (LA3_7 == 97) :
                LA3_16 = self.input.LA(3)

                if (LA3_16 == 108) :
                    LA3_21 = self.input.LA(4)

                    if (LA3_21 == 115) :
                        LA3_25 = self.input.LA(5)

                        if (LA3_25 == 101) :
                            LA3_27 = self.input.LA(6)

                            if ((48 <= LA3_27 <= 57) or (65 <= LA3_27 <= 90) or LA3_27 == 95 or (97 <= LA3_27 <= 122)) :
                                alt3 = 11
                            else:
                                alt3 = 7

                        else:
                            alt3 = 11

                    else:
                        alt3 = 11

                else:
                    alt3 = 11

            else:
                alt3 = 11

        elif LA3 == 40:
            alt3 = 8
        elif LA3 == 41:
            alt3 = 9
        elif LA3 == 36:
            alt3 = 10
        elif LA3 == 48 or LA3 == 49 or LA3 == 50 or LA3 == 51 or LA3 == 52 or LA3 == 53 or LA3 == 54 or LA3 == 55 or LA3 == 56 or LA3 == 57 or LA3 == 65 or LA3 == 66 or LA3 == 67 or LA3 == 68 or LA3 == 69 or LA3 == 70 or LA3 == 71 or LA3 == 72 or LA3 == 73 or LA3 == 74 or LA3 == 75 or LA3 == 76 or LA3 == 77 or LA3 == 78 or LA3 == 79 or LA3 == 80 or LA3 == 81 or LA3 == 82 or LA3 == 83 or LA3 == 84 or LA3 == 85 or LA3 == 86 or LA3 == 87 or LA3 == 88 or LA3 == 89 or LA3 == 90 or LA3 == 95 or LA3 == 98 or LA3 == 99 or LA3 == 100 or LA3 == 101 or LA3 == 103 or LA3 == 104 or LA3 == 105 or LA3 == 106 or LA3 == 107 or LA3 == 108 or LA3 == 109 or LA3 == 112 or LA3 == 113 or LA3 == 114 or LA3 == 115 or LA3 == 117 or LA3 == 118 or LA3 == 119 or LA3 == 120 or LA3 == 121 or LA3 == 122:
            alt3 = 11
        else:
            nvae = NoViableAltException("", 3, 0, self.input)

            raise nvae


        if alt3 == 1:
            # cadbiom/models/guard_transitions/condexp.g:1:10: WS
            pass 
            self.mWS()



        elif alt3 == 2:
            # cadbiom/models/guard_transitions/condexp.g:1:13: COMMENT
            pass 
            self.mCOMMENT()



        elif alt3 == 3:
            # cadbiom/models/guard_transitions/condexp.g:1:21: AND
            pass 
            self.mAND()



        elif alt3 == 4:
            # cadbiom/models/guard_transitions/condexp.g:1:25: OR
            pass 
            self.mOR()



        elif alt3 == 5:
            # cadbiom/models/guard_transitions/condexp.g:1:28: NOT
            pass 
            self.mNOT()



        elif alt3 == 6:
            # cadbiom/models/guard_transitions/condexp.g:1:32: T
            pass 
            self.mT()



        elif alt3 == 7:
            # cadbiom/models/guard_transitions/condexp.g:1:34: F
            pass 
            self.mF()



        elif alt3 == 8:
            # cadbiom/models/guard_transitions/condexp.g:1:36: PG
            pass 
            self.mPG()



        elif alt3 == 9:
            # cadbiom/models/guard_transitions/condexp.g:1:39: PD
            pass 
            self.mPD()



        elif alt3 == 10:
            # cadbiom/models/guard_transitions/condexp.g:1:42: DOL
            pass 
            self.mDOL()



        elif alt3 == 11:
            # cadbiom/models/guard_transitions/condexp.g:1:46: IDENT
            pass 
            self.mIDENT()








 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(condexpLexer)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
