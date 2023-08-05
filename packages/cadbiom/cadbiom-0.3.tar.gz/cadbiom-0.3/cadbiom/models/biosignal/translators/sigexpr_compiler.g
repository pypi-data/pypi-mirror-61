//
// Filename    : chart_compiler.g
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
// IRISA have been advised of the possibility of such damage.  See
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

parser grammar sigexpr_compiler;

options{
    language = Python;
    ASTLabelType = CommonTree;
    k=2;
    tokenVocab = sigexpr_lexer;
    output = AST; 
}

@header{
from cadbiom.models.biosignal.sig_expr import *
import string
}
// auxiliary methods
@members{
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
            
}
// Compiler options and internals

@init{
self.state_events = []
self.free_clocks = []
self.state_only = False
self.state_only_in_bool = False
self.catch_free_clocks = False
self.deep = -1
self.message = ""
self.error_reporter = None
}

// RULES       {$exp = $exp1.exp}
sig_expression[tab_symb] returns [exp]
        : exp1=sig_expression1[tab_symb] DOL
            {$exp = $exp1.exp}
        | exp2 = sig_constraint[tab_symb] DOL
            {$exp = $exp2.exp}
        ;

sig_expression1[tab_symb] returns [exp]
        : exp1=sig_exp[tab_symb] {$exp = $exp1.exp} 
          (DEFAULT^ exp2=sig_exp[tab_symb] 
            {$exp = SigDefaultExpr($exp, $exp2.exp)}
          )* 
// void expressions =  default to True
        | {$exp = SigConstExpr(True)}
        ;
        
sig_exp[tab_symb]  returns [exp] 
        :  exp1=sig_bool[tab_symb] {$exp = $exp1.exp} 
          (WHEN^ 
              {st_only_save = self.state_only; self.state_only = self.state_only_in_bool}
            exp2=sig_bool[tab_symb] 
            {$exp = SigWhenExpr($exp, $exp2.exp) 
             self.state_only = st_only_save}
          )* 
           
        ;
        
sig_bool[tab_symb] returns [exp]
        : exp1=sig_bool_and[tab_symb] {$exp = $exp1.exp }
          (OR^ exp2=sig_bool_and[tab_symb] 
            {$exp = SigSyncBinExpr("or", $exp, $exp2.exp)}
          )*
        ;
        
sig_bool_and[tab_symb] returns [exp]
        : exp1=sig_primary[tab_symb] {$exp = $exp1.exp }
          (AND^ exp2=sig_primary[tab_symb] 
                   {$exp = SigSyncBinExpr("and",$exp, $exp2.exp)}
          )*
        ;
        
sig_primary[tab_symb] returns [exp]
        : NOT^ nexp=sig_primary[tab_symb]
            {$exp = SigNotExpr($nexp.exp)} // TODO
            
        | cexp=sig_constant
            {$exp = $cexp.exp}
                    
        | EVENT PG! exps=sig_expression1[tab_symb] PD!
           {$exp = SigEventExpr($exps.exp)}
          
        | WHEN PG! expw=sig_expression1[tab_symb] PD!
            {$exp = SigWhenExpr(SigConstExpr(True),$expw.exp)}

        | i7=IDENT UP 
            {$exp = self.check_updown(tab_symb, $i7.text, 1)}

        | i8=IDENT DOWN
            {$exp = self.check_updown(tab_symb, $i8.text, 2)}
            
//        | i9=IDENT CHG
//            {$exp = self.check_change(tab_symb, $i9.text)}   
        | id2=IDENT
             {$exp = self.check_ident(tab_symb, self.state_only, self.catch_free_clocks, self.deep, self.message, $id2.text)}
             
        | PG expse=sig_expression1[tab_symb] PD
             {$exp = $expse.exp}
        ;

sig_constant returns [exp]
         : T {$exp = SigConstExpr(True)}
         | F {$exp = SigConstExpr(False)}
         ;
                  
sig_constraint[tab_symb] returns [exp]
         : SYNC^ PG! el=exp_list[tab_symb]  PD!
            {$exp = self.check_sync($el.expl)}          
            
         | EXC^  PG! el = exp_list[tab_symb] PD!
            {$exp = self.check_exclus($el.expl)}

         | INC^ PG! e3=sig_expression1[tab_symb] COM! e4=sig_exp[tab_symb] PD!
            {$exp = self.check_included($e3.exp, $e4.exp)}
         ;
        
exp_list[tab_symb] returns [expl]
         : exp1=sig_expression1[tab_symb] {$expl = [$exp1.exp]}
            (COM exp2=sig_expression1[tab_symb]
              {$expl.append($exp2.exp)}
            )*
         ; 
         
