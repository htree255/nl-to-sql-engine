from prompt_examples import EXAMPLES
from schema_linker import tokenize


def get_similar_examples(question, top_n=3):
    """
    Score each example by word overlap with the question.
    Return top_n most similar examples.
    """
    question_words = tokenize(question)

    scores = []

    for example in EXAMPLES:
        example_words = tokenize(example["question"])
        overlap = example_words & question_words
        scores.append((len(overlap), example))

    # Sort by score, highest first
    scores.sort(key=lambda pair: pair[0], reverse=True)
    top_examples = []

    # Take the top N, but only ones with at least some overlap
    for score, ex in scores[:top_n]:
        top_examples.append(ex)

    return top_examples


def build_examples_text(examples):
    """
    Format selected examples as text to insert into the prompt.
    """

    if not examples:
        return ""

    text = "\nHere are some example questions and their correct SQL: \n"

    for ex in examples:
        text += f"Question: {ex["question"]}\n"
        text += f"SQL: {ex["sql"]}\n"

    return text


if __name__ == "__main__":

    test_questions = [
        "Who has the lowest salary?",
        "How many products has each employee sold?",
        "What is the total stock across all products?",
        "What is the most expensive product?",
    ]

    for question in test_questions:
        examples = get_similar_examples(question)
        print(f"Question: {question} \n")

        for ex in examples:
            print(f"Matched: {ex["question"]}\n")
