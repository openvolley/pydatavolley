"""
Python Client for generic Biothings API services
"""
from __future__ import print_function

import logging
import os
import platform
import time
import warnings
from collections import Counter
from itertools import islice

import requests

from .utils import str_types, is_py27

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

try:
    from pandas import DataFrame, json_normalize

    df_avail = True
except ImportError:
    df_avail = False

try:
    import requests_cache

    caching_avail = True
except ImportError:
    caching_avail = False


__version__ = "0.3.1"

logger = logging.getLogger("biothings.client")
if is_py27:
    # we need to setup default log handler in Py 2.7
    # Py 3.x does it by default
    handler = logging.StreamHandler()
    # formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    # handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Future work:
# Consider use "verbose" settings to control default logging output level
# by doing this instead of using branching throughout the application,
# the business logic can be more concise and more readable.


class ScanError(Exception):
    # for errors in scan search type
    pass


def alwayslist(value):
    """If input value if not a list/tuple type, return it as a single value list.

    Example:

    >>> x = 'abc'
    >>> for xx in alwayslist(x):
    ...     print xx
    >>> x = ['abc', 'def']
    >>> for xx in alwayslist(x):
    ...     print xx

    """
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


def safe_str(s, encoding="utf-8"):
    """Perform proper encoding if input is an unicode string."""
    try:
        _s = str(s)
    except UnicodeEncodeError:
        _s = s.encode(encoding)
    return _s


def list_itemcnt(li):
    """Return number of occurrence for each item in the list."""
    return list(Counter(li).items())


def iter_n(iterable, n, with_cnt=False):
    """
    Iterate an iterator by chunks (of n)
    if with_cnt is True, return (chunk, cnt) each time
    """
    it = iter(iterable)
    if with_cnt:
        cnt = 0
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        if with_cnt:
            cnt += len(chunk)
            yield (chunk, cnt)
        else:
            yield chunk


class BiothingClient(object):
    """This is the client for a biothing web service."""

    def __init__(self, url=None):
        if url is None:
            url = self._default_url
        self.url = url
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        self.max_query = self._max_query
        # delay and step attributes are for batch queries.
        self.delay = self._delay  # delay is ignored when requests made from cache.
        self.step = self._step
        self.scroll_size = self._scroll_size
        # raise requests.exceptions.HTTPError for status_code > 400
        #   but not for 404 on getvariant
        #   set to False to suppress the exceptions.
        self.raise_for_status = True
        self.default_user_agent = (
            "{package_header}/{client_version} (" "python:{python_version} " "requests:{requests_version}" ")"
        ).format(
            **{
                "package_header": self._pkg_user_agent_header,
                "client_version": __version__,
                "python_version": platform.python_version(),
                "requests_version": requests.__version__,
            }
        )
        self._cached = False

    def use_http(self):
        """Use http instead of https for API calls."""
        if self.url:
            self.url = self.url.replace("https://", "http://")

    def use_https(self):
        """Use https instead of http for API calls. This is the default."""
        if self.url:
            self.url = self.url.replace("http://", "https://")

    @staticmethod
    def _dataframe(obj, dataframe, df_index=True):
        """Converts object to DataFrame (pandas)"""
        if not df_avail:
            raise RuntimeError("Error: pandas module must be installed " "(or upgraded) for as_dataframe option.")
        # if dataframe not in ["by_source", "normal"]:
        if dataframe not in [1, 2]:
            raise ValueError("dataframe must be either 1 (using json_normalize) " "or 2 (using DataFrame.from_dict")
        if "hits" in obj:
            if dataframe == 1:
                df = json_normalize(obj["hits"])
            else:
                df = DataFrame.from_dict(obj)
        else:
            if dataframe == 1:
                df = json_normalize(obj)
            else:
                df = DataFrame.from_dict(obj)
        if df_index:
            df = df.set_index("query")
        return df

    def _get(self, url, params=None, none_on_404=False, verbose=True):
        params = params or {}
        debug = params.pop("debug", False)
        return_raw = params.pop("return_raw", False)
        headers = {"user-agent": self.default_user_agent}
        res = requests.get(url, params=params, headers=headers)
        from_cache = getattr(res, "from_cache", False)
        if debug:
            return from_cache, res
        if none_on_404 and res.status_code == 404:
            return from_cache, None
        if self.raise_for_status:
            # raise requests.exceptions.HTTPError if not 200
            res.raise_for_status()
        if return_raw:
            return from_cache, res.text
        ret = res.json()
        return from_cache, ret

    def _post(self, url, params, verbose=True):
        return_raw = params.pop("return_raw", False)
        headers = {"user-agent": self.default_user_agent}
        res = requests.post(url, data=params, headers=headers)
        from_cache = getattr(res, "from_cache", False)
        if self.raise_for_status:
            # raise requests.exceptions.HTTPError if not 200
            res.raise_for_status()
        if return_raw:
            return from_cache, res
        ret = res.json()
        return from_cache, ret

    @staticmethod
    def _format_list(a_list, sep=",", quoted=True):
        if isinstance(a_list, (list, tuple)):
            if quoted:
                _out = sep.join(['"{}"'.format(safe_str(x)) for x in a_list])
            else:
                _out = sep.join(["{}".format(safe_str(x)) for x in a_list])
        else:
            _out = a_list  # a_list is already a comma separated string
        return _out

    def _handle_common_kwargs(self, kwargs):
        # handle these common parameters accept field names as the value
        for kw in ["fields", "always_list", "allow_null"]:
            if kw in kwargs:
                kwargs[kw] = self._format_list(kwargs[kw], quoted=False)
        return kwargs

    def _repeated_query_old(self, query_fn, query_li, verbose=True, **fn_kwargs):
        """This is deprecated, query_li can only be a list"""
        step = min(self.step, self.max_query)
        if len(query_li) <= step:
            # No need to do series of batch queries, turn off verbose output
            verbose = False
        for i in range(0, len(query_li), step):
            is_last_loop = i + step >= len(query_li)
            if verbose:
                logger.info("querying {0}-{1}...".format(i + 1, min(i + step, len(query_li))))
            query_result = query_fn(query_li[i : i + step], **fn_kwargs)

            yield query_result

            if verbose:
                logger.info("done.")
            if not is_last_loop and self.delay:
                time.sleep(self.delay)

    def _repeated_query(self, query_fn, query_li, verbose=True, **fn_kwargs):
        """Run query_fn for input query_li in a batch (self.step).
        return a generator of query_result in each batch.
        input query_li can be a list/tuple/iterable
        """
        step = min(self.step, self.max_query)
        i = 0
        for batch, cnt in iter_n(query_li, step, with_cnt=True):
            if verbose:
                logger.info("querying {0}-{1}...".format(i + 1, cnt))
            i = cnt
            from_cache, query_result = query_fn(batch, **fn_kwargs)
            yield query_result
            if verbose:
                cache_str = " {0}".format(self._from_cache_notification) if from_cache else ""
                logger.info("done.{0}".format(cache_str))
            if not from_cache and self.delay:
                # no need to delay if requests are from cache.
                time.sleep(self.delay)

    @property
    def _from_cache_notification(self):
        """Notification to alert user that a cached result is being returned."""
        return "[ from cache ]"

    def _metadata(self, verbose=True, **kwargs):
        """Return a dictionary of Biothing metadata."""
        _url = self.url + self._metadata_endpoint
        from_cache, ret = self._get(_url, params=kwargs, verbose=verbose)
        if verbose and from_cache:
            logger.info(self._from_cache_notification)
        return ret

    def _set_caching(self, cache_db=None, verbose=True, **kwargs):
        """Installs a local cache for all requests.

        **cache_db** is the path to the local sqlite cache database."""
        if caching_avail:
            if cache_db is None:
                cache_db = self._default_cache_file
            requests_cache.install_cache(cache_name=cache_db, allowable_methods=("GET", "POST"), **kwargs)
            self._cached = True
            if verbose:
                logger.info('[ Future queries will be cached in "{0}" ]'.format(os.path.abspath(cache_db + ".sqlite")))
        else:
            raise RuntimeError(
                "The requests_cache python module is required to use request caching. See "
                "https://requests-cache.readthedocs.io/en/latest/user_guide.html#installation"
            )

    def _stop_caching(self):
        """Stop caching."""
        if self._cached and caching_avail:
            requests_cache.uninstall_cache()
            self._cached = False
        return

    def _clear_cache(self):
        """Clear the globally installed cache."""
        try:
            requests_cache.clear()
        except AttributeError:
            # requests_cache is not enabled
            logger.warning("requests_cache is not enabled. Nothing to clear.")

    def _get_fields(self, search_term=None, verbose=True):
        """Wrapper for /metadata/fields

            **search_term** is a case insensitive string to search for in available field names.
            If not provided, all available fields will be returned.

        .. Hint:: This is useful to find out the field names you need to pass to **fields** parameter of other methods.

        """
        _url = self.url + self._metadata_fields_endpoint
        if search_term:
            params = {"search": search_term}
        else:
            params = {}
        from_cache, ret = self._get(_url, params=params, verbose=verbose)
        for k, v in ret.items():
            del k
            # Get rid of the notes column information
            if "notes" in v:
                del v["notes"]
        if verbose and from_cache:
            logger.info(self._from_cache_notification)
        return ret

    def _getannotation(self, _id, fields=None, **kwargs):
        """Return the object given id.
        This is a wrapper for GET query of the biothings annotation service.

        :param _id: an entity id.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned.

        :return: an entity object as a dictionary, or None if _id is not found.
        """
        verbose = kwargs.pop("verbose", True)
        if fields:
            kwargs["fields"] = fields
        kwargs = self._handle_common_kwargs(kwargs)
        _url = self.url + self._annotation_endpoint + str(_id)
        from_cache, ret = self._get(_url, kwargs, none_on_404=True, verbose=verbose)
        if verbose and from_cache:
            logger.info(self._from_cache_notification)
        return ret

    def _getannotations_inner(self, ids, verbose=True, **kwargs):
        _kwargs = {"ids": self._format_list(ids)}
        _kwargs.update(kwargs)
        _url = self.url + self._annotation_endpoint
        return self._post(_url, _kwargs, verbose=verbose)

    def _annotations_generator(self, query_fn, ids, verbose=True, **kwargs):
        """Function to yield a batch of hits one at a time."""
        for hits in self._repeated_query(query_fn, ids, verbose=verbose):
            for hit in hits:
                yield hit

    def _getannotations(self, ids, fields=None, **kwargs):
        """Return the list of annotation objects for the given list of ids.
        This is a wrapper for POST query of the biothings annotation service.

        :param ids: a list/tuple/iterable or a string of ids.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned.
        :param as_generator: if True, will yield the results in a generator.
        :param as_dataframe: if True or 1 or 2, return object as DataFrame (requires Pandas).
                                  True or 1: using json_normalize
                                  2        : using DataFrame.from_dict
                                  otherwise: return original json
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.

        :return: a list of objects or a pandas DataFrame object (when **as_dataframe** is True)

        .. Hint:: A large list of more than 1000 input ids will be sent to the backend
                  web service in batches (1000 at a time), and then the results will be
                  concatenated together. So, from the user-end, it's exactly the same as
                  passing a shorter list. You don't need to worry about saturating our
                  backend servers.

        .. Hint:: If you need to pass a very large list of input ids, you can pass a generator
                  instead of a full list, which is more memory efficient.
        """
        if isinstance(ids, str_types):
            ids = ids.split(",") if ids else []
        if not (isinstance(ids, (list, tuple, Iterable))):
            raise ValueError('input "ids" must be a list, tuple or iterable.')
        if fields:
            kwargs["fields"] = fields
        kwargs = self._handle_common_kwargs(kwargs)
        verbose = kwargs.pop("verbose", True)
        dataframe = kwargs.pop("as_dataframe", None)
        df_index = kwargs.pop("df_index", True)
        generator = kwargs.pop("as_generator", False)
        if dataframe in [True, 1]:
            dataframe = 1
        elif dataframe != 2:
            dataframe = None
        return_raw = kwargs.get("return_raw", False)
        if return_raw:
            dataframe = None

        def query_fn(ids):
            return self._getannotations_inner(ids, verbose=verbose, **kwargs)

        if generator:
            return self._annotations_generator(query_fn, ids, verbose=verbose, **kwargs)
        out = []
        for hits in self._repeated_query(query_fn, ids, verbose=verbose):
            if return_raw:
                out.append(hits)  # hits is the raw response text
            else:
                out.extend(hits)
        if return_raw and len(out) == 1:
            out = out[0]
        if dataframe:
            out = self._dataframe(out, dataframe, df_index=df_index)
        return out

    def _query(self, q, **kwargs):
        """Return the query result.
        This is a wrapper for GET query of biothings query service.

        :param q: a query string.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned.
        :param size:   the maximum number of results to return (with a cap
                       of 1000 at the moment). Default: 10.
        :param skip:   the number of results to skip. Default: 0.
        :param sort:   Prefix with "-" for descending order, otherwise in ascending order.
                       Default: sort by matching scores in decending order.
        :param as_dataframe: if True or 1 or 2, return object as DataFrame (requires Pandas).
                                  True or 1: using json_normalize
                                  2        : using DataFrame.from_dict
                                  otherwise: return original json
        :param fetch_all: if True, return a generator to all query results (unsorted).  This can provide a very fast
                          return of all hits from a large query.
                          Server requests are done in blocks of 1000 and yielded individually.  Each 1000 block of
                          results must be yielded within 1 minute, otherwise the request will expire at server side.

        :return: a dictionary with returned variant hits or a pandas DataFrame object (when **as_dataframe** is True)
                 or a generator of all hits (when **fetch_all** is True)

        .. Hint:: By default, **query** method returns the first 10 hits if the matched hits are >10.
                  If the total number of hits are less than 1000, you can increase the value for
                  **size** parameter. For a query that returns more than 1000 hits, you can pass
                  "fetch_all=True" to return a `generator <http://www.learnpython.org/en/Generators>`_
                  of all matching hits (internally, those hits are requested from the server in blocks of 1000).
        """
        _url = self.url + self._query_endpoint
        verbose = kwargs.pop("verbose", True)
        kwargs = self._handle_common_kwargs(kwargs)
        kwargs.update({"q": q})
        fetch_all = kwargs.get("fetch_all")
        if fetch_all in [True, 1]:
            if kwargs.get("as_dataframe", None) in [True, 1]:
                warnings.warn(
                    "Ignored 'as_dataframe' because 'fetch_all' is specified. "
                    "Too many documents to return as a Dataframe."
                )
            return self._fetch_all(url=_url, verbose=verbose, **kwargs)
        dataframe = kwargs.pop("as_dataframe", None)
        if dataframe in [True, 1]:
            dataframe = 1
        elif dataframe != 2:
            dataframe = None
        from_cache, out = self._get(_url, kwargs, verbose=verbose)
        if verbose and from_cache:
            logger.info(self._from_cache_notification)
        if dataframe:
            out = self._dataframe(out, dataframe, df_index=False)
        return out

    def _fetch_all(self, url, verbose=True, **kwargs):
        """Function that returns a generator to results. Assumes that 'q' is in kwargs."""

        # function to get the next batch of results, automatically disables cache if we are caching
        def _batch():
            if caching_avail and self._cached:
                self._cached = False
                with requests_cache.disabled():
                    from_cache, ret = self._get(url, params=kwargs, verbose=verbose)
                    del from_cache
                self._cached = True
            else:
                from_cache, ret = self._get(url, params=kwargs, verbose=verbose)
            return ret

        batch = _batch()
        if verbose:
            logger.info("Fetching {0} {1} . . .".format(batch["total"], self._optionally_plural_object_type))
        for key in ["q", "fetch_all"]:
            kwargs.pop(key)
        while not batch.get("error", "").startswith("No results to return"):
            if "error" in batch:
                logger.error(batch["error"])
                break
            if "_warning" in batch and verbose:
                logger.warning(batch["_warning"])
            for hit in batch["hits"]:
                yield hit
            kwargs.update({"scroll_id": batch["_scroll_id"]})
            batch = _batch()

    def _querymany_inner(self, qterms, verbose=True, **kwargs):
        _kwargs = {"q": self._format_list(qterms)}
        _kwargs.update(kwargs)
        _url = self.url + self._query_endpoint
        return self._post(_url, params=_kwargs, verbose=verbose)

    def _querymany(self, qterms, scopes=None, **kwargs):
        """Return the batch query result.
        This is a wrapper for POST query of "/query" service.

        :param qterms: a list/tuple/iterable of query terms, or a string of comma-separated query terms.
        :param scopes: specify the type (or types) of identifiers passed to **qterms**,
                       either a list or a comma-separated fields to specify type of input qterms.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned.
        :param returnall:   if True, return a dict of all related data, including dup. and missing qterms
        :param verbose:     if True (default), print out information about dup and missing qterms
        :param as_dataframe: if True or 1 or 2, return object as DataFrame (requires Pandas).
                                  True or 1: using json_normalize
                                  2        : using DataFrame.from_dict
                                  otherwise: return original json
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.
        :return: a list of matching objects or a pandas DataFrame object.

        .. Hint:: Passing a large list of ids (>1000) to :py:meth:`querymany` is perfectly fine.

        .. Hint:: If you need to pass a very large list of input qterms, you can pass a generator
                  instead of a full list, which is more memory efficient.

        """
        if isinstance(qterms, str_types):
            qterms = qterms.split(",") if qterms else []
        if not (isinstance(qterms, (list, tuple, Iterable))):
            raise ValueError('input "qterms" must be a list, tuple or iterable.')

        if scopes:
            kwargs["scopes"] = self._format_list(scopes, quoted=False)
        kwargs = self._handle_common_kwargs(kwargs)
        returnall = kwargs.pop("returnall", False)
        verbose = kwargs.pop("verbose", True)
        dataframe = kwargs.pop("as_dataframe", None)
        if dataframe in [True, 1]:
            dataframe = 1
        elif dataframe != 2:
            dataframe = None
        df_index = kwargs.pop("df_index", True)
        return_raw = kwargs.get("return_raw", False)
        if return_raw:
            dataframe = None

        out = []
        li_missing = []
        li_dup = []
        li_query = []

        def query_fn(qterms):
            return self._querymany_inner(qterms, verbose=verbose, **kwargs)

        for hits in self._repeated_query(query_fn, qterms, verbose=verbose):
            if return_raw:
                out.append(hits)  # hits is the raw response text
            else:
                out.extend(hits)
                for hit in hits:
                    if hit.get("notfound", False):
                        li_missing.append(hit["query"])
                    else:
                        li_query.append(hit["query"])

        if verbose:
            logger.info("Finished.")
        if return_raw:
            if len(out) == 1:
                out = out[0]
            return out

        # check dup hits
        if li_query:
            li_dup = [(query, cnt) for query, cnt in list_itemcnt(li_query) if cnt > 1]
            del li_query

        if dataframe:
            out = self._dataframe(out, dataframe, df_index=df_index)
            li_dup_df = DataFrame.from_records(li_dup, columns=["query", "duplicate hits"])
            li_missing_df = DataFrame(li_missing, columns=["query"])

        if verbose:
            if li_dup:
                logger.warning("{0} input query terms found dup hits:".format(len(li_dup)) + "\t" + str(li_dup)[:100])
            if li_missing:
                logger.warning(
                    "{0} input query terms found no hit:".format(len(li_missing)) + "\t" + str(li_missing)[:100]
                )

        if returnall:
            if dataframe:
                return {"out": out, "dup": li_dup_df, "missing": li_missing_df}
            else:
                return {"out": out, "dup": li_dup, "missing": li_missing}
        else:
            if verbose and (li_dup or li_missing):
                logger.info('Pass "returnall=True" to return complete lists of duplicate or missing query terms.')
            return out
