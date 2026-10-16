"""Observable behavior tests for Dum-E."""

from collections.abc import Callable
import subprocess
import sys
from pathlib import Path

import pytest

import chatbot


GREETING_ALIASES = (
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
)
HELP_ALIASES = (
    "help",
    "commands",
    "what can you do",
    "what do you do",
    "how can you help",
    "how do i use you",
)
BOT_IDENTITY_ALIASES = (
    "who are you",
    "what is your name",
    "what's your name",
    "whats your name",
    "are you ai",
    "are you an ai",
)
SIR_IDENTITY_ALIASES = (
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
)
SMALL_TALK_ALIASES = ("how are you", "how are you doing")
THANKS_ALIASES = (
    "thanks",
    "thank you",
    "thank you dum e",
    "thanks dum e",
    "thanks arkadeep",
    "thank you arkadeep",
    "thanks arkadeep sengupta",
    "thank you arkadeep sengupta",
)
PYTHON_FAQ_ALIASES = (
    "what is python",
    "what's python",
    "whats python",
    "define python",
)
PROGRAMMING_FAQ_ALIASES = ("what is programming", "define programming")
JOKE_ALIASES = ("joke", "tell me a joke", "make me laugh")
EXIT_ALIASES = ("q", "quit", "exit", "bye", "goodbye")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("HELLO", "hello"),
        ("Hello", "hello"),
        ("hello!!!", "hello"),
        ("  Hi   there ", "hi there"),
        ("WHAT'S YOUR NAME?", "what's your name"),
        ("WHAT\u2019S YOUR NAME?", "what's your name"),
        ("WHAT\u2018S YOUR NAME?", "what's your name"),
        ("good-morning", "good morning"),
        ("q!!!", "q"),
        ("\uff28\uff25\uff2c\uff2c\uff2f", "hello"),
        ("\t hello\nthere \t", "hello there"),
        ("'hello'", "hello"),
        ("don't", "don't"),
        ("   ", ""),
        ("!!!", ""),
        ("\U0001f642\U0001f680", ""),
    ],
)
def test_normalize_message(raw: str, expected: str) -> None:
    assert chatbot.normalize_message(raw) == expected


@pytest.mark.parametrize("raw", [None, 3, object()])
def test_normalize_message_rejects_non_strings(raw: object) -> None:
    with pytest.raises(TypeError):
        chatbot.normalize_message(raw)  # type: ignore[arg-type]


@pytest.mark.parametrize("alias", GREETING_ALIASES)
def test_every_greeting_alias_is_supported_and_addresses_peanut(alias: str) -> None:
    response = chatbot.get_response(alias)
    assert response == chatbot.GREETING_RESPONSE
    assert "peanut" in response.casefold()


def test_greeting_punctuation_and_hyphen_variants_are_normalized() -> None:
    assert chatbot.get_response("HELLO!!!") == chatbot.GREETING_RESPONSE
    assert chatbot.get_response("hi dum-e") == chatbot.GREETING_RESPONSE


@pytest.mark.parametrize(
    "raw",
    (
        "Hey Arkadeep",
        "Good day, Arkadeep",
        "HEY, ARKADEEP!!!",
        "  good   day, Arkadeep Sengupta  ",
    ),
)
def test_whole_message_arkadeep_greetings_win_over_sir_detection(raw: str) -> None:
    response = chatbot.get_response(raw)
    assert response == chatbot.GREETING_RESPONSE
    assert "peanut" in response.casefold()


@pytest.mark.parametrize(
    "raw",
    (
        "Good day, peanut",
        "Good morning, peanut",
        "Good afternoon, peanut",
        "Good evening, peanut",
        "Hi, peanut",
        "Hello, peanut",
        "Hey, peanut",
        "GOOD DAY, PEANUT!!!",
        " hi,   peanut ",
    ),
)
def test_required_peanut_greeting_variants_are_warm_and_deterministic(raw: str) -> None:
    response = chatbot.get_response(raw)
    assert response == chatbot.GREETING_RESPONSE
    assert "peanut" in response.casefold()


@pytest.mark.parametrize("alias", HELP_ALIASES)
def test_every_help_alias_is_supported(alias: str) -> None:
    assert chatbot.get_response(alias) == chatbot.HELP_RESPONSE


@pytest.mark.parametrize("alias", BOT_IDENTITY_ALIASES)
def test_every_bot_identity_alias_is_supported(alias: str) -> None:
    response = chatbot.get_response(alias)
    assert response == chatbot.BOT_IDENTITY_RESPONSE
    assert "Dum-E" in response
    assert "generative AI" in response


@pytest.mark.parametrize(
    "raw",
    ("WHAT'S YOUR NAME", "WHAT\u2019S YOUR NAME", "WHAT\u2018S YOUR NAME"),
)
def test_all_supported_apostrophe_forms_resolve_to_bot_identity(raw: str) -> None:
    assert chatbot.get_response(raw) == chatbot.BOT_IDENTITY_RESPONSE


@pytest.mark.parametrize("raw", ("WHO\u2019S YOUR SIR?", "WHO\u2018S YOUR SIR?"))
def test_curly_apostrophe_sir_aliases_resolve_to_the_configured_identity(raw: str) -> None:
    assert chatbot.get_response(raw) == chatbot.SIR_RESPONSE


@pytest.mark.parametrize(
    "raw",
    (
        "Who is Dum-E's Sir?",
        "Who's Dum-E's Sir?",
        "Tell me about Dum-E's Sir",
        "Who is Dum-E's creator?",
        "Who's Dum-E's creator?",
        "Who created Dum-E?",
        "Who is Dum-E\u2018s Sir?",
        "Who is Dum-E\u2019s creator?",
    ),
)
def test_hyphenated_dum_e_sir_and_creator_references_are_supported(raw: str) -> None:
    assert chatbot.get_response(raw) == chatbot.SIR_RESPONSE
    assert chatbot.get_response(raw) == "My Sir, Arkadeep Sengupta."


@pytest.mark.parametrize(
    ("sir_query", "creator_query"),
    [
        ("Who is Dum-E's Sir?", "Who is Dum-E's creator?"),
        ("who is dum-e's sir", "who is dum-e's creator"),
        ("WHO IS DUM-E'S SIR???", "WHO IS DUM-E'S CREATOR???"),
        ("Who's Dum-E's Sir?", "Who's Dum-E's creator?"),
        ("Who is Dum-E\u2019s Sir?", "Who is Dum-E\u2019s creator?"),
        ("Who is Dum-E\u2018s Sir?", "Who is Dum-E\u2018s creator?"),
        ("Who\u2019s Dum-E\u2019s Sir?", "Who\u2019s Dum-E\u2019s creator?"),
        ("Who\u2018s Dum-E\u2018s Sir?", "Who\u2018s Dum-E\u2018s creator?"),
    ],
)
def test_sir_and_creator_questions_are_strictly_equal(
    sir_query: str, creator_query: str
) -> None:
    sir_response = chatbot.get_response(sir_query)
    creator_response = chatbot.get_response(creator_query)
    assert sir_response == creator_response
    assert sir_response == chatbot.SIR_RESPONSE
    assert sir_response == "My Sir, Arkadeep Sengupta."


@pytest.mark.parametrize("alias", SIR_IDENTITY_ALIASES)
def test_every_sir_identity_alias_uses_the_exact_configured_identity(alias: str) -> None:
    response = chatbot.get_response(alias)
    assert response.startswith("My Sir, Arkadeep Sengupta.")


def test_about_me_response_limits_knowledge_to_the_configured_identity() -> None:
    response = chatbot.get_response("what do you know about me")
    assert response == chatbot.ABOUT_SIR_RESPONSE
    assert response.startswith("My Sir, Arkadeep Sengupta.")
    assert "only personal detail configured" in response
    assert "remember" not in response.casefold()


@pytest.mark.parametrize(
    "message",
    (
        "Who is Arkadeep?",
        "Describe Arkadeep",
        "Tell me about Arkadeep Sengupta",
        "Who is Arkadeep's colleague?",
    ),
)
def test_about_arkadeep_questions_start_with_the_configured_identity(message: str) -> None:
    response = chatbot.get_response(message)
    assert response.startswith("My Sir, Arkadeep Sengupta.")


def test_unknown_arkadeep_detail_is_honest_about_the_limitation() -> None:
    response = chatbot.get_response("Who is Arkadeep's colleague?")
    assert response == chatbot.SIR_DETAIL_LIMITATION_RESPONSE
    assert "no configured or verified information" in response


@pytest.mark.parametrize(
    "message",
    ("Who is Arkadeep\u2019s colleague?", "Who is Arkadeep\u2018s colleague?"),
)
def test_curly_possessive_arkadeep_detail_questions_are_limited_honestly(message: str) -> None:
    assert chatbot.get_response(message) == chatbot.SIR_DETAIL_LIMITATION_RESPONSE


@pytest.mark.parametrize("message", ("arkadeepish", "who is arkadeepish", "my masterplan"))
def test_name_or_sir_substrings_do_not_trigger_identity_detection(message: str) -> None:
    assert chatbot.get_response(message) == chatbot.FALLBACK_RESPONSE


@pytest.mark.parametrize(
    "message",
    (
        "What is your master plan?",
        "My master plan needs work",
        "master plan",
        "master's degree",
        "master copy",
    ),
)
def test_ordinary_master_phrases_do_not_trigger_sir_detection(message: str) -> None:
    assert chatbot.get_response(message) == chatbot.FALLBACK_RESPONSE


def test_exact_greeting_has_priority_over_the_broader_sir_detector(monkeypatch) -> None:
    monkeypatch.setattr(chatbot, "is_about_sir_message", lambda message: True)
    assert chatbot.get_response("hello") == chatbot.GREETING_RESPONSE


@pytest.mark.parametrize("alias", SMALL_TALK_ALIASES)
def test_every_small_talk_alias_is_supported(alias: str) -> None:
    assert chatbot.get_response(alias) == chatbot.SMALL_TALK_RESPONSE


@pytest.mark.parametrize("alias", THANKS_ALIASES)
def test_every_thanks_alias_is_supported(alias: str) -> None:
    assert chatbot.get_response(alias) == chatbot.THANKS_RESPONSE


@pytest.mark.parametrize(
    "message",
    (
        "Thanks, Arkadeep!",
        "Thank you, Arkadeep!",
        "THANKS, ARKADEEP SENGUPTA!!!",
        "  thank   you, Arkadeep Sengupta  ",
    ),
)
def test_thanks_addressed_to_arkadeep_are_not_hijacked_by_sir_detection(message: str) -> None:
    response = chatbot.get_response(message)
    assert response == chatbot.THANKS_RESPONSE
    assert response == "You are welcome! Happy to help."


@pytest.mark.parametrize("alias", PYTHON_FAQ_ALIASES)
def test_every_python_faq_alias_is_supported(alias: str) -> None:
    assert chatbot.get_response(alias) == chatbot.PYTHON_FAQ_RESPONSE


@pytest.mark.parametrize("alias", PROGRAMMING_FAQ_ALIASES)
def test_every_programming_faq_alias_is_supported(alias: str) -> None:
    assert chatbot.get_response(alias) == chatbot.PROGRAMMING_FAQ_RESPONSE


@pytest.mark.parametrize("alias", JOKE_ALIASES)
def test_every_joke_alias_is_supported(alias: str) -> None:
    assert chatbot.get_response(alias) == chatbot.JOKE_RESPONSE


@pytest.mark.parametrize("alias", EXIT_ALIASES)
def test_every_exit_alias_returns_the_farewell(alias: str) -> None:
    assert chatbot.get_response(alias) == chatbot.EXIT_RESPONSE


def test_empty_and_unsupported_messages_have_useful_distinct_responses() -> None:
    assert chatbot.get_response("\U0001f642") == chatbot.EMPTY_RESPONSE
    assert chatbot.get_response("blorbo") == chatbot.FALLBACK_RESPONSE


def test_required_response_content_is_truthful_and_actionable() -> None:
    help_response = chatbot.get_response("help")
    assert "Python" in help_response
    assert "joke" in help_response
    assert "q, quit, exit, bye, or goodbye" in help_response

    assert "general-purpose programming language" in chatbot.get_response("what is python")
    assert "instructions that a computer can execute" in chatbot.get_response(
        "what is programming"
    )
    assert chatbot.get_response("tell me a joke") == (
        "Why do programmers prefer dark mode? Because light attracts bugs."
    )
    assert "help" in chatbot.get_response("unlisted request").casefold()
    assert "generative AI model" in chatbot.get_response("who are you")


def test_all_alias_collections_are_immutable() -> None:
    alias_groups = (
        chatbot.EXIT_ALIASES,
        chatbot.SIR_IDENTITY_ALIASES,
        chatbot.ABOUT_SIR_ALIASES,
        chatbot.SELF_IDENTITY_ALIASES,
        chatbot.HELP_ALIASES,
        chatbot.BOT_IDENTITY_ALIASES,
        chatbot.GREETING_ALIASES,
        chatbot.SMALL_TALK_ALIASES,
        chatbot.THANKS_ALIASES,
        chatbot.PYTHON_FAQ_ALIASES,
        chatbot.PROGRAMMING_FAQ_ALIASES,
        chatbot.JOKE_ALIASES,
    )
    assert all(isinstance(group, frozenset) for group in alias_groups)
    assert chatbot.ABOUT_SIR_ALIASES <= chatbot.SIR_IDENTITY_ALIASES


@pytest.mark.parametrize(
    "message",
    (
        "this is useful",
        "history",
        "I don't want to quit",
        "quitting",
        "goodbye to everyone",
        "hi what is python",
    ),
)
def test_partial_or_compound_messages_do_not_match_supported_phrases(message: str) -> None:
    assert chatbot.get_response(message) == chatbot.FALLBACK_RESPONSE


def test_standalone_punctuated_exit_is_recognized_after_normalization() -> None:
    assert chatbot.get_response("QUIT!!!") == chatbot.EXIT_RESPONSE


def test_same_normalized_message_always_has_the_same_response() -> None:
    assert chatbot.get_response("  HELLO!!! ") == chatbot.get_response("hello")


def _scripted_input(
    events: list[str | BaseException], prompts: list[str]
) -> Callable[[str], str]:
    iterator = iter(events)

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        event = next(iterator)
        if isinstance(event, BaseException):
            raise event
        return event

    return fake_input


def test_main_runs_multiple_messages_then_exits() -> None:
    outputs: list[str] = []
    prompts: list[str] = []
    status = chatbot.main(
        _scripted_input(["hello", "what is python", "quit"], prompts), outputs.append
    )

    assert status == 0
    assert outputs.count(chatbot.WELCOME_BANNER) == 1
    assert outputs[1] == f"Dum-E: {chatbot.GREETING_RESPONSE}"
    assert outputs[2] == f"Dum-E: {chatbot.PYTHON_FAQ_RESPONSE}"
    assert outputs[3] == f"Dum-E: {chatbot.EXIT_RESPONSE}"
    assert prompts == ["You: ", "You: ", "You: "]


@pytest.mark.parametrize("alias", EXIT_ALIASES)
def test_main_ends_for_each_exact_exit_alias(alias: str) -> None:
    outputs: list[str] = []
    prompts: list[str] = []
    status = chatbot.main(_scripted_input([alias], prompts), outputs.append)

    assert status == 0
    assert outputs.count(f"Dum-E: {chatbot.EXIT_RESPONSE}") == 1
    assert prompts == ["You: "]


def test_main_normalizes_exit_before_terminating() -> None:
    outputs: list[str] = []
    status = chatbot.main(_scripted_input(["QUIT!!!"], []), outputs.append)

    assert status == 0
    assert outputs[-1] == f"Dum-E: {chatbot.EXIT_RESPONSE}"


def test_main_blank_and_unknown_messages_continue_without_echoing_raw_input() -> None:
    outputs: list[str] = []
    prompts: list[str] = []
    unknown = "blorbo private-looking text"
    status = chatbot.main(
        _scripted_input(["   ", unknown, "hello", "exit"], prompts), outputs.append
    )

    assert status == 0
    assert f"Dum-E: {chatbot.EMPTY_RESPONSE}" in outputs
    assert f"Dum-E: {chatbot.FALLBACK_RESPONSE}" in outputs
    assert f"Dum-E: {chatbot.GREETING_RESPONSE}" in outputs
    assert unknown not in "\n".join(outputs)
    assert len(prompts) == 4


def test_main_does_not_exit_for_an_exit_word_inside_a_longer_message() -> None:
    outputs: list[str] = []
    prompts: list[str] = []
    status = chatbot.main(
        _scripted_input(["I don't want to quit", "quit"], prompts), outputs.append
    )

    assert status == 0
    assert outputs[1] == f"Dum-E: {chatbot.FALLBACK_RESPONSE}"
    assert outputs.count(f"Dum-E: {chatbot.EXIT_RESPONSE}") == 1
    assert len(prompts) == 2


def test_main_handles_eof_cleanly() -> None:
    outputs: list[str] = []
    status = chatbot.main(_scripted_input([EOFError()], []), outputs.append)

    assert status == 0
    assert outputs == [chatbot.WELCOME_BANNER, f"Dum-E: {chatbot.EOF_FAREWELL}"]


def test_main_handles_ctrl_c_cleanly() -> None:
    outputs: list[str] = []
    status = chatbot.main(_scripted_input([KeyboardInterrupt()], []), outputs.append)

    assert status == 130
    assert outputs == [chatbot.WELCOME_BANNER, f"Dum-E: {chatbot.INTERRUPT_FAREWELL}"]


def test_main_handles_ctrl_c_during_response_processing(monkeypatch) -> None:
    outputs: list[str] = []

    def interrupting_response(_: str) -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr(chatbot, "get_response", interrupting_response)
    status = chatbot.main(_scripted_input(["hello"], []), outputs.append)

    assert status == 130
    assert outputs == [chatbot.WELCOME_BANNER, f"Dum-E: {chatbot.INTERRUPT_FAREWELL}"]


def test_main_handles_ctrl_c_from_output_without_duplicate_farewell() -> None:
    outputs: list[str] = []
    calls = 0

    def interrupting_output(message: str) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise KeyboardInterrupt
        outputs.append(message)

    status = chatbot.main(_scripted_input(["hello"], []), interrupting_output)

    assert status == 130
    assert outputs == [chatbot.WELCOME_BANNER, f"Dum-E: {chatbot.INTERRUPT_FAREWELL}"]


def test_main_returns_when_interrupt_farewell_output_is_interrupted() -> None:
    def always_interrupt(_: str) -> None:
        raise KeyboardInterrupt

    status = chatbot.main(_scripted_input([KeyboardInterrupt()], []), always_interrupt)

    assert status == 130


def test_importing_the_module_has_no_conversation_or_output_side_effect() -> None:
    result = subprocess.run(
        [sys.executable, "-S", "-c", "import chatbot"],
        cwd=Path(__file__).parent,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


@pytest.mark.parametrize(
    "message",
    [
        "I met Arkadeep yesterday",
        "Arkadeep is my friend",
        "Thanks to Arkadeep for helping me",
        "Great work, Arkadeep!",
        "Hey Arkadeep, thanks!",
    ],
)
def test_unrelated_mentions_of_arkadeep_do_not_trigger_sir_response(message: str) -> None:
    response = chatbot.get_response(message)
    assert response != chatbot.SIR_RESPONSE
    assert response != chatbot.ABOUT_SIR_RESPONSE
    assert response != chatbot.SIR_DETAIL_LIMITATION_RESPONSE


@pytest.mark.parametrize(
    "message",
    [
        "Who is Arkadeep's colleague?",
        "What do you know about Arkadeep?",
        "Tell me about Arkadeep",
        "Who is Dum-E's Sir?",
        "Who is Dum-E's creator?",
    ],
)
def test_actual_identity_questions_still_use_configured_identity_behavior(message: str) -> None:
    response = chatbot.get_response(message)
    assert response.startswith("My Sir, Arkadeep Sengupta.")
