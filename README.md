# AI Based Drug Compatibility Alert System

Developed a self-service automated system to alert customers about potential drug interaction between patients history and drug compatibility using first order logic inference. Program takes a query of new drug list and produces a logical conclusion of whether to issue a warning. The complete program was developed in Python.

Input format:
<N = Number of Queries>
<Query 1>
<Query 2>
...
<Query N>
<K = Number of sentences in Knowledge Base>
<KB 1>
<KB 2>
...
<KB K>
  
Query format:Each query will be a single literal of the form Predicate(Constant_Arguments)or ~Predicate(Constant_Arguments)and will not contain any variables.Each predicate will have between 1 and 25constant arguments. Two or more arguments will be separated by commas. 

KB format:Each sentence in the knowledge base is written in one of the following forms:
1)An implication of the form p1∧p2∧... ∧pm⇒q, where its premise is a conjunction of literals and its conclusion is a single literal.Remember that a literal is an atomic sentence or a negated atomic sentence.
2)A single literal: q or ~q
