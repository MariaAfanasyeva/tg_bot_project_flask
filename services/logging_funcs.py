from app import app


def before_request_log(model, user_id, method, raw_id):
    app.logger.info(
        f"User with id={user_id} has started {method} model {model} (raw ID={raw_id})"
    )


def after_request_log(model, user_id, method, raw_id):
    app.logger.info(
        f"User with id={user_id} has finished {method} model {model} (raw ID={raw_id})"
    )


def before_rollback_log(model, user_id, method, raw_id):
    app.logger.info(
        f"Before rollback user with id={user_id} has started {method} model {model} (raw ID={raw_id})"
    )


def check_owner(instance):
    try:
        owner_id = instance.add_by_user
    except:
        owner_id = None
    return owner_id


def session_handler(session):
    session_info = {}
    session_instance = ""
    method = ""
    for instance in session.new:
        method = "creating"
        session_instance = instance
    for instance in session.deleted:
        method = "deleting"
        session_instance = instance
    for instance in session.dirty:
        method = "updating"
        session_instance = instance
    owner_id = check_owner(session_instance)
    session_info["user_id"] = owner_id
    session_info["method"] = method
    session_info["model"] = session_instance.__tablename__
    session_info["raw_id"] = session_instance.id
    return session_info
