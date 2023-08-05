 // read a textual description of a chart model and build it

grammar cadlang;

options {
  language= Python;
 //k = 3;
  output = AST; // hack
  }
  
@lexer::members{
def set_error_reporter(self, err):
    self.error_reporter = err

def displayRecognitionError(self, tokenNames, re):
    hdr = self.getErrorHeader(re)
    msg = self.getErrorMessage(re, tokenNames)
    self.error_reporter.display(hdr+' '+msg)
    

def displayExceptionMessage(self, e):
    msg = self.getErrorMessage(self, e, tokenNames)
    self.error_reporter.display(msg)
}
  
@header{

}

@members{
def set_error_reporter(self, err):
    self.error_reporter = err

def displayRecognitionError(self, tokenNames, re):
    hdr = self.getErrorHeader(re)
    msg = self.getErrorMessage(re, tokenNames)
    self.error_reporter.display(hdr+' '+msg)
    

def displayExceptionMessage(self, e):
    msg = self.getErrorMessage(self, e, tokenNames)
    self.error_reporter.display(msg)
  
def check_ident_dec(self, id, type, line):
    """
    @param id : string
    """
    line_txt = 'line '+str(line)+':'
    try:
      place = self.symb_tab[id]
      self.error_reporter.display(line_txt+" Node double declaration:"+id)
    
    except KeyError:
      if type == 'S':
        node = self.current_macro.add_simple_node(id, 0,0)
      elif type == 'P':
        node = self.current_macro.add_perm_node(id, 0,0)
      elif type == 'I':
        node = self.current_macro.add_input_node(id, 0,0)
      else:
        self.error_reporter.display(line_txt+ " Unknown type - bug?")
      self.symb_tab[id] = node

    
def check_ident_trans(self, id, type, line):
    """
    @param id : string
    """
    line_txt = 'line '+str(line)+':'
    try:
      # already used node
      node = self.symb_tab[id]
      tok = (node.is_input() and type == 'I') or (node.is_perm() and type == 'P') or (type == 'N')
      if (not tok)  :
        self.error_reporter.display(line_txt + " Type error in transition: "+id)
    except KeyError:
      if type == 'N':
        node = self.current_macro.add_simple_node(id, 0,0)
      elif type == 'P':
        node = self.current_macro.add_perm_node(id, 0,0)
      elif type == 'I':
        node = self.current_macro.add_input_node(id, 0,0)
      else:
        self.error_reporter.display(line_txt+ " Unknown type - bug?")
      self.symb_tab[id] = node
    return node
   
def check_ident_start(self, id, line):
    """
    @param id : string
    """
    line_txt = 'line '+str(line)+':'
    try:
      # already used node, must be simple or macro
      node = self.symb_tab[id]
      tnok = node.is_input() or node.is_perm() 
      if tnok:
        self.error_reporter.display(line_txt+ " Type error in start transition: "+id)
    except KeyError:
      node = self.current_macro.add_simple_node(id, 0,0)
      self.symb_tab[id] = node
    return node
    
def check_ident_deg(self, id, line):
    """
    @param id : string
    """
    line_txt = 'line '+str(line)+':'
    try:
      # already used node, must be simple
      node = self.symb_tab[id]
      if not (node.is_simple() or node.is_macro()):
        # degradation allowed from macro nodes - TO MODIFY??
        self.error_reporter.display(line_txt+" Type error in degradation transition: "+id)
    except KeyError:
      node = self.current_macro.add_simple_node(id, 0,0)
      self.symb_tab[id] = node
    return node
    
def build_transition(self, id1, modif, id2, modif2, gc, note, line):
    line_txt = 'line '+str(line)+':'
    if modif:
      type = self.modif_code(modif)
    else:
      type = 'N'
    ori = self.check_ident_trans(id1, type, line)
    if modif2:
      type2 = self.modif_code(modif)
    else:
      type2 = 'N'
    target = self.check_ident_trans(id2, type2, line)
    # check if origin and target are in the same macro
    if not ori.father == target.father:
      self.error_reporter.display(line_txt+" Node:"+id1+ " and node:"+id2 + " are not in the same macro")
    if gc[0]:
      event = gc[0]
    else:
      event = ''
    if gc[1]:
      cond = gc[1]
    else:
      cond = ''
    note_txt = self.clean_note(note)
    t = self.current_macro.add_transition(ori, target)
    if event:
      t.set_event(event)
    t.set_condition(cond)
    if len(note_txt)>0:
      t.note = note_txt
    
def build_start_transition(self, id, note, line):   
    ori = self.current_macro.add_start_node(0,0)
    target = self.check_ident_start(id, line)
    t = self.current_macro.add_transition(ori, target)
    if note:
      note_txt = self.clean_note(note)
      t.set_note(note_txt)
    
def build_deg_transition(self, id, gc, note, line):
    target = self.current_macro.add_trap_node(0,0)
    ori = self.check_ident_deg(id, line)
    event = gc[0]
    cond = gc[1]
    note_txt = self.clean_note(note)
    t = self.current_macro.add_transition(ori, target)
    if event:
      t.set_event(event)
    t.set_condition(cond)
   
def enter_macro(self, id, line):
    line_txt = 'line '+str(line)+':'
    self.macro_pile.append(self.current_macro)
    try:
      node = self.symb_tab[id]
      if not node.is_macro():
        self.error_reporter.display(line_txt+ " Not macro node used as macro:"+id)
        return
      else:
        self.error_reporter.display(line_txt+ " Macro double definition:"+id)
        
    except KeyError:
      node = self.current_macro.add_macro_subnode(id,0,0, 0.25, 0.25)
      self.symb_tab[id] = node
    self.current_macro = node
    
    
def leave_macro(self, id=None):
    self.current_macro = self.macro_pile.pop()
    
def clean_note(self, note):
    return note[1:-1]
    
def modif_code(self, modif):
    if modif == '/p':
      return 'P'
    elif modif == '/i':
      return 'I'

def check_end(self):
    if len(self.macro_pile)>0:
      self.error_reporter.display("Bad macro imbrication - missing \endmacro?")
}


// RULES
// boolean expressions in conditions 
cad_model[model] 
            @init{
              self.model = model
              self.macro_pile = []
              self.symb_tab = dict()} 
           :
                {self.current_macro = self.model.get_root()}
            
            (NAME id=IDENT {self.model.name = $id.text})?
            (macro|transition|dec)+
                {self.check_end()}
            (txt=constraints {self.model.constraints = $txt.text})?
             EOF 
           ;
    
dec        :{type = 'S'}

            id=IDENT (m=modifier {type = self.modif_code($m.text)})? SC
            {self.check_ident_dec(id.text, type, id.line)}
           ;
           
transition :
            id1=IDENT (m=modifier)? TARROW id2=IDENT SC gc=guard (m2=modifier)? ntext=note SC
            {self.build_transition($id1.text, $m.text, $id2.text, $m2.text, $gc.guard_component, $ntext.text, $id1.line)}
            
           | id3=IDENT TARROW  SC gc1=guard ntext1=note SC // degradation transition
            {self.build_deg_transition($id3.text, $gc1.guard_component, $ntext1.text, $id3.line)}
            
           | TARROW id4=IDENT  SC (ntext2=note SC)?   // frontier place with start
            {self.build_start_transition($id4.text, $ntext2.text, $id4.line)}
           ;
    
modifier   : 
            PERM
            
           |INPUT
           ;
    
guard  returns [guard_component]      
           :
            (h=sig_expression)? LB (bt=bool_exp) RB (id2=IDENT)?
            {if h and id2: $guard_component = ($h.text, $bt.text, $id2.text)
            elif h: $guard_component = ($h.text, $bt.text, None)
            elif id2: $guard_component = (None, $bt.text, $id2.text)
            else:  $guard_component = (None, $bt.text, None)}
           ;
           
note       : 
            TEXT 
           |
           ;
            
macro      @init{id2 = None}
           :
            MACRO id1=IDENT 
            {self.enter_macro($id1.text, $id1.line)}
            (macro|transition|dec)*
            ENDMACRO 
            {self.leave_macro()} 
            
           ;
           
sig_expression returns [text]
        : exp1=sig_exp  {$text = $exp1.text}
          (DEFAULT^ exp2=sig_exp
            {$text = $text + ' default '+ $exp2.text}
          )*
        ; 
        
sig_exp  returns [text] 
        :  exp1=sig_exp_primary {$text = $exp1.text}
          (WHEN^ exp2=bool_exp 
            {$text = $text + ' when '+ $exp2.text}
          )*
        ;
        
sig_exp_primary returns [text]
        : id=IDENT
          {$text = $id.text}
        | LP se=sig_expression RP
          {$text = '('+$se.text+')'}
        ;                
                  
bool_exp  returns [text]
           : 
            b1=bool_and {$text = $b1.text}
            (OR b2=bool_and {$text = $text + ' '+'or '+$b2.text})*
           | {$text = ""}
           ;
        
bool_and  returns [text]
           : b1=bool_primary {$text = $b1.text}
            (AND b2=bool_primary {$text = $text + ' '+'and '+$b2.text})*
           ;
        
bool_primary returns [text]
           : NOT b1=bool_primary {$text = 'not '+$b1.text}
            
           | b2=bool_constant {$text = $b2.text}
   
           | id=IDENT  {$text = $id.text}
             
           | LP b3=bool_exp RP {$text = '('+$b3.text+')'}

           ;

bool_constant returns [text]
           : T  {$text = 'true'}
           | F  {$text = 'false'}
           ;
         
constraints returns [text]
           @init {
           SEP = ';'
           }
           : CONST t1=const_exp {$text = $t1.text+SEP}
             (t2=const_exp {$text = $text+'\n'+$t2.text+SEP})* ENDCONST
           ;         

const_exp returns [text]
           : SYNC LP t1=exp_list RP 
            {$text = 'synchro('+$t1.text+')'}
           | EXCL LP t2=exp_list RP 
            {$text = 'exclus('+$t2.text+')'}
           | INC LP t3=sig_expression COM t4=sig_expression RP 
            {$text = 'included('+$t3.text+', '+ $t4.text+')'}
           ;
           
exp_list  returns [text]
           : t1=sig_expression {$text = $t1.text}
           (COM t2=sig_expression { $text = $text +', '+$t2.text})*
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

LP      : '(' ;
RP      : ')' ;
LB      : '[' ;
RB      : ']' ;
SC      : ';' ;
COM     : ',' ;


TARROW  : '-->';
PERM    : '/p' ;
INPUT   : '/i' ;
MACRO   : '/macro' ;
ENDMACRO: '/endmacro' ;
NAME    : '/name' ;
DEFAULT : 'default';
WHEN    : 'when' ;
CONST   : '/constraints' ;
ENDCONST: '/endconstraints' ;
SYNC    : 'synchro' ;
EXCL    : 'exclus'  ;
INC     : 'included' ;

fragment LETTER   : 'a'..'z'|'A'..'Z'|'_';

fragment DIGIT    : '0'..'9';

IDENT   : (LETTER|DIGIT )+ ;

TEXT    : '{'(~'}')*'}';
         
         
