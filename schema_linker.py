from schema import SCHEMA
import string

# Common English words that appear everywhere and carry no
# meaningful signal about which table is relevant.
STOPWORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "in",
    "on",
    "at",
    "of",
    "to",
    "and",
    "or",
    "for",
    "with",
    "by",
    "this",
    "that",
    "each",
    "which",
    "what",
    "who",
    "how",
    "many",
    "list",
    "show",
    "all",
    "find",
    "get",
    "as",
    "be",
    "it",
    "its",
}


def clean_word(word):
    return word.strip(string.punctuation).lower()


def tokenize(text):
    """
    Split text into a set of cleaned, meaningful words —
    lowercased, punctuation stripped, stopwords removed.
    """
    cleaned = set()
    words = text.split()
    for word in words:
        if word and clean_word(word) not in STOPWORDS:
            cleaned.add(clean_word(word))

    return cleaned


def get_table_keywords(table_name, table_info):
    """
    Build a 'bag of words' for one table — every word that's
    associated with it.

    This is what we'll compare against the question's words.
    """

    keywords = set()

    # Add the table name
    keywords.add(table_name)

    # Add the table description
    keywords.update(tokenize(table_info["description"]))

    # Add the columns
    for col_name, col_desc in table_info["columns"].items():
        keywords.update(tokenize(col_name))
        keywords.update(tokenize(col_desc))

    return keywords


def get_relevant_tables(question, schema=SCHEMA):
    """
    Given a plain English question, figure out which tables
    are relevant by counting how many words overlap between
    the question and each table's keyword set.

    Returns a list of table names, most relevant first.
    """

    # Break the question into individual lowercase words
    question_words = set(question.lower().replace("?", "").split())

    # Score each table by counting overlapping words
    scores = {}

    for table_name, table_info in schema.items():
        table_keywords = get_table_keywords(table_name, table_info)
        overlap = question_words & table_keywords
        scores[table_name] = len(overlap)

    # Sort tables by score, highest first
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    # Always include the top-scoring table.
    # Include any others that scored above 0 too —
    # the question might genuinely need multiple tables (joins).
    selected = [ranked[0][0]]

    for table_name, table_score in ranked[1:]:
        if table_score > 0:
            selected.append(table_name)

    return selected


def build_schema(table_names, schema=SCHEMA):
    """
    Given a list of table names, build a
    plain-text schema description only for those tables.
    """
    text = ""

    for table_name in table_names:
        table_info = schema[table_name]
        text += f"\nTable: {table_name}\n"
        text += f" ({table_info['description']})\n"
        for col_name, col_desc in table_info["columns"].items():
            text += f" - {col_name} : {col_desc}\n"

    return text


# Test
if __name__ == "__main__":

    questions = [
        "What is the highest salary in the Engineering department?",
        "Which product has the lowest stock?",
        "How many units did each employee sell?",
        "List all products under $100",
    ]

    for question in questions:
        tables = get_relevant_tables(question)
        print(f"Question: {question}")
        print(f"Selected tables: {tables}")
        print("Schema sent to AI.")
        print(build_schema(tables))
