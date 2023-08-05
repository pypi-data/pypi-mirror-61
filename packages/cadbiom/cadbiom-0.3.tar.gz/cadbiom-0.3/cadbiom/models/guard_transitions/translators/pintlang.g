// compiler for pint language import

grammar pintlang;

options {
  language= Python;
//  k = 3;
  }
  
@lexer::members{
def set_error_reporter(self, err):
    self.error_reporter = err

def displayRecognitionError(self, tokenNames, re):
    hdr = self.getErrorHeader(re)
    msg = self.getErrorMessage(re, tokenNames)
    self.error_reporter.display(hdr,msg)
    

def displayExceptionMessage(self, e):
    msg = self.getErrorMessage(self, e, tokenNames)
    self.error_reporter.display('',msg)
}
  
@header{
from cadbiom.models.guard_transitions.chart_model import ChartModel
}
@members{
def set_error_reporter(self, err):
    self.error_reporter = err

def displayRecognitionError(self, tokenNames, re):
    hdr = self.getErrorHeader(re)
    msg = self.getErrorMessage(re, tokenNames)
    self.error_reporter.display(hdr,msg)
    

def displayExceptionMessage(self, e):
    msg = self.getErrorMessage(self, e, tokenNames)
    self.error_reporter.display('',msg)
    
def check_process(self, name, level, line):
    line_txt = 'line '+str(line)+':'
    try:
        lev = self.symb_tab[name]
        self.error_reporter.display(line_txt, "Process double declaration: "+id)
    
    except KeyError:
        self.symb_tab[name] = level
        for ii in range(level+1):
            pname = name + '_' + str(ii)
            self.model.get_root().add_simple_node(pname, 0.0, 0.0)
            
def check_action(self, fname, flevel, cname, clevel1, clevel2, line):
    line_txt = 'line '+str(line)+':'
    try:
        lev = self.symb_tab[fname]
        if flevel>lev:
            self.error_reporter(line_txt, "Incorrect level for:"+fname)
            return
    except KeyError:
        self.error_reporter.display(line_txt, "Undeclared process: "+fname)
        return
    try:
        lev = self.symb_tab[cname]
        if clevel1>lev or clevel2>lev:
            self.error_reporter(line_txt, "Incorrect level for:"+cname)
            return
    except KeyError:
        self.error_reporter.display(line_txt, "Undeclared process: "+cname)
        return
        
    n1 = self.model.get_simple_node(cname+'_'+str(clevel1))
    n2 = self.model.get_simple_node(cname+'_'+str(clevel2))
    tr=self.model.get_root().add_transition(n1, n2)
    tr.set_condition(fname+'_'+str(flevel))
    h_name = 'hh_'+str(self.clock_cpt)
    self.clock_cpt +=1
    tr.set_event(h_name)
    self.clock_list.append(h_name)
    return
    
def check_transition(self, cname, clevel1, clevel2, line):
    line_txt = 'line '+str(line)+':'
    try:
        lev = self.symb_tab[cname]
        if clevel1>lev or clevel2>lev:
            self.error_reporter(line_txt, "Incorrect level for:"+cname)
            return
    except KeyError:
        self.error_reporter.display(line_txt, "Undeclared process: "+cname)
        return
        
    n1 = self.model.get_simple_node(cname+'_'+str(clevel1))
    n2 = self.model.get_simple_node(cname+'_'+str(clevel2))
    tr=self.model.get_root().add_transition(n1, n2)
    return tr
    
def check_tt_rhs(self, tr, il ,l_cond):
    line_txt = 'line '+'? :'
    cond = self.tt_translate_lcond(il, l_cond, line_txt)
    tr.set_condition(cond)
    h_name = 'hh_'+str(self.clock_cpt)
    self.clock_cpt +=1
    tr.set_event(h_name)
    self.clock_list.append(h_name)
    
def check_tr_rhs(self, cond, cname, clevel1, clevel2, line):
    line_txt = 'line '+str(line)+':'
    try:
        lev = self.symb_tab[cname]
        if clevel1>lev or clevel2>lev:
            self.error_reporter(line_txt, "Incorrect level for:"+cname)
            return
    except KeyError:
        self.error_reporter.display(line_txt, "Undeclared process: "+cname)
        return
        
    n1 = self.model.get_simple_node(cname+'_'+str(clevel1))
    n2 = self.model.get_simple_node(cname+'_'+str(clevel2))
    tr=self.model.get_root().add_transition(n1, n2)
    tr.set_condition(cond)
    h_name = 'hh_'+str(self.clock_cpt)
    self.clock_cpt +=1
    tr.set_event(h_name)
    self.clock_list.append(h_name)
    
    
def tt_translate_cond(self, id_list, val_list, line_txt):
    if len(id_list) != len(val_list):
        self.error_reporter.display(line_txt, "Bad condition specification"+id_list.__str__())
        return None
    cond = id_list[0] + "_"+str(val_list[0])
    for i in range(1, len(id_list)):
        cond_el = id_list[i] + "_" + str(val_list[i])
        cond = cond + " and "+ cond_el
    return cond
    
    
def tt_translate_lcond(self, id_list, lval_list, line_txt):
    cond_el = self.tt_translate_cond(id_list, lval_list[0], line_txt)
    if cond_el:
        cond = '(' + cond_el + ')'
    else:
        return ""
    for i in range(1,len(lval_list)):
        cond_el = self.tt_translate_cond(id_list, lval_list[i], line_txt)
        if cond_el:
            cond = cond + ' or (' + cond_el + ')'
        else:
            return ""
    return cond
    

}

// RULES
pintspec[model_name]    @init{
              self.model = ChartModel(model_name)
              self.symb_tab = dict()
              self.clock_cpt = 0
              self.clock_list = []}  
           : (process|action|cooper)*  EOF
           ;
           
process
           : PROC id=IDENT  i=INT
              {self.check_process($id.text, int($i.text), id.line)}
           ;
        
action     
           : fid=IDENT flev=INT ARROW cid=IDENT lev1=INT lev2=INT
             {self.check_action($fid.text, int($flev.text), $cid.text, int($lev1.text), int($lev2.text), fid.line)} 
           ;
           
cooper     
           : COOP LP lha=coop_lhs COM coop_rhs[$lha.transition, $lha.id_list, $lha.condition] RP
           ;
           
coop_lhs   returns [transition, id_list, condition]
           : il=sort_list
              {$id_list = il} 
             rc=rcoop_lhs[il]
             {$transition = $rc.transition
              $condition = $rc.condition }
           ;
           
rcoop_lhs [ids] returns [transition, condition]
           : kw=IN_KW  tt=tt_condition cond=tail_logexp
              {$condition = self.tt_translate_lcond(ids, $tt.l_cond,  'line '+str(kw.line)+':') + $cond.cond}
           | ARROW id=IDENT i1=INT i2=INT
             {$transition = self.check_transition($id.text, int($i1.text), int($i2.text), $id.line)}
           ;
           
coop_rhs[tr, il, cond]   
           : tt=tt_condition
            {self.check_tt_rhs(tr,il, $tt.l_cond, )}
           | id=IDENT cc=COM i1=INT  COM i2=INT
            {self.check_tr_rhs(cond, $id.text, int($i1.text), int($i2.text), cc.line)}
           ;
           
sort_list  returns [id_list]
           : LB id1=IDENT  
              {$id_list = [$id1.text]} 
             (SC id2=IDENT {$id_list.append($id2.text)})* RB
           ;
           
tt_condition returns [l_cond]
           : LB tt1=tt_conjunction {$l_cond = [$tt1.lval]}
             (SC tt2=tt_conjunction  {$l_cond.append($tt2.lval)})* RB
           ;
           
tt_conjunction returns [lval]
           :  LB i1=INT {$lval = [int($i1.text)]}
              (SC i2=INT {$lval.append(int($i2.text))} )* RB
           ; 
           
tail_logexp returns [cond]
           : {$cond = ""}
           | AND tt1=tt_logexp
              {$cond = ' and ' + $tt1.cond}
           | OR  tt2=tt_logexp
              {$cond = ' and ' + $tt1.cond}
           | tt_primary
              {$cond = $tt1.cond}
           ;
          
tt_logexp  returns [cond]
           : tt1=tt_logexp2 {$cond = $tt1.cond}
            (OR tt2=tt_logexp2 {$cond = $cond + ' or ' + $tt2.cond})*
           ;
           
tt_logexp2 returns [cond]
           : tt1=tt_primary {$cond = $tt1.cond}
             (AND tt2=tt_primary  {$cond = $cond + ' and ' + $tt2.cond})*
           ;
           
tt_primary returns [cond]
           : NOT tt1=tt_primary
            {$cond = 'not (' + $tt1.cond + ')'}
           | st=sort_list kw=IN_KW tt2=tt_condition
            {$cond = self.tt_translate_lcond($st.id_list, $tt2.l_cond, 'line '+str(kw.line)+':')}
           | LP tt3=tt_logexp RP
            {$cond = '('+$tt3.cond+')'}
           ;
           
           
//lexer


WS          :  (' '|'\t'|'\n'){$channel = HIDDEN;};

COMMENT     : '//'(~'\n')*'\n'{$channel = HIDDEN;};

// keywords
PROC    : 'process' ;
ARROW   : '->';
COOP    : 'COOPERATIVITY' ;
IN_KW   : 'in' ;

LP      : '(' ;
RP      : ')' ;
LB      : '[' ;
RB      : ']' ;
SC      : ';' ;
COM     : ',' ;

AND     : 'and' ;
OR      : 'or' ;
NOT     : 'not';

fragment LETTER   : 'a'..'z'|'A'..'Z'|'_';

fragment DIGIT    : '0'..'9';

IDENT   : LETTER( LETTER|DIGIT )* ;

INT     : DIGIT+ ;