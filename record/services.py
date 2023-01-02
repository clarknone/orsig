import copy
import hashlib
import json

from django.utils.timezone import now

from record.models import Record, Commit


def get_last_commit():
    try:
        return Commit.objects.latest('date')
    except Commit.DoesNotExist:
        return None


def create_new_commit(record: Record, commit_hash: str):
    rest = copy.deepcopy(record.__dict__)
    rest['commit_hash'] = commit_hash
    last_commit = get_last_commit()
    rest['previous_hash'] = last_commit.hash if last_commit else ""
    rest['hash_name'] = "SHA512"
    rest['date'] = str(now())
    rest['user'] = record.user.email
    rest['date_created'] = str(record.date_created)
    rest['is_salted'] = False
    del rest['_state']
    del rest['user_id']
    del rest['is_committed']
    record_str = json.dumps(rest, sort_keys=True).encode()
    rest["hash"] = hashlib.sha512(record_str).hexdigest()
    commit = Commit.objects.create(**rest)
    return commit
