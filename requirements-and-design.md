# Dum-E v1 Requirements and Design

## Product and scope

Dum-E is a polished, deterministic Python console chatbot. It is deliberately
small: runtime behavior uses only the standard library and prepared responses.
There is no generative AI, fuzzy/NLP matching, network/API access, GUI, saved
history, database, user account, plugin system, or executable packaging.

Its tone is friendly, concise, and lightly playful: funnily dumb but never
annoyingly dumb. Greeting replies address people naturally as `peanut`. Dum-E
is honest that it is a Python rule-based chatbot, and never claims web access,
learning, private-data access, or memory it does not have.

## Configured identity

The sole configured personal fact is the exact phrase **My Sir, Arkadeep
Sengupta.** Creator/owner/Sir questions and all supported questions about
Arkadeep or the user include that exact identification. About-user answers say
that it is the only personal detail configured; Dum-E invents no biography and
does not persist conversation data.

## Matching design

`normalize_message(raw: str) -> str` is pure. It rejects non-strings with
`TypeError`, applies Unicode NFKC normalization and `casefold()`, changes curly
left and right apostrophes to straight ones, preserves only internal
apostrophes, turns other punctuation (including hyphens) into separators, and
collapses whitespace.

`get_response(raw_message: str) -> str` is also pure. Its visible `if` / `elif`
/ `else` rule chain compares whole normalized phrases with immutable
`frozenset` alias collections. One deliberately narrow exception is the about-Sir helper: it recognizes
whole-token `arkadeep` (including the exact possessive `arkadeep's`). Explicit
aliases handle configured Sir/creator/master questions and self-identity queries
so ordinary phrases such as `my master plan` do not accidentally become Sir
requests. It never uses a broad name substring or fuzzy matching, so
`arkadeepish`, `history`, and `I don't want to quit` do not trigger unintended
behavior.

The fixed priority is: empty input; exit; exact greeting; exact about-Sir
identity; exact Sir identity; whole-token/phrase about-Sir detection; help;
Dum-E identity; small talk; thanks; Python FAQ; programming FAQ; joke;
fallback. Exact greetings come before the broader about-Sir detector so they
always retain the warm `peanut` response.

## Supported intents

| Intent | Exact normalized phrases |
| --- | --- |
| Greeting | `hi`, `hello`, `hey`; each with `there`, `dum e`, `peanut`, `arkadeep`, or `arkadeep sengupta`; `good day`, `good morning`, `good afternoon`, `good evening`; and those four good-time greetings with `peanut`, `arkadeep`, or `arkadeep sengupta` |
| Help | `help`, `commands`, `what can you do`, `what do you do`, `how can you help`, `how do i use you` |
| Dum-E identity | `who are you`, `what is your name`, `what's your name`, `whats your name`, `are you ai`, `are you an ai` |
| Sir/user identity | creator/owner/Sir/master aliases, exact Arkadeep and about-user aliases, plus the documented whole-token/phrase helper for unconfigured Arkadeep/Sir details |
| Small talk and thanks | `how are you`, `how are you doing`, `thanks`, `thank you`, `thank you dum e` |
| Python FAQ | `what is python`, `what's python`, `whats python`, `define python` |
| Programming FAQ | `what is programming`, `define programming` |
| Joke | `joke`, `tell me a joke`, `make me laugh` |
| Exit | `q`, `quit`, `exit`, `bye`, `goodbye` |

The Sir/user alias collection explicitly includes: `who made you`, `who created
you`, `who is your creator`, `who is your sir`, `who's your sir`, `who is my sir`,
`who's my sir`, `who is your master`, `who's your master`, `who is my master`,
`who's my master`, `who do you serve`, `who is your owner`, `who is your boss`,
`who built you`, `who programmed you`, `who is dum e's sir`, `who's dum e's sir`,
`who is dum e's creator`, `who's dum e's creator`, `who created dum e`,
`tell me about dum e's sir`, `tell me about your sir`, `tell me about your master`,
all listed `who/tell/describe/about Arkadeep` forms, `what do you know about me`,
`tell me about me`, `who am i`, and all three `my name` forms. Every answer
about Arkadeep/Sir starts with `My Sir, Arkadeep Sengupta.`. A question asking
for an unconfigured detail receives a brief no-configured-or-verified-information
limitation rather than invented biographical facts.

Unsupported input receives a concise fallback that suggests `help`. Blank,
punctuation-only, and emoji-only input receive an empty-input prompt and do not
exit.

## Console loop and shutdown

`main(input_fn=None, output_fn=None) -> int` resolves standard `input` and
`print` at runtime, displays one welcome banner, and repeatedly prompts with
`You: `. Responses are emitted as `Dum-E: <response>` without re-echoing raw
user messages.

Only a whole normalized exit alias stops the loop, after exactly one farewell,
with status `0`. `EOFError` emits one labelled farewell and returns `0`.
`KeyboardInterrupt` emits one labelled farewell and returns `130`; neither path
prints a traceback. Importing the module has no console side effect. The main
guard raises `SystemExit(main())` only when the file is run directly.

## Test plan and acceptance criteria

`pytest` tests every declared alias in each intent group, required `peanut`
greeting punctuation/case variants, both curly apostrophes, the normalizer
contract (including NFKC, whitespace, emoji, and invalid types), about-Arkadeep
detail limitations, whole-token false positives, deterministic responses, and
the injected-input console loop. Loop tests cover repeated messages, every exit
alias, blank and unknown input, EOF, Ctrl+C, exact exit matching, output labels,
and import safety.

Acceptance requires passing compilation and test checks, an accurate README,
an ignored local virtual environment/cache, and a manual session covering a
greeting, help, bot identity, Sir identity, FAQ, joke, fallback, another
message, and clean exit.
