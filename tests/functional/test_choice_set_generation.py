from app.factories.app_factory import create_app
from app.core.extensions import db
from app.helpers.helper import init_questions, init_event_types



app = create_app("Emil", "test")
db.create_all()
db.session.commit()
init_questions()
init_event_types()

client = app.test_client()


def test_choice_set_generated():
    response = client.post("http://localhost:5000/choicesets/", json = {"task_id": "test_task_id"})
    task_id = response.get_json()["choice_set"][0]["task_id"]
    assert task_id == "test_task_id"