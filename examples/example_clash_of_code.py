from time import sleep

import codingame

client = codingame.Client()

# get a pending public clash of code
coc = client.get_pending_clash_of_code()
# or get a clash of code from its public handle
coc = client.get_clash_of_code("clash of code handle here")

# or if you want to create and play a private clash of code
client.login(remember_me_cookie="your cookie here")
coc = client.create_private_clash_of_code(
    language_ids=["Python3"], modes=["SHORTEST"]
)
print("Join here :", coc.join_url)

# wait for at least 2 players
while len(coc.players) < 2:
    # refetch the data every second
    sleep(1)
    coc.fetch()
    print("Players :", ", ".join([p.pseudo for p in coc.players]), end="\r")

coc.start(refetch=True)

# coc.start just starts a 5s countdown so we have to wait
while not coc.started:
    sleep(1)
    coc.fetch()

print("Started with players :", ", ".join([p.pseudo for p in coc.players]))

# get the prompt and update the CoC object
question = coc.get_question()


# parse the statement if BeautifulSoup4 is installed
try:
    import html

    from bs4 import BeautifulSoup, Tag
except ModuleNotFoundError:
    print(question.raw_statement)
else:

    def readable(tag: Tag) -> str:
        return (
            html.unescape(tag.decode_contents())
            .replace("<var>", "`")
            .replace("</var>", "`")
            .replace("<const>", "")
            .replace("</const>", "")
            .replace("<strong>", "**")
            .replace("</strong>", "**")
            .replace("<br/>", "\n")
        )

    statement_soup = BeautifulSoup(question.raw_statement, "html.parser")
    statement = readable(statement_soup.find(class_="question-statement"))
    statement_input = readable(
        statement_soup.find(class_="question-statement-input")
    )
    statement_output = readable(
        statement_soup.find(class_="question-statement-output")
    )
    statement_constraints = readable(
        statement_soup.find(class_="question-statement-constraints")
    )
    example_in = readable(
        statement_soup.find(class_="question-statement-example-in")
    )
    example_out = readable(
        statement_soup.find(class_="question-statement-example-out")
    )

    print(
        "Goal",
        statement,
        "",
        "Input",
        statement_input,
        "",
        "Output",
        statement_output,
        "",
        "Constraints",
        statement_constraints,
        "",
        "Example",
        "Input",
        example_in,
        "Output",
        example_out,
        "",
        sep="\n",
    )

# choose a programming language among the allowed ones
print("Languages :", ", ".join(coc.programming_languages))
lang = (
    input("Your language : ")
    if len(coc.programming_languages) > 1
    else coc.programming_languages[0]
)
while lang not in coc.programming_languages:
    print(
        "Wrong language, allowed languages :",
        ", ".join(coc.programming_languages),
    )
    lang = input("Your language : ")

# write the code for the statement
print("\nEnter your code, enter \\q at the end")
code = input()
while "\\q" not in code:
    code += "\n" + input()
code = code.replace("\\q", "")

# test the code against the test cases
test_case_results = coc.play_test_cases(lang, code, refetch=True)
print("\nTest cases")
for index, result in test_case_results.items():
    print("Test case", index, "passed" if result.success else "failed")
    if not result.success:
        print("Expected :", result.expected)
        print("Found :", result.found)

# submit the code
solution = coc.submit(lang, code, refetch=True)
# share the code
solution.share()
print("Code submitted and shared")

# wait for the clash of code to be finished
while not coc.finished:
    sleep(5)
    coc.fetch()

# show the rankings with the code if shared
ranked_players = sorted(coc.players, key=lambda p: p.rank)
for player in ranked_players:
    print(
        "\n{0.rank}. {0.pseudo}, {0.score}%{1}, "
        "{0.duration.seconds}s, {0.language_id}".format(
            player,
            f", {player.code_length} char" if coc.mode == "SHORTEST" else "",
        )
    )
    if player.solution_shared:
        solution = player.get_solution()
        print(solution.code)
