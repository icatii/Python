"""ADHD self-screening CLI app.

This tool is educational and cannot diagnose ADHD.
If screening suggests elevated risk, it recommends consulting
qualified healthcare professionals for proper assessment.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    text: str
    inattentive: bool


QUESTIONS = [
    Question("How often do you have trouble wrapping up final details of a project?", True),
    Question("How often do you have difficulty getting things in order for tasks?", True),
    Question("How often do you have problems remembering appointments or obligations?", True),
    Question("How often do you delay or avoid starting tasks requiring a lot of thought?", True),
    Question("How often do you fidget or squirm when sitting for a long time?", False),
    Question("How often do you feel overly active and compelled to do things?", False),
]

OPTIONS = {
    "0": ("Never", 0),
    "1": ("Rarely", 1),
    "2": ("Sometimes", 2),
    "3": ("Often", 3),
    "4": ("Very often", 4),
}


def ask_question(question: Question) -> int:
    print(f"\n{question.text}")
    for key, (label, _) in OPTIONS.items():
        print(f"  {key} - {label}")

    while True:
        choice = input("Choose 0-4: ").strip()
        if choice in OPTIONS:
            return OPTIONS[choice][1]
        print("Invalid choice. Enter a number from 0 to 4.")


def interpret_score(total_score: int, inattentive_score: int, hyperactive_score: int) -> str:
    if total_score >= 16 or inattentive_score >= 10 or hyperactive_score >= 8:
        return (
            "Your responses suggest possible ADHD-related symptoms. "
            "This is not a diagnosis. Please seek evaluation from a psychiatrist, "
            "psychologist, or another licensed specialist."
        )

    if total_score >= 10:
        return (
            "Your responses indicate some ADHD-like difficulties. "
            "Consider discussing this with a clinician if these issues affect school, work, or relationships."
        )

    return (
        "Your responses do not currently suggest a high likelihood of ADHD, "
        "but only a qualified specialist can assess this reliably."
    )


def run_screening() -> None:
    print("=" * 56)
    print("ADHD SELF-SCREENING (Educational, Not Diagnostic)")
    print("=" * 56)
    print(
        "This quick questionnaire is based on common adult ADHD symptom areas.\n"
        "It cannot diagnose ADHD or replace professional care."
    )

    total = 0
    inattentive_total = 0
    hyperactive_total = 0

    for question in QUESTIONS:
        score = ask_question(question)
        total += score
        if question.inattentive:
            inattentive_total += score
        else:
            hyperactive_total += score

    print("\n--- Result ---")
    print(f"Total score: {total}/24")
    print(f"Inattentive cluster: {inattentive_total}/16")
    print(f"Hyperactive/impulsive cluster: {hyperactive_total}/8")
    print(interpret_score(total, inattentive_total, hyperactive_total))
    print(
        "\nIf symptoms have lasted 6+ months and interfere with daily life, "
        "book a full assessment with a specialist."
    )


def main() -> None:
    run_screening()


if __name__ == "__main__":
    main()
