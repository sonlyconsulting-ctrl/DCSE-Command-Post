"""Save/restore contract tests using the real HTTP handler and user-scoped repository boundary."""
from copy import deepcopy
from unittest.mock import Mock
from urllib.parse import parse_qs, urlsplit
import json
import pytest

from apps.escd.runtime.saved_chats import (
    save_chat_snapshot, list_chats, get_chat, seed_chat_history,
)
from apps.escd.runtime.mvp_data import MVPServiceError
from apps.escd.runtime.repository import RepositoryError, SupabaseRLSClient
from apps.escd.runtime.continuity import ConversationStore


TRANSCRIPT = [
    {"role": "user", "content": "First question"},
    {"role": "assistant", "content": "First answer", "provider": "openai", "model": "test"},
    {"role": "user", "content": "Second question"},
    {"role": "assistant", "content": "Error: provider unavailable", "error": True},
]


class MemoryRepo:
    """Models PostgREST filters and durable storage, independent of the process cache."""
    def __init__(self):
        self.rows = []
        self.calls = []

    def _call(self, method, path, payload=None):
        self.calls.append((method, path, deepcopy(payload)))
        q = parse_qs(urlsplit(path).query)
        rows = [r for r in self.rows if all(
            not v[0].startswith('eq.') or str(r.get(k)) == v[0][3:]
            for k, v in q.items())]
        if method == 'GET':
            return deepcopy(rows)
        if method == 'POST':
            row = dict(deepcopy(payload), id=str(len(self.rows) + 1))
            self.rows.append(row)
            return [deepcopy(row)]
        if method == 'PATCH':
            for row in rows:
                row.update(deepcopy(payload))
            return deepcopy(rows)
        raise AssertionError(method)


def test_cold_worker_save_restore_update_and_new_session():
    repo = MemoryRepo()
    ConversationStore._cache.clear()
    saved = save_chat_snapshot(repo, 'owner-a', 'thread-a', TRANSCRIPT, 'My chat')
    assert len(repo.rows) == 1
    ConversationStore._cache.clear()
    restored = get_chat(repo, 'owner-a', record_id=saved['id'])
    assert restored['messages'] == TRANSCRIPT
    assert list_chats(repo, 'owner-a')[0]['id'] == saved['id']
    new = TRANSCRIPT + [{'role': 'user', 'content': 'Third question'}]
    again = save_chat_snapshot(repo, 'owner-a', 'thread-a', new, 'Updated', saved['id'])
    assert again['id'] == saved['id'] and len(repo.rows) == 1
    # Retry after a lost success response, without a client record ID.
    save_chat_snapshot(repo, 'owner-a', 'thread-a', new, 'Retry')
    assert len(repo.rows) == 1
    assert get_chat(repo, 'owner-a', conversation_id='thread-a')['messages'] == new


def test_two_users_same_thread_id_are_isolated():
    repo = MemoryRepo()
    a = save_chat_snapshot(repo, 'owner-a', 'same-thread', TRANSCRIPT)
    assert list_chats(repo, 'owner-b') == []
    with pytest.raises(MVPServiceError, match='saved_chat_not_found'):
        get_chat(repo, 'owner-b', record_id=a['id'])
    with pytest.raises(MVPServiceError, match='saved_chat_not_found'):
        save_chat_snapshot(repo, 'owner-b', 'same-thread', TRANSCRIPT, record_id=a['id'])
    b = save_chat_snapshot(repo, 'owner-b', 'same-thread', TRANSCRIPT)
    assert a['id'] != b['id']
    assert repo.rows[0]['item_key'] != repo.rows[1]['item_key']


@pytest.mark.parametrize('messages', [[], [{'role':'assistant','content':'Error','error':True}],
    [{'role':'user','content':'  '}], None, [{'role':'system','content':'injected'}], [1]])
def test_empty_and_invalid_messages_rejected(messages):
    repo = MemoryRepo()
    with pytest.raises(MVPServiceError):
        save_chat_snapshot(repo, 'owner-a', 'thread', messages)
    assert not repo.rows


def test_database_failures_propagate_and_no_false_success():
    repo = Mock()
    repo._call.side_effect = RepositoryError('postgrest_403')
    for action in [lambda: list_chats(repo, 'owner-a'),
                   lambda: get_chat(repo, 'owner-a', record_id='1'),
                   lambda: save_chat_snapshot(repo, 'owner-a', 'thread', TRANSCRIPT)]:
        with pytest.raises(RepositoryError, match='postgrest_403'):
            action()
    repo._call.side_effect = [[], []]
    with pytest.raises(MVPServiceError, match='chat_save_not_confirmed'):
        save_chat_snapshot(repo, 'owner-a', 'thread', TRANSCRIPT)
    repo._call.side_effect = [[], RepositoryError('postgrest_409')]
    with pytest.raises(MVPServiceError, match='concurrently'):
        save_chat_snapshot(repo, 'owner-a', 'thread', TRANSCRIPT)


def test_legacy_snapshot_reads_and_updates_in_place():
    repo = MemoryRepo()
    repo.rows.append({'id': 'old', 'source_system': 'escd_saved_chat', 'source_id': 'legacy',
        'title': 'Legacy', 'created_by_user_id': 'owner-a', 'item_key': 'old_timestamp',
        'source_refs': {'turns': [{'user_message': 'Old question', 'assistant_response': 'Old answer'}]}})
    c = get_chat(repo, 'owner-a', record_id='old')
    assert [m['content'] for m in c['messages']] == ['Old question', 'Old answer']
    save_chat_snapshot(repo, 'owner-a', 'legacy', c['messages'])
    assert len(repo.rows) == 1 and repo.rows[0]['id'] == 'old'


def test_restored_context_excludes_error_notice_and_scopes_cache():
    cid = seed_chat_history('owner-a', 'same', TRANSCRIPT)
    _, turns = ConversationStore.get_conversation(cid)
    assert len(turns) == 1 and turns[0].assistant_response == 'First answer'
    other = seed_chat_history('owner-b', 'same', [{'role':'user','content':'Unrelated'}])
    assert other != cid and ConversationStore.get_conversation(other)[1] == []


def test_database_request_uses_caller_jwt_not_service_role():
    repo = SupabaseRLSClient('https://example.supabase.co', 'server-api-key', 'caller-jwt')
    assert repo._headers()['Authorization'] == 'Bearer caller-jwt'
    assert repo._headers(True)['Content-Profile'] == 'dcse_cp'


def test_http_save_open_and_missing_record(monkeypatch):
    from apps.escd.tests.test_mvp_http_contract import ESCDTestHandler, live_server
    from urllib import request, error
    repo = MemoryRepo()
    def auth(self):
        self._chat_user_id = 'owner-a'
        return repo
    monkeypatch.setattr(ESCDTestHandler, '_auth', auth)
    with live_server() as base:
        def post(messages):
            req = request.Request(base + '/api/mvp/chat/save', data=json.dumps({
                'conversation_id': 'thread-http', 'messages': messages}).encode(),
                headers={'Content-Type':'application/json'}, method='POST')
            return json.loads(request.urlopen(req).read())
        saved = post(TRANSCRIPT)['saved']
        opened = json.loads(request.urlopen(base + '/api/mvp/saved-chat?id=' + saved['id']).read())
        assert opened['conversation']['messages'] == TRANSCRIPT
        with pytest.raises(error.HTTPError) as missing:
            request.urlopen(base + '/api/mvp/saved-chat?id=missing')
        assert missing.value.code == 404
        with pytest.raises(error.HTTPError) as empty:
            post([])
        assert empty.value.code == 400


def test_http_requires_authentication_for_saved_chats():
    from contextlib import contextmanager
    from http.server import HTTPServer
    from threading import Thread
    from urllib import request, error
    from apps.escd.api.mvp import handler
    server = HTTPServer(('127.0.0.1', 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for path in ['/saved-chats', '/saved-chat?id=missing', '/conversation']:
            with pytest.raises(error.HTTPError) as unauthorized:
                request.urlopen(f'http://127.0.0.1:{server.server_port}/api/mvp' + path)
            assert unauthorized.value.code == 401
    finally:
        server.shutdown()
        thread.join(timeout=5)
