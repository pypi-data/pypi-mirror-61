# Questionnaire DSL

A DSL for describing questionnaires with a simple terminal interpreter.

Example:
```
Q: Project type
1[lang]. Language project
2[gen]. Generator project

Q[package]: Package name
___ /[a-z][a-z0-9_]*$/

Q: Author name
___

Q: Author email
___

Q: This question is to
   test multiline feature and indenting.
   1. Working
   2. Not working.
      This is also to test multiline in choices.
```

Each question begins with `Q:` or `Q[<question ID>]`. The type of the question
is either free-form (specified by `___`) or choice if enumerated options are given.

Both question and option can span multiple lines (like in the last question).

For free-form question an optional regular expression can be given inside `//`
(see `Package name` above). This regex is an input validator.

This package provides an interpreter of the questionnaire
`txquestionnaire.questionnaire_interpreter(model, data=None)` which accepts the
model created by parsing of questionnaire description using this language and
optionally a dictionary of default answers keyed by either question ID if given
or question number. The interpreter will run the questionnaire on the console
and return a dictionary of collected data. The values for options are ordinal
numbers or IDs if given (like in `Project type` above -- `lang`, `gen`).

Please see
[tests](https://github.com/textX/textx-lang-questionnaire/tree/master/tests) for
the detailed usage.
