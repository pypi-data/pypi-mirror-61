//
// Filename    : chart_lexer.g
// Author(s)   : Michel Le Borgne
// Created     : 4/2010
// Revision    : 
// Source      : 
//
// Copyright 2009 - 2010 : IRISA-IRSET
//
// This library is free software; you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published
// by the Free Software Foundation; either version 2.1 of the License, or
// any later version.
//
// This library is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
// MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
// documentation provided hereunder is on an "as is" basis, and IRISA has
// no obligations to provide maintenance, support, updates, enhancements
// or modifications.
// In no event shall IRISA be liable to any party for direct, indirect,
// special, incidental or consequential damages, including lost profits,
// arising out of the use of this software and its documentation, even if
//  have been advised of the possibility of such damage.  See
// the GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this library; if not, write to the Free Software Foundation,
// Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
//
// The original code contained here was initially developed by:
//
//     Michel Le Borgne.
//     IRISA
//     Symbiose team
//     IRISA  Campus de Beaulieu
//     35042 RENNES Cedex, FRANCE 
//     
//
//     http:
//     mailto:
//
// Contributor(s):
//

lexer grammar sigexpr_lexer; 

options {
  language= Python;
  k = 3;
  }

WS          :  (' '|'\t'|'\n'){$channel = HIDDEN;};

COMMENT     : '//'(~'\n')*'\n'{$channel = HIDDEN;};

// keywords
DEFAULT   : 'default' ;
WHEN    : 'when' ;
EVENT   : 'event';
SYNC    : 'synchro';
EXC     : 'exclus';
INC     :   'included';
SEQ     :   'sequence';
AND     : 'and' ;
OR      : 'or' ;
NOT     : 'not';
T       : 'true';
F       : 'false';
CONSTR  :   'constraint';
//PRIO    :   'priority';
DEF     :   ':=' ;
EG      :   '=';
NOTEG   : '!=';
PG      : '(' ;
PD      : ')' ;
DOL     : '$' ;
COM     : ',' ;
UP      :   '>';
DOWN    :   '<';
CHG     :   '!';
SCOL    :   ';';
PLUS    :   '+';
MINUS   :   '-';
MUL     :   '*';
EXP     :   '^';


fragment LETTER   : 'a'..'z'|'A'..'Z'|'_';

fragment DIGIT    : '0'..'9' ;

//INT     : (DIGIT)+;

IDENT   : (LETTER|DIGIT )+ ;

