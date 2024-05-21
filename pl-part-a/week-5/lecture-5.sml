(* This week started with sml type inference and how a 
    human would probably do it *)

(* An example would be to;
    - gather all the facts for type checking
    - the facts constrains the type of the function
    - polymorphic types occur when their are less
        facts about a specific bindings or all of the 
        bindings
*)

(* example of type inference *)
(*  
    f : T1 * T2 * T3 -> T4  ;because it is a function
    x : T1
    y : T2
    z : T3

    T4 : T1 * T2 * T3
    T4 : T2 * T1 * T3
    since no other constraints are available, we will
     work with the contraints above to type check the 
     function

    The function would type check if and only if;
        T1 = T2
    
    T4 : T1 * T1 * T3 or 
    T4 : 'a * 'a * 'b

    Hence, the function would be;
    f : 'a * 'a * 'b  ->  'a * 'a * 'b
*)

fun f (x,y,z) =
    if true
    then (x,y,z)
    else (y,x,z)


(* another example *)
(*
    compose : T1 * T2 -> T3
         f  : T2 -> T1
         g  : T4 -> T2
        fn  : T4 -> T3
         x  : T4

    No more constraints, compose function will have the following type

    compose : (T2 -> T1) * (T4 -> T2) -> (T4 -> T2) -> T1

    Replacing T's with sml types;

    compose : ('a -> 'b) * ('c -> 'a) -> 'c  -> 'b

*)
fun compose (f,g) = fn x => f (g x)


(* Another language feature that was not discussed was 
    mutual recursion. 
    This is allowing g to call g and  g to call f. 
    In the usual syntax, this is not possible because 
    sml static environment only contains the bindings
    before it, so functions can only use the bindings 
    defined before the function. However, mutual recursion
    needs to call a function after it.
