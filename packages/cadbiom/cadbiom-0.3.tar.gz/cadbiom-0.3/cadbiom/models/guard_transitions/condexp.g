// Collect ident names in a boolean expression

grammar condexp;

options {
  language= Python;
  k = 3;
  }
@header{
}
// RULES
// returns the set of ids in boolean expression
sig_bool returns [idents]
      @init{idents = set([])}
        : id1=sig_bool1 DOL {$idents = id1}
        | DOL 
        ;        
               
sig_bool1 returns [idents]
      @init{idents = set([])}
        : id1=sig_bool_and {$idents = id1}
          (OR id2=sig_bool_and {$idents = $idents | id2}
          )*
        ;
        
sig_bool_and returns [idents]
      @init{idents = set([])}
        : id1=sig_primary {$idents = id1}
          (AND id2=sig_primary {$idents =  $idents | id2}
          )*
        ;
        
sig_primary returns [idents]
      @init{idents = set([])}
        : NOT id1=sig_primary
            {$idents = id1} 
            
        | id4=sig_constant
            {$idents = id4}
   
        | id2=IDENT
             {$idents = set([$id2.text.encode("utf8")])}
             
        | PG id3= sig_bool1 PD
             {$idents = id3}
        ;

sig_constant returns [idents]
      @init{idents = set([])}
         : T {$idents = set([])}
         | F {$idents = set([])}
         ;
         
//lexer
WS          :  (' '|'\t'|'\n'){$channel = HIDDEN;};

COMMENT     : '//'(~'\n')*'\n'{$channel = HIDDEN;};

// keywords
AND     : 'and' ;
OR      : 'or' ;
NOT     : 'not';
T       : 'true';
F       : 'false';

PG      : '(' ;
PD      : ')' ;
DOL     : '$';


fragment LETTER   : 'a'..'z'|'A'..'Z'|'_';

fragment DIGIT    : '0'..'9';

IDENT   : ( LETTER|DIGIT )+ ;

         
