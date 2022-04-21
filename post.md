In this article we are going to implement a lexer/parser for a programming lanugage xdlang. We will ,define the grammar in EBNF and create a lexer/parser with lark.

Before we proceed, let's define a subset of our language first. Thats it, we are not going to make everything in one pass - that would be too much. For now xdlang will contain four data types:
* character (ascii, no unicde for now!) `char`
* 64-bit integer `int`
* 32-bit `float`
* boolean `bool`

Bunch of operators:
1. Arithmetic (`+`, `-`, `*`, `/`, `%`)
2. Comparision (`==`, `!=`, `<`, `>`, `<=`, `>=`)
3. Unary minus and negation (`-`, `!`)
4. Parenthesis (`(`, `)`)

An operator takes two operand (left-hand side and right-hand side), perform an operation and return the result.

With them we can define expressions like:
* Literals - `3.14`, `42`, `true`, `false`, `'a'`
* Binary expressions - `7 + 15`, `35.53 - 8`, `7 < 3`
* And combine them - `(3 + 4) * 5`, `(3 + 4) * (5 - 2)`
* We can also reference a variable: `3 + x > z`

Expression is basically "something that can be evaluated to a value".

The next construct is statement. Statements is more or less an instruction that can be executed.
1. Variable definition: `let TYPE NAME = EXPRESSION;`, eg: `let int x = 3 + z / 8;`
2. Variable mutation (yes we are going to differentiate them): `mut NAME = EXPRESSION;` eg: `mut x = x + 1;`
3. Empty statement `NOOP;` - it will do nothing - same as `pass` in python or `;` in C.
4. Return statement - `return EXPRESSION;`

A sequence of statements will be called block.

The program is a block with a return statement at the end.

At this moment there are no control flow statements, function definitions, etc but we will add them later. In a moment you will see that there is already quite a lot of things to implement.

Formal notation (EBFN)

Creating parser is so common think that there are standarized notations for parser definiton. We will use EBNF (Extended Backus-Naur Form). It contains two basic constructs:

1. A terminal symbol - piece of text that cannot be further divided. Good examples are keywords: `let`, `mut`, `return`, `if`, `else`, `for`, `while` etc
2. A non-terminal -
3. A production rule - a recipe how terminals can be combined into a legal sequence.

Let's start with the simplest rule - for boolean literals:

```
BOOL_LITERAL: "true" | "false"
```

Terminal names are capitalized. Here we defined a terminal called `BOOL_LITERAL` that can be matched either as `true` or `false`.

Another one for numbers:
```
DIGIT: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
INT: DIGIT+
```

Here we have a `DIGIT` terminal - obviously representing a single ditit. Given it we can easily define a `INT` terminal - wchich is in face a sequence of digits. `DIGIT+` means: "match at least one `DIGIT`".
In lark we have alrady defined such common terminals - we will be using them.

Derivation

Now something more interesing. Let's build a production rule for binary expressions:
```
expr = INT ("+" | "-" | "*" | "/" | "%") INT
```
It says: match and integer followed by one of `+`, `-`, `*`, `/`, `%` followed by an integer. It works but is't veru useful - for examle we cannot parse expression `1 + 2 - 3`. There is a naive fix:

```
expr = INT
    | expr ("+" | "-" | "*" | "/" | "%") expr
```
We read it as follows: Non-terminal `exp` can be `INT` or `exp ("+" | "-" | "*" | "/" | "%") EXPR`. This allows us to parse `1 + 2 * 3`. Let's see how we can perform the derivation:

```
expr +      expr
expr + (expr * expr)
INT  + (INT  * INT)
1    + (2    * 3)
```

But wait, there is another way!

```
 expr +       expr
(expr + expr)  * expr
(INT  + INT)   * INT
(1    + 2)     * 3
```

Those two definetelly are not equivalent. We see that this grammar is ambigous. Of course the programming language must be precise? What we can do? One option is to include additional information about operators priority and associativity. Second one is to rewrite the grammar in a non-ambigous way. We will do the latter.

Fixing the grammar

If you just want to see the solution you can freely skip this section.
