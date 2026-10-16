# Dum-E Simple Chatbot

Dum-E is a small, local command-line chatbot written in Python. It is a
deterministic rule-based program, not a generative-AI assistant: it recognizes
an explicit set of normalized phrases and returns prepared responses. A narrow,
whole-token rule also recognizes messages about Arkadeep or Dum-E's Sir so it
can state its configured identity honestly.

Dum-E is meant to be funnily dumb without being annoyingly dumb--friendly,
concise, and lightly playful. In greetings it calls people `peanut`; when asked
about its Sir, it identifies **My Sir, Arkadeep Sengupta** and does not invent
other personal details.

## Features

- Exact, case-insensitive phrase matching after Unicode, punctuation, and
  whitespace normalization.
- Friendly greetings, `help`, Dum-E identity, small talk, thanks, basic Python
  and programming FAQs, and one harmless joke.
- Configured Sir/user identity responses, including `who made you` and
  `what do you know about me`. Questions about Arkadeep or Dum-E's Sir begin
  with **My Sir, Arkadeep Sengupta.**; unconfigured personal details are not
  invented.
- Exact exit commands: `q`, `quit`, `exit`, `bye`, and `goodbye`.
- Clean handling of blank input, end-of-input, and Ctrl+C.
- No network access, APIs, saved history, database, GUI, or runtime
  third-party dependency.

Try prompts such as `hello`, `what can you do`, `what is Python`, `who made
you`, `who is Arkadeep's colleague`, `tell me a joke`, or `help`.

## Run Dum-E

The chatbot itself uses only the Python standard library. From this project
folder, run:

```powershell
python chatbot.py
```

On Windows systems that provide the Python launcher, `py -3 chatbot.py` is an
equivalent command.

## Development setup and tests

`pytest` is needed only for development and testing.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m py_compile chatbot.py test_chatbot.py
python -m pytest -v
```

If your system does not provide the `py` launcher, replace the first command
with the path to a Python 3.10+ interpreter followed by `-m venv .venv`.

## Example conversation

```text
========================================
 Dum-E - Simple Rule-Based Chatbot
 Type 'help' for ideas or 'quit' to exit.
========================================
You: HELLO!!!
Dum-E: Hi, peanut! Nice to see you. Type 'help' if you need ideas.
You: Who is Arkadeep's colleague?
Dum-E: My Sir, Arkadeep Sengupta. I have no configured or verified information about that extra detail.
You: what is Python
Dum-E: Python is a general-purpose programming language commonly used for automation, web development, data work, and much more.
You: tell me a joke
Dum-E: Why do programmers prefer dark mode? Because light attracts bugs.
You: blorbo
Dum-E: I do not know that one yet. My brain cell is doing its best--try 'help' for things I can answer.
You: quit
Dum-E: Goodbye, peanut. Try not to miss me too much.
```

## Limitations

Dum-E has fixed responses and supports explicit normalized phrases, plus a
small whole-token rule for Arkadeep/Sir references. It does not understand
arbitrary language, use generative AI, access the network, or retain persistent
memory between (or during) sessions.

See [the requirements and design document](Chatbot/requirements-and-design.md)
for the complete v1 behavior contract.
