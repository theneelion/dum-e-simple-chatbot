"""Dum-E, a small deterministic command-line chatbot."""

from collections.abc import Callable
import unicodedata


BOT_NAME = "Dum-E"

EXIT_ALIASES: frozenset[str] = frozenset({"q", "quit", "exit", "bye", "goodbye"})

SIR_IDENTITY_ALIASES: frozenset[str] = frozenset(
    {
        "who made you",
        "who created you",
        "who is your creator",
        "who is your sir",
        "who's your sir",
        "who is my sir",
        "who's my sir",
        "who is your master",
        "who's your master",
        "who is my master",
        "who's my master",
        "who do you serve",
        "who is your owner",
        "who is your boss",
        "who built you",
        "who programmed you",
        "who is dum e's sir",
        "who's dum e's sir",
        "who is dum e's creator",
        "who's dum e's creator",
        "who created dum e",
        "tell me about dum e's sir",
        "who is arkadeep",
        "who is arkadeep sengupta",
        "tell me about arkadeep",
        "tell me about arkadeep sengupta",
        "describe arkadeep",
        "describe arkadeep sengupta",
        "what do you know about arkadeep",
        "what do you know about arkadeep sengupta",
        "what do you know about me",
        "tell me about me",
        "who am i",
        "what is my name",
        "what's my name",
        "whats my name",
        "do you know arkadeep",
        "do you know arkadeep sengupta",
        "about arkadeep",
        "about arkadeep sengupta",
        "tell me about your sir",
        "tell me about your master",
    }
)

ABOUT_SIR_ALIASES: frozenset[str] = frozenset(
    {
        "tell me about arkadeep",
        "tell me about arkadeep sengupta",
        "describe arkadeep sengupta",
        "what do you know about arkadeep",
        "what do you know about arkadeep sengupta",
        "what do you know about me",
        "tell me about me",
        "who am i",
        "what is my name",
        "what's my name",
        "whats my name",
        "do you know arkadeep",
        "do you know arkadeep sengupta",
        "about arkadeep",
        "about arkadeep sengupta",
        "tell me about your sir",
        "tell me about your master",
    }
)

SELF_IDENTITY_ALIASES: frozenset[str] = frozenset(
    {
        "what do you know about me",
        "tell me about me",
        "who am i",
        "what is my name",
        "what's my name",
        "whats my name",
    }
)

HELP_ALIASES: frozenset[str] = frozenset(
    {
        "help",
        "commands",
        "what can you do",
        "what do you do",
        "how can you help",
        "how do i use you",
    }
)

BOT_IDENTITY_ALIASES: frozenset[str] = frozenset(
    {
        "who are you",
        "what is your name",
        "what's your name",
        "whats your name",
        "are you ai",
        "are you an ai",
    }
)

GREETING_ALIASES: frozenset[str] = frozenset(
    {
        "hi",
        "hello",
        "hey",
        "hi there",
        "hello there",
        "hey there",
        "hi dum e",
        "hello dum e",
        "hey dum e",
        "hi peanut",
        "hello peanut",
        "hey peanut",
        "hi arkadeep",
        "hello arkadeep",
        "hey arkadeep",
        "hi arkadeep sengupta",
        "hello arkadeep sengupta",
        "hey arkadeep sengupta",
        "good day",
        "good day peanut",
        "good day arkadeep",
        "good day arkadeep sengupta",
        "good morning",
        "good morning peanut",
        "good morning arkadeep",
        "good morning arkadeep sengupta",
        "good afternoon",
        "good afternoon peanut",
        "good afternoon arkadeep",
        "good afternoon arkadeep sengupta",
        "good evening",
        "good evening peanut",
        "good evening arkadeep",
        "good evening arkadeep sengupta",
    }
)

SMALL_TALK_ALIASES: frozenset[str] = frozenset({"how are you", "how are you doing"})
THANKS_ALIASES: frozenset[str] = frozenset(
    {
        "thanks",
        "thank you",
        "thank you dum e",
        "thanks dum e",
        "thanks arkadeep",
        "thank you arkadeep",
        "thanks arkadeep sengupta",
        "thank you arkadeep sengupta",
    }
)
PYTHON_FAQ_ALIASES: frozenset[str] = frozenset(
    {"what is python", "what's python", "whats python", "define python"}
)
PROGRAMMING_FAQ_ALIASES: frozenset[str] = frozenset(
    {"what is programming", "define programming"}
)
JOKE_ALIASES: frozenset[str] = frozenset(
    {"joke", "tell me a joke", "make me laugh"}
)

EMPTY_RESPONSE = "I did not catch that, peanut. Try a greeting or type 'help'."
EXIT_RESPONSE = "Goodbye, peanut. Try not to miss me too much."
SIR_RESPONSE = "My Sir, Arkadeep Sengupta."
ABOUT_SIR_RESPONSE = (
    "My Sir, Arkadeep Sengupta. That is the only personal detail configured "
    "into me; I do not keep a dossier, peanut."
)
SIR_DETAIL_LIMITATION_RESPONSE = (
    "My Sir, Arkadeep Sengupta. I have no configured or verified information "
    "about that extra detail."
)
HELP_RESPONSE = (
    "I can greet you, explain my rule-based setup, answer a few Python and "
    "programming questions, handle small talk and thanks, tell one joke, and "
    "identify my Sir. Try 'what is Python?', 'tell me a joke', or 'who made you'. "
    "Exit with q, quit, exit, bye, or goodbye."
)
BOT_IDENTITY_RESPONSE = (
    "I am Dum-E, a small Python rule-based chatbot. "
    "I use prepared if/elif rules, not a generative AI model."
)
GREETING_RESPONSE = "Hi, peanut! Nice to see you. Type 'help' if you need ideas."
SMALL_TALK_RESPONSE = "I am running smoothly. Emotionally? The loading bar is inconclusive."
THANKS_RESPONSE = "You are welcome! Happy to help."
PYTHON_FAQ_RESPONSE = (
    "Python is a general-purpose programming language commonly used for "
    "automation, web development, data work, and much more."
)
PROGRAMMING_FAQ_RESPONSE = "Programming is writing instructions that a computer can execute."
JOKE_RESPONSE = "Why do programmers prefer dark mode? Because light attracts bugs."
FALLBACK_RESPONSE = (
    "I do not know that one yet. My brain cell is doing its best--try 'help' "
    "for things I can answer."
)

WELCOME_BANNER = (
    "========================================\n"
    " Dum-E - Simple Rule-Based Chatbot\n"
    " Type 'help' for ideas or 'quit' to exit.\n"
    "========================================"
)
EOF_FAREWELL = "Goodbye, peanut. I ran out of input, so I will power down."
INTERRUPT_FAREWELL = "Goodbye, peanut. I will stop there."


def normalize_message(raw: str) -> str:
    """Return a normalized, exact-match-friendly representation of *raw*.

    The function intentionally has no I/O or state. Apostrophes remain only when
    they occur inside an alphanumeric word or phrase, so contractions such as
    ``what's`` match while surrounding quote marks become separators.
    """

    if not isinstance(raw, str):
        raise TypeError("raw must be a string")

    normalized = (
        unicodedata.normalize("NFKC", raw)
        .casefold()
        .replace("\u2018", "'")
        .replace("\u2019", "'")
    )
    characters: list[str] = []

    for index, character in enumerate(normalized):
        if character.isalnum():
            characters.append(character)
        elif character == "'" and _is_internal_apostrophe(normalized, index):
            characters.append(character)
        else:
            characters.append(" ")

    return " ".join("".join(characters).split())


def _is_internal_apostrophe(text: str, index: int) -> bool:
    """Return whether the apostrophe at *index* belongs inside a word."""

    return (
        index > 0
        and index < len(text) - 1
        and text[index - 1].isalnum()
        and text[index + 1].isalnum()
    )


def is_about_sir_message(message: str) -> bool:
    """Recognize question-like messages about Arkadeep beyond exact aliases.

    A mere mention of Arkadeep is not an identity question. Exact configured
    aliases are handled separately by ``get_response``; this fallback only
    covers question-shaped prompts that begin with a supported interrogative
    or a direct request for information.
    """

    tokens = tuple(message.split())
    if not any(token in {"arkadeep", "arkadeep's"} for token in tokens):
        return False

    question_starters = {
        "who", "what", "when", "where", "why", "how",
        "is", "are", "was", "were", "do", "does", "did",
        "can", "could", "would", "should",
    }
    if tokens and tokens[0] in question_starters:
        return True

    return (
        len(tokens) >= 3
        and tokens[:3] == ("tell", "me", "about")
    ) or (
        len(tokens) >= 2
        and tokens[0] in {"describe", "explain"}
    )


def get_response(raw_message: str) -> str:
    """Return Dum-E's one deterministic response for a raw user message."""

    message = normalize_message(raw_message)

    # Priority is deliberate: blank input, exits, whole-message greetings, and
    # whole-message thanks win before explicit and broad Sir detection; existing
    # exact intents then retain their stable order before the generic fallback.
    if not message:
        return EMPTY_RESPONSE
    elif message in EXIT_ALIASES:
        return EXIT_RESPONSE
    elif message in GREETING_ALIASES:
        return GREETING_RESPONSE
    elif message in THANKS_ALIASES:
        return THANKS_RESPONSE
    elif message in ABOUT_SIR_ALIASES:
        return ABOUT_SIR_RESPONSE
    elif message in SIR_IDENTITY_ALIASES:
        return SIR_RESPONSE
    elif is_about_sir_message(message):
        return SIR_DETAIL_LIMITATION_RESPONSE
    elif message in HELP_ALIASES:
        return HELP_RESPONSE
    elif message in BOT_IDENTITY_ALIASES:
        return BOT_IDENTITY_RESPONSE
    elif message in SMALL_TALK_ALIASES:
        return SMALL_TALK_RESPONSE
    elif message in PYTHON_FAQ_ALIASES:
        return PYTHON_FAQ_RESPONSE
    elif message in PROGRAMMING_FAQ_ALIASES:
        return PROGRAMMING_FAQ_RESPONSE
    elif message in JOKE_ALIASES:
        return JOKE_RESPONSE
    else:
        return FALLBACK_RESPONSE


def main(
    input_fn: Callable[[str], str] | None = None,
    output_fn: Callable[[str], None] | None = None,
) -> int:
    """Run one repeat conversation and return its process-style exit status."""

    if input_fn is None:
        input_fn = input
    if output_fn is None:
        output_fn = print

    try:
        output_fn(WELCOME_BANNER)

        while True:
            raw_message = input_fn("You: ")

            response = get_response(raw_message)
            output_fn(f"{BOT_NAME}: {response}")

            if normalize_message(raw_message) in EXIT_ALIASES:
                return 0
    except EOFError:
        output_fn(f"{BOT_NAME}: {EOF_FAREWELL}")
        return 0
    except KeyboardInterrupt:
        return _handle_interrupt(output_fn)


def _handle_interrupt(output_fn: Callable[[str], None]) -> int:
    """Best-effort cancellation output without masking the shutdown result."""

    try:
        output_fn(f"{BOT_NAME}: {INTERRUPT_FAREWELL}")
    except KeyboardInterrupt:
        pass
    return 130


if __name__ == "__main__":
    raise SystemExit(main())
