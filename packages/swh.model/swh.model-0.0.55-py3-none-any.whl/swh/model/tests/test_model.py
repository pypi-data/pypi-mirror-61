# Copyright (C) 2019 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import copy

from hypothesis import given

from swh.model.model import Content, Directory, Revision, Release, Snapshot
from swh.model.hashutil import hash_to_bytes
from swh.model.hypothesis_strategies import objects, origins, origin_visits
from swh.model.identifiers import (
    directory_identifier, revision_identifier, release_identifier,
    snapshot_identifier
)
from swh.model.tests.test_identifiers import (
    directory_example, revision_example, release_example, snapshot_example
)


@given(objects())
def test_todict_inverse_fromdict(objtype_and_obj):
    (obj_type, obj) = objtype_and_obj

    if obj_type in ('origin', 'origin_visit'):
        return

    obj_as_dict = obj.to_dict()
    obj_as_dict_copy = copy.deepcopy(obj_as_dict)

    # Check the composition of to_dict and from_dict is the identity
    assert obj == type(obj).from_dict(obj_as_dict)

    # Check from_dict() does not change the input dict
    assert obj_as_dict == obj_as_dict_copy

    # Check the composition of from_dict and to_dict is the identity
    assert obj_as_dict == type(obj).from_dict(obj_as_dict).to_dict()


@given(origins())
def test_todict_origins(origin):
    obj = origin.to_dict()

    assert 'type' not in obj
    assert type(origin)(url=origin.url) == type(origin).from_dict(obj)


@given(origin_visits())
def test_todict_origin_visits(origin_visit):
    obj = origin_visit.to_dict()

    assert origin_visit == type(origin_visit).from_dict(obj)


def test_content_get_hash():
    hashes = dict(
        sha1=b'foo', sha1_git=b'bar', sha256=b'baz', blake2s256=b'qux')
    c = Content(length=42, status='visible', **hashes)
    for (hash_name, hash_) in hashes.items():
        assert c.get_hash(hash_name) == hash_


def test_directory_model_id_computation():
    dir_dict = dict(directory_example)
    del dir_dict['id']

    dir_id = hash_to_bytes(directory_identifier(dir_dict))
    for dir_model in [Directory(**dir_dict), Directory.from_dict(dir_dict)]:
        assert dir_model.id == dir_id


def test_revision_model_id_computation():
    rev_dict = dict(revision_example)
    del rev_dict['id']

    rev_id = hash_to_bytes(revision_identifier(rev_dict))
    for rev_model in [Revision(**rev_dict), Revision.from_dict(rev_dict)]:
        assert rev_model.id == rev_id


def test_revision_model_id_computation_with_no_date():
    """We can have revision with date to None

    """
    rev_dict = dict(revision_example)
    rev_dict['date'] = None
    rev_dict['committer_date'] = None
    del rev_dict['id']

    rev_id = hash_to_bytes(revision_identifier(rev_dict))
    for rev_model in [Revision(**rev_dict), Revision.from_dict(rev_dict)]:
        assert rev_model.date is None
        assert rev_model.committer_date is None
        assert rev_model.id == rev_id


def test_release_model_id_computation():
    rel_dict = dict(release_example)
    del rel_dict['id']

    rel_id = hash_to_bytes(release_identifier(rel_dict))
    for rel_model in [Release(**rel_dict), Release.from_dict(rel_dict)]:
        assert rel_model.id == hash_to_bytes(rel_id)


def test_snapshot_model_id_computation():
    snp_dict = dict(snapshot_example)
    del snp_dict['id']

    snp_id = hash_to_bytes(snapshot_identifier(snp_dict))
    for snp_model in [Snapshot(**snp_dict), Snapshot.from_dict(snp_dict)]:
        assert snp_model.id == snp_id
