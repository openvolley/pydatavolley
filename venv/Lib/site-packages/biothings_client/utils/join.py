def get_dotfield(d, df):
    s = set()

    def _helper(_d, _k):
        _f = _k.split(".")
        if len(_f) == 0:
            return
        elif len(_f) == 1:
            _tk = _f[0]
            _nk = ""
        else:
            _tk = _f[0]
            _nk = ".".join(_f[1:])
        if isinstance(_d, list):
            for x in _d:
                _helper(x, _tk)
        elif isinstance(_d, dict):
            _v = _d.get(_tk, None)
            if _v:
                _helper(_v, _nk)
        else:
            s.add(_d)

    _helper(d, df)
    return list(s)


def unordered_chunk_iterator(client, query, join_field, chunk_size=100, query_kwargs=None):
    chunk = []
    join_val_dict = {}
    query_kwargs = query_kwargs or {}
    if query_kwargs.get("fields", None) and query_kwargs["fields"] != "all" and join_field != "_id":
        query_kwargs["fields"] = query_kwargs["fields"].rstrip(", ") + "," + join_field
    for doc in client.query(query, fetch_all=True, **query_kwargs):
        for doc_join_val in get_dotfield(doc, join_field):
            join_val_dict.setdefault(str(doc_join_val).lower(), []).append(len(chunk))
        chunk.append(doc)
        if len(join_val_dict) == chunk_size:
            yield chunk, join_val_dict
            chunk = []
            join_val_dict = {}
    if chunk:
        yield chunk, join_val_dict


def join(
    e1_client,
    e2_client,
    size=10,
    e1_query="__all__",
    e2_query="__all__",
    e1_join_field="_id",
    e2_join_field="_id",
    e1_kwargs=None,
    e2_kwargs=None,
):
    """implements a join with e1 being the outer loop and e2 being the inner loop"""
    ret_chunk = []
    e1_kwargs = e1_kwargs or {}
    e2_kwargs = e2_kwargs or {}
    for outer_doc_chunk, outer_join_val_dict in unordered_chunk_iterator(e1_client, e1_query, e1_join_field, e1_kwargs):
        if outer_doc_chunk:
            inner_query_string = " OR ".join(["{}:{}".format(e2_join_field, x) for x in outer_join_val_dict.keys()])
            if e2_query != "__all__":
                inner_query_string = "((" + inner_query_string + ") AND (" + e2_query + "))"
            if e2_kwargs.get("fields", None) and e2_kwargs["fields"] != "all" and e2_join_field != "_id":
                e2_kwargs["fields"] = e2_kwargs["fields"].rstrip(", ") + "," + e2_join_field
            e2_val_join_dict = {}
            for inner_doc in e2_client.query(inner_query_string, fetch_all=True, **e2_kwargs):
                for doc_join_val in get_dotfield(inner_doc, e2_join_field):
                    e2_val_join_dict.setdefault(str(doc_join_val).lower(), []).append(inner_doc)
            # merge the docs for this chunk
            chunk_intersection = set(list(e2_val_join_dict.keys())).intersection(set(list(outer_join_val_dict.keys())))
            if len(chunk_intersection) > 0:
                for merge_join_field in set(list(e2_val_join_dict.keys())).intersection(
                    set(list(outer_join_val_dict.keys()))
                ):
                    for index in outer_join_val_dict[merge_join_field]:
                        outer_doc_chunk[index].setdefault(e2_client._entity, []).extend(
                            e2_val_join_dict[merge_join_field]
                        )
                for p in set([p for v in chunk_intersection for p in outer_join_val_dict[v]]):
                    ret_chunk.append(outer_doc_chunk[p])
                    if len(ret_chunk) == size:
                        yield ret_chunk
                        ret_chunk = []
    if ret_chunk:
        yield ret_chunk
