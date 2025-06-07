import json
from django.conf import settings
import django


settings.configure(
    DEBUG=True,
    INSTALLED_APPS=("django.contrib.contenttypes",),
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "OPTIONS": {
                "service": "aba.rocks",
                "passfile": ".pgpass",
            },
        },
    },
)
django.setup()


from django.contrib.contenttypes.models import ContentType


def convert_fixture(file):
    with open(file) as f:
        d = json.load(f)
    j = []
    c = []
    a = []
    for i in d:
        if (
            i["model"] == "quiz.multiplechoicequestion"
            or i["model"] == "quiz.truefalsequestion"
        ):
            bf = i["fields"]
            q_model = i["model"].split(".")
            q_type = ContentType.objects.get_by_natural_key(q_model[0], q_model[1]).id
            bfs = dict(
                text=bf["text"],
                category=bf["category"],
                hint=bf["hint"],
                disabled=False,
                type=q_type,
            )
            b = dict(model="quiz.basequestion", pk=i["pk"], fields=bfs)
            j.append(b)

            cf = i["fields"]
            cfs = dict(answer=cf["answer"])
            ch = dict(model=i["model"], pk=i["pk"], fields=cfs)
            c.append(ch)
        elif i["model"] == "quiz.multiplechoiceanswer":
            af = i["fields"]
            afs = dict(question=af["question"], text=af["text"])
            ca = dict(
                model="quiz.multiplechoiceanswer",
                pk=i["pk"],
                fields=afs,
            )
            a.append(ca)
    j = j + c + a

    with open("quiz/fixtures/quiz_questions_choices.json", "w") as o:
        json.dump(
            j,
            o,
            indent=4,
        )


if __name__ == "__main__":
    import sys

    convert_fixture(sys.argv[1])
